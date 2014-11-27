"""Tests for data_updater.py."""

import unittest

from deltacompression.backend import data_updater
from deltacompression.backend import storage
from deltacompression.backend import chunk_hash


class DummyUpdaterTest(unittest.TestCase):
    """Tests for class DummyUpdater."""

    def setUp(self):
        self._hash_function = chunk_hash.HashSHA256()
        self._storage = storage.Storage(self._hash_function, None)
        self._updater = data_updater.DummyUpdater(self._storage)

    def testUpdate(self):
        chunk = storage.Chunk("some data")
        update = self._updater.update(chunk)
        self.assertEqual(update.getChunk().get(), chunk.get())
        self.assertIs(self._updater.update(chunk), None)
