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


class ChunkTest(unittest.TestCase):

    def testGet(self):
        chunk = storage.Chunk("asd")
        self.assertEqual(chunk.get(), "asd")

        chunk2 = storage.Chunk("dsa")
        self.assertEqual(chunk2.get(), "dsa")

if __name__ == '__main__':
    unittest.main()
