"""Tests for chunk_hash.py."""
import unittest

from deltacompression.backend import storage
from deltacompression.backend import chunk_hash


class HashSHA256Test(unittest.TestCase):

    def setUp(self):
        self._sha_hash = chunk_hash.HashSHA256()

    def testSampleHash(self):
        chunk = storage.Chunk("asd")
        exp = "688787d8ff144c502c7f5cffaafe2cc588d86079f9de88304c26b0cb99ce91c6"
        self.assertEqual(exp, self._sha_hash.calculateHash(chunk))


if __name__ == '__main__':
    unittest.main()
