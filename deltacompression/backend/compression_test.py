"""Tests for compression.py"""

import unittest

from deltacompression.backend import compression


class DummyCompressionTest(unittest.TestCase):

    def setUp(self):
        self._compression = compression.DummyCompression()

    def testCompression(self):
        data = "Lorem ipsum dolor sit amet"
        self.assertEqual(self._compression.compress(data), data)

    def testDecompression(self):
        data = "Lorem ipsum dolor sit amet"
        self.assertEqual(self._compression.decompress(data), data)
