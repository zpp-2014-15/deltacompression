"""Tests for data_updater.py."""

import unittest

from deltacompression.backend import data_updater
from deltacompression.backend import storage
from deltacompression.backend import chunk_hash
from deltacompression.backend import chunk_update
from deltacompression.backend import test_utils


class DummyUpdaterTest(unittest.TestCase):
    """Tests for class DummyUpdater."""

    def setUp(self):
        self._hash_function = chunk_hash.HashSHA256()
        self._storage = storage.Storage(self._hash_function, None)
        self._updater = data_updater.DummyUpdater(self._storage)

    def testUpdate(self):
        data = "some data"
        chunk = storage.Chunk(data)
        update = self._updater.update(chunk)
        self.assertEqual(update.getNewChunk().get(), data)
        self.assertIs(self._updater.update(chunk), None)

    def testaddReceivedData(self):
        cont = ["spam", "eggs"]
        data_pieces = []
        for chunk in [storage.Chunk(data) for data in cont]:
            update = chunk_update.DummyChunkUpdate(chunk)
            data_pieces.append(update.serialize())
        data = "".join(data_pieces)
        self._updater.addReceivedData(data)
        self.assertEqual(set(cont),
                         set([ch.get() for ch in self._storage.getChunks()]))


class DeltaUpdaterTest(unittest.TestCase):

    def setUp(self):
        self._hash_function = chunk_hash.HashSHA256()
        self._storage = storage.Storage(self._hash_function, None)
        self._diff = test_utils.MockupDiff()
        self._updater = data_updater.OptimalDeltaUpdater(self._storage,
                                                         self._diff)

    def testAddReceivedData(self):
        cont = ["I sleep all night", "I sleep all day"]
        chunks = [storage.Chunk(data) for data in cont]
        update1 = chunk_update.DeltaChunkUpdate(None, chunks[0].get())
        hash_value = self._hash_function.calculateHash(chunks[0])
        diff = self._diff.calculateDiff(chunks[0], chunks[1])
        update2 = chunk_update.DeltaChunkUpdate(hash_value, diff)
        data = update1.serialize() + update2.serialize()
        self._updater.addReceivedData(data)
        self.assertEqual(set(cont),
                         set([ch.get() for ch in self._storage.getChunks()]))


class OptimalDeltaUpdaterTest(unittest.TestCase):

    def setUp(self):
        self._hash_function = chunk_hash.HashSHA256()
        self._storage = storage.Storage(self._hash_function, None)
        self._diff = test_utils.PrefixDiff()
        self._updater = data_updater.OptimalDeltaUpdater(self._storage,
                                                         self._diff)

    def testUpdate(self):
        sent_bytes = 0
        for data in ["Oh, I'm a lumberjack, and I'm okay",
                     "I sleep all night and I work all day" * 2,
                     "I sleep all night and I work all day" * 2 + "aaa"]:
            chunk = storage.Chunk(data)
            update = self._updater.update(chunk)
            sent_bytes += update.getBinarySize()
            target_chunk = update.getNewChunk(
                diff=self._diff, storage=self._storage)
            self.assertEqual(target_chunk.get(), data)
            self.assertIs(self._updater.update(chunk), None)
        self.assertEqual(sent_bytes, 160)


class SimilarityIndexDeltaUpdaterTest(unittest.TestCase):
    """Test for class SimilarityIndex."""

    def setUp(self):
        self._hash_function = chunk_hash.HashSHA256()
        self._storage = storage.Storage(self._hash_function, None)
        self._diff = test_utils.PrefixDiff()
        par = data_updater.SimilarityIndexParams(fmod=4, ssize=2, win=2,
                                                 qmod=13, prim=5, pis=[(1, 2),
                                                                       (3, 4)])
        self._par = par
        self._updater = data_updater.SimilarityIndexDeltaUpdater(self._storage,
                                                                 self._diff,
                                                                 par)

    def testGetBestBase(self):
        all_sfeatures = {'1': [1, 2, 3, 4], '2': [1, 3, 5, 7],
                         '3': [1, 3, 4, 7], '4': [9, 11, 13, 20]}
        all_hashes = {1: ['1', '2', '3'], 2: ['1'], 3: ['2'], 4: ['3'],
                      5: ['2'], 7: ['2', '3'], 11: ['4'], 13: ['4'],
                      20: ['4']}
        self.assertEqual(self._updater.getBestBase([1, 5, 7, 20], all_sfeatures,
                                                   all_hashes),
                         '2')

    def testCreateSuperfeature(self):
        features = [1, 2, 3, 4, 10, 20]
        power = 1
        val = 0
        for feat in reversed(features):
            val += feat * power
            power *= self._par.prim
        val %= self._par.qmod
        self.assertEqual(self._updater.createSuperfeature(features), val)

    def testCalculateFeatures(self):
        chunk = storage.Chunk("".join(chr(x) for x in [1, 2, 3, 4, 5, 6, 7]))
        self.assertEqual(self._updater.calculateFeatures(chunk), [5, 5])
