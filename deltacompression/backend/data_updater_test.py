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
        chunk1 = storage.Chunk("some data")
        hash1 = self._hash_function.calculateHash(chunk1)
        self.assertEqual(self._updater.update(chunk1), chunk1.get())
        self.assertEqual(self._updater.update(chunk1), hash1)
        self.assertEqual(self._updater.update(chunk1), hash1)

        chunk2 = storage.Chunk("other data")
        hash2 = self._hash_function.calculateHash(chunk2)
        self.assertEqual(self._updater.update(chunk2), chunk2.get())
        self.assertEqual(self._updater.update(chunk2), hash2)
        self.assertEqual(self._updater.update(chunk1), hash1)

    def testGetName(self):
        self.assertEqual(self._updater.getName(), "Dummy Updater")
