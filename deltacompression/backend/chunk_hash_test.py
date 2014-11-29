"""Tests for chunk_hash.py."""
import unittest

from deltacompression.backend import storage
from deltacompression.backend import chunk_hash


class HashSHA256Test(unittest.TestCase):

    def setUp(self):
        self._sha_hash = chunk_hash.HashSHA256()

    def testSampleHash(self):
        chunk = storage.Chunk("asd")
        exp = ("h\x87\x87\xd8\xff\x14LP,\x7f\\\xff\xaa\xfe,\xc5\x88\xd8`y\xf9"
               "\xde\x880L&\xb0\xcb\x99\xce\x91\xc6")
        self.assertEqual(exp, self._sha_hash.calculateHash(chunk))


if __name__ == "__main__":
    unittest.main()
