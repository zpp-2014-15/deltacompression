"""Tests for compression.py"""

import unittest

from deltacompression.backend import compression


class DummyCompressionTest(unittest.TestCase):

    def setUp(self):
        self._algorithm = compression.DummyCompression()

    def testCompression(self):
        data = "Lorem ipsum dolor sit amet"
        self.assertEqual(self._algorithm.compress(data), data)

    def testDecompression(self):
        data = "Lorem ipsum dolor sit amet"
        self.assertEqual(self._algorithm.decompress(data), data)
