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


class LzoCompression(unittest.TestCase):

    def setUp(self):
        self._compression = compression.LzoCompression()
        self._input = "Lorem ipsum dolor sit amet"
        self._compressed = ("\xf1\x00\x00\x00\x1a+Lorem ipsum dolor " +
                            "sit amet\x11\x00\x00")

    def testCompression(self):
        self.assertEqual(self._compression.compress(self._input),
                         self._compressed)

    def testDecompression(self):
        self.assertEqual(self._compression.decompress(self._compressed),
                         self._input)


class ZipCompression(unittest.TestCase):

    def setUp(self):
        self._compression = compression.ZipCompression()
        self._input = "Lorem ipsum dolor sit amet"
        self._compressed = ("x\xda\xf3\xc9/J\xcdU\xc8,(.\xcdUH\xc9\xcf" +
                            "\xc9/R(\xce,QH\xccM-\x01\x00\x83\xd5\t\xc5")

    def testCompresion(self):
        self.assertEqual(self._compression.compress(self._input),
                         self._compressed)

    def testDecompression(self):
        self.assertEqual(self._compression.decompress(self._compressed),
                         self._input)
