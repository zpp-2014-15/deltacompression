"""Tests for compression_algorithm.py"""

import unittest

from deltacompression.backend import compression_algorithm


class DummyCompressionAlgorithmTest(unittest.TestCase):

    def setUp(self):
        self._algorithm = compression_algorithm.DummyCompressionAlgorithm()

    def testCompression(self):
        data = "Lorem ipsum dolor sit amet"
        self.assertEqual(self._algorithm.compress(data), data)

    def testDecompression(self):
        data = "Lorem ipsum dolor sit amet"
        self.assertEqual(self._algorithm.decompress(data), data)
