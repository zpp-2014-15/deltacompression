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
        self._diff_algorithm = test_utils.MockupDiff()
        self._updater = data_updater.OptimalDeltaUpdater(self._storage,
                                                         self._diff_algorithm)

    def testAddReceivedData(self):
        cont = ["I sleep all night", "I sleep all day"]
        chunks = [storage.Chunk(data) for data in cont]
        update1 = chunk_update.DeltaChunkUpdate(None, chunks[0].get())
        hash_value = self._hash_function.calculateHash(chunks[0])
        diff = self._diff_algorithm.calculateDiff(chunks[0], chunks[1])
        update2 = chunk_update.DeltaChunkUpdate(hash_value, diff)
        data = update1.serialize() + update2.serialize()
        self._updater.addReceivedData(data)
        self.assertEqual(set(cont),
                         set([ch.get() for ch in self._storage.getChunks()]))


class OptimalDeltaUpdaterTest(unittest.TestCase):

    def setUp(self):
        self._hash_function = chunk_hash.HashSHA256()
        self._storage = storage.Storage(self._hash_function, None)
        self._diff_algorithm = test_utils.PrefixDiff()
        self._updater = data_updater.OptimalDeltaUpdater(self._storage,
                                                         self._diff_algorithm)

    def testUpdate(self):
        sent_bytes = 0
        for data in ["Oh, I'm a lumberjack, and I'm okay",
                     "I sleep all night and I work all day" * 2,
                     "I sleep all night and I work all day" * 2 + "aaa"]:
            chunk = storage.Chunk(data)
            update = self._updater.update(chunk)
            sent_bytes += update.getBinarySize()
            target_chunk = update.getNewChunk(
                diff_algorithm=self._diff_algorithm, storage=self._storage)
            self.assertEqual(target_chunk.get(), data)
            self.assertIs(self._updater.update(chunk), None)
        self.assertEqual(sent_bytes, 160)
