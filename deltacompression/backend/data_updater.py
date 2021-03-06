"""This module contains class responsible for adding chunks to the storage."""

import collections
import itertools

from deltacompression.backend import features_calculator
from deltacompression.backend import chunk_update


class DataUpdater(object):
    """Class responsible for adding new chunks to the storage."""

    def __init__(self, storage_object):
        """Creates DataUpdater object.

        Args:
            storageObject: instance of Storage.
        """
        self._storage = storage_object

    def update(self, chunk):
        if self._storage.containsChunk(chunk):
            if self.getLogger():
                self.getLogger().incDuplicates()
            return None
        else:
            if self.getLogger():
                self.getLogger().incTotalBlocks()
            return self.addNewChunk(chunk)

    def addNewChunk(self, new_chunk):
        """Adds new chunk to the storage.

        Args:
            chunk: instance of Chunk that will be added to the storage.
        Returns:
            ChunkUpdate object for the given chunk.
        """
        raise NotImplementedError

    def getLogger(self):
        return self._storage.getLogger()

    def addReceivedData(self, decompressed_data):
        """Updates the storage with the decompressed data received from another
        storage."""
        raise NotImplementedError


class DummyUpdater(DataUpdater):

    def addNewChunk(self, chunk):
        self._storage.addChunk(chunk)
        return chunk_update.DummyChunkUpdate(chunk)

    def addReceivedData(self, data):
        while data:
            update = chunk_update.DummyChunkUpdate.deserialize(data)
            self._storage.addChunk(update.getNewChunk())
            data = data[update.getBinarySize():]


class DeltaUpdater(DataUpdater):

    def __init__(self, storage_obj, diff):
        super(DeltaUpdater, self).__init__(storage_obj)
        self._diff = diff

    def addReceivedData(self, data):
        while data:
            update = chunk_update.DeltaChunkUpdate.deserialize(
                data, hash_size=self._storage.getHashFunction().getHashSize())
            new_chunk = update.getNewChunk(storage=self._storage,
                                           diff=self._diff)
            self._storage.addChunk(new_chunk)
            data = data[update.getBinarySize():]


class OptimalDeltaUpdater(DeltaUpdater):

    def addNewChunk(self, chunk):
        best_update = chunk_update.DeltaChunkUpdate(None, chunk.get())
        for base in self._storage.getChunks():
            diff = self._diff.calculateDiff(base, chunk)
            hash_value = self._storage.getHashOfChunk(base)
            update = chunk_update.DeltaChunkUpdate(hash_value, diff)
            if update.getBinarySize() < best_update.getBinarySize():
                best_update = update
        self._storage.addChunk(chunk)
        return best_update


# ssize: number of features per superfeature.
# win: size of the rolling window in bytes.
# prim: prime for the Rabin fingerprint.
# qmod: prime for the Rabin fingerprint modulo operation.
# pis: list of coprime pairs (multiplier, adder) for every pi function;
        # its length should be divisible by ssize.
# fmod: value for modulo operation in pi functions
SimilarityIndexParams = collections.namedtuple("SimilarityIndexParams",
                                               "ssize win prim qmod pis fmod")

class SimilarityIndexDeltaUpdater(DeltaUpdater):
    """A class for a delta encoding algorithm which uses similarity index."""

    def __init__(self, storage_obj, diff, par):
        """Delta updater using similarity index.

        Args:
            par: SimilarityIndexParams object.
        """
        super(SimilarityIndexDeltaUpdater, self).__init__(storage_obj, diff)
        self._par = par

        values = itertools.chain([par.prim, par.qmod, par.fmod], *par.pis)
        if [x for x in values if x > 10 ** 9]:
            raise ValueError("All the parameters must not exceed 10^9")
        # mapping chunk's hash to its superfeatures' list
        self._sfeatures = {}
        # mapping superfeatures to lists of hashes
        self._hashes = {}

    def calculateFeatures(self, chunk):
        """Calculating all the features per chunk (perhaps for many
        superfeatures).

        Returns:
            a list of consecutive features.
        """
        par = self._par
        return features_calculator.calculateFeatures(chunk.get(), par.prim,
                                                     par.qmod, par.win,
                                                     par.fmod, par.pis)

    def createSuperfeature(self, features):
        """Create a superfeature from the feature's list."""
        value = 0
        for feature in features:
            value = (value * self._par.prim + feature) % self._par.qmod
        return value

    def getBestBase(self, sfeatures, all_sfeatures, all_hashes):
        hashes = set([])
        for sfeature in sfeatures:
            hashes |= set(all_hashes.get(sfeature, []))

        best = (0, None)
        for hval in hashes:
            common = len(set(all_sfeatures.get(hval, [])) & set(sfeatures))
            if common > best[0]:
                best = common, hval

        return best[1]

    def addNewChunk(self, chunk):
        features = self.calculateFeatures(chunk)
        sfeatures = [self.createSuperfeature(features[x:x + self._par.ssize])
                     for x in xrange(0, len(features), self._par.ssize)]

        best_hash = self.getBestBase(sfeatures, self._sfeatures, self._hashes)
        best_update = chunk_update.DeltaChunkUpdate(None, chunk.get())
        if best_hash:
            base = self._storage.getChunk(best_hash)
            diff = self._diff.calculateDiff(base, chunk)
            update = chunk_update.DeltaChunkUpdate(best_hash, diff)
            if update.getBinarySize() < best_update.getBinarySize():
                best_update = update

        ch_hash = self._storage.addChunk(chunk)
        for sfeature in sfeatures:
            hashes = self._hashes.get(sfeature, [])
            hashes.append(ch_hash)
            self._hashes[sfeature] = hashes
        self._sfeatures[ch_hash] = sfeatures

        return best_update
