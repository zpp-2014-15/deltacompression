"""Tests for storage.py."""

import unittest

from deltacompression.backend import storage
from deltacompression.backend import chunk_hash


class SimpleHasher(chunk_hash.HashFunction):

    def calculateHash(self, chunk):
        return sum(map(ord, chunk.get()))


class StorageTest(unittest.TestCase):
    """Tests for Storage class."""

    def setUp(self):
        self._hasher = SimpleHasher()
        self._storage = storage.Storage(self._hasher, None)

    def testAddChunk(self):
        chunk1 = storage.Chunk("aaa")
        chunk2 = storage.Chunk("bbb")
        chunk1_hash = self._hasher.calculateHash(chunk1)
        chunk2_hash = self._hasher.calculateHash(chunk2)
        returned_hash1 = self._storage.addChunk(chunk1)
        returned_hash2 = self._storage.addChunk(chunk2)

        self.assertEqual(chunk1_hash, returned_hash1)
        self.assertEqual(chunk2_hash, returned_hash2)

    def testGetChunk(self):
        chunk1 = storage.Chunk("aaa")
        chunk2 = storage.Chunk("bbb")
        hash1 = self._storage.addChunk(chunk1)
        hash2 = self._storage.addChunk(chunk2)

        self.assertEqual("aaa", self._storage.getChunk(hash1).get())
        self.assertEqual("bbb", self._storage.getChunk(hash2).get())

    def testAddChunkRaisesWhenChunkExists(self):
        chunk1 = storage.Chunk("aaa")
        self._storage.addChunk(chunk1)
        self.assertRaises(storage.StorageException, self._storage.addChunk,
                          chunk1)

    def testGetChunkRaisesWhenChunkDoesNotExist(self):
        self.assertRaises(storage.StorageException, self._storage.getChunk, 123)

    def testContainsHash(self):
        chunk1 = storage.Chunk("aaa")
        hash1 = self._storage.addChunk(chunk1)
        self.assertTrue(self._storage.containsHash(hash1))
        self.assertFalse(self._storage.containsHash(123))

    def testContainsChunk(self):
        chunk1 = storage.Chunk("aaa")
        self.assertFalse(self._storage.containsChunk(chunk1))
        self._storage.addChunk(chunk1)
        self.assertTrue(self._storage.containsChunk(chunk1))

    def testGetHashOfChunk(self):
        chunk1 = storage.Chunk("aaa")
        hash1 = self._hasher.calculateHash(chunk1)

        with self.assertRaises(storage.StorageException):
            self._storage.getHashOfChunk(chunk1)

        self._storage.addChunk(chunk1)
        self.assertEqual(self._storage.getHashOfChunk(chunk1), hash1)


class ChunkTest(unittest.TestCase):

    def testGet(self):
        chunk = storage.Chunk("asd")
        self.assertEqual(chunk.get(), "asd")

        chunk2 = storage.Chunk("dsa")
        self.assertEqual(chunk2.get(), "dsa")

if __name__ == "__main__":
    unittest.main()
