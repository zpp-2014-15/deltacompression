"""Tests for data_updater.py."""

import unittest

from deltacompression.backend import data_updater
from deltacompression.backend import storage
from deltacompression.backend import chunk_hash
from deltacompression.backend import chunk_update


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
        self.assertEqual(update.getChunk().get(), data)
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
