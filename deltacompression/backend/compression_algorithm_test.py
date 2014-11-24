"""Tests for compression_algorithm.py"""

import unittest

from deltacompression.backend import compression_algorithm


class DummyCompressionAlgorithmTest(unittest.TestCase):

    def setUp(self):
        self._algorithm = compression_algorithm.DummyCompressionAlgorithm()

    def testCompression(self):
        data = ["Lorem ipsu", "m do", "", "lor sit", " amet"]
        self.assertEqual(self._algorithm.compress(data),
                         "Lorem ipsum dolor sit amet")

    def testGetName(self):
        self.assertEqual(self._algorithm.getName(),
                         "Dummy Compression Algorithm")
