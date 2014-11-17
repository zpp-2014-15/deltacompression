"""Tests for storage.py."""

import unittest

from deltacompression import storage


# TODO(marseel): should be derivied class of HashFunction
class SimpleHasher(object):

    def computeHash(self, chunk):
        """Computes hash.

        Args:
            chunk: string
        Returns:
            Integer"""
        return sum(map(ord, chunk))


class StorageTest(unittest.TestCase):
    """Tests for Storage class."""

    def setUp(self):
        self._hasher = SimpleHasher()
        self._storage = storage.Storage(self._hasher, None)

    def testAddChunk(self):
        chunk1 = "aaa"
        chunk2 = "bbb"
        chunk1_hash = self._hasher.computeHash(chunk1)
        chunk2_hash = self._hasher.computeHash(chunk2)
        returned_hash1 = self._storage.addChunk(chunk1)
        returned_hash2 = self._storage.addChunk(chunk2)

        self.assertEqual(chunk1_hash, returned_hash1)
        self.assertEqual(chunk2_hash, returned_hash2)

    def testGetChunk(self):
        chunk1 = "aaa"
        chunk2 = "bbb"
        hash1 = self._storage.addChunk(chunk1)
        hash2 = self._storage.addChunk(chunk2)

        self.assertEqual("aaa", self._storage.getChunk(hash1))
        self.assertEqual("bbb", self._storage.getChunk(hash2))

    def testAddChunkRaisesWhenChunkExists(self):
        self._storage.addChunk("aaa")
        self.assertRaises(storage.StorageException, self._storage.addChunk, "aaa")

    def testGetChunkRaisesWhenChunkDoesNotExist(self):
        self.assertRaises(storage.StorageException, self._storage.getChunk, 123)

    def testContainsHash(self):
        hash1 = self._storage.addChunk("aaa")
        self.assertTrue(self._storage.containsHash(hash1))
        self.assertFalse(self._storage.containsHash(123))


if __name__ == '__main__':
    unittest.main()
