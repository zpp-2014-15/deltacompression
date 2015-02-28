"""This module contains class responsible for adding chunks to the storage."""

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
        """Adds chunk to the storage.

        Args:
            chunk: instance of Chunk that will be added to the storage.
        Returns:
            ChunkUpdate object for the given chunk.
        """
        raise NotImplementedError

    def addReceivedData(self, decompressed_data):
        """Updates the storage with the decompressed data received from another
        storage."""
        raise NotImplementedError


class DummyUpdater(DataUpdater):

    def update(self, chunk):
        if not self._storage.containsChunk(chunk):
            self._storage.addChunk(chunk)
            return chunk_update.DummyChunkUpdate(chunk)
        else:
            return None

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

    def update(self, chunk):
        if self._storage.containsChunk(chunk):
            return None
        best_update = chunk_update.DeltaChunkUpdate(None, chunk.get())
        for base in self._storage.getChunks():
            diff = self._diff.calculateDiff(base, chunk)
            hash_value = self._storage.getHashOfChunk(base)
            update = chunk_update.DeltaChunkUpdate(hash_value, diff)
            if update.getBinarySize() < best_update.getBinarySize():
                best_update = update
        self._storage.addChunk(chunk)
        return best_update


class SimilarityIndexParams(object):
    """All the parameters of delta updater with similarity index.

    Attributes:
        fmod: value for calculating value of feature
        ssize: number of features per superfeature.
        win: size of the rolling window in bytes.
        prim: prime for the Rabin fingerprint.
        qmod: prime for the Rabin fingerprint modulo operation.
        pis: list of coprime pairs (multiplier, adder) for every pi function;
             its length should be divisible by ssize.
    """
    fmod = None
    ssize = None
    win = None
    prim = None
    qmod = None
    pis = None


class SimilarityIndexDeltaUpdater(DeltaUpdater):
    """A class for a delta encoding algorithm which uses similarity index."""

    def __init__(self, storage_obj, diff, par):
        """Delta updater using similarity index.

        Args:
            par: SimilarityIndexParams object.
        """
        super(SimilarityIndexDeltaUpdater, self).__init__(storage_obj, diff)
        # TODO some validation of parameters?
        self._par = par
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
        data = chunk.get()
        val = 0
        ppow = (par.prim ** (par.win - 1)) % par.qmod
        best = [-1] * len(par.pis)
        features = [0] * len(par.pis)

        for byte in data[:par.win]:
            val = (val * par.prim + ord(byte)) % par.qmod

        for i, byte in enumerate(data[par.win:]):
            val = (val + (par.qmod - ord(data[i - par.win])) * ppow) % par.qmod
            val = (val * par.prim + ord(byte)) % par.qmod
            for i, (mul, add) in enumerate(par.pis):
                fval = (val * mul + add) % par.fmod
                if fval > best[i]:
                    best[i] = fval
                    features[i] = val

        return features

    def createSuperfeature(self, features):
        """Create a superfeature from the feature's list."""
        value = 0
        for feature in features:
            value = (value * self._par.prim + feature) % self._par.qmod
        return value

    def getCandidates(self, sfeatures):
        hashes = set([])
        for sfeature in sfeatures:
            hashes |= set(self._hashes.get(sfeature, []))
        return hashes

    def update(self, chunk):
        if self._storage.containsChunk(chunk):
            return None
        features = self.calculateFeatures(chunk)
        sfeatures = [self.createSuperfeature(features[x:x + self._par.ssize])
                     for x in xrange(0, len(features), self._par.ssize)]
        best = (0, None)
        for hval in self.getCandidates(sfeatures):
            common = len(set(self._sfeatures.get(hval, [])) & set(sfeatures))
            if common > best[0]:
                best = common, hval

        best_update = chunk_update.DeltaChunkUpdate(None, chunk.get())
        if best[1]:
            base = self._storage.getChunk(best[1])
            diff = self._diff.calculateDiff(base, chunk)
            update = chunk_update.DeltaChunkUpdate(best[1], diff)
            if update.getBinarySize() < best_update.getBinarySize():
                best_update = update

        ch_hash = self._storage.addChunk(chunk)
        for sfeature in sfeatures:
            hashes = self._hashes.get(sfeature, [])
            hashes.append(ch_hash)
            self._hashes[sfeature] = hashes
        self._sfeatures[ch_hash] = sfeatures

        return best_update
