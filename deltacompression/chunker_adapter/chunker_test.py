"""Tests for chunker.py"""

import os
import os.path as op
import unittest

from deltacompression.chunker_adapter import chunker


class ChunkerTest(unittest.TestCase):
    """ Test for the Chunker class. """

    file_name = op.join(op.abspath(op.dirname(__file__)), "__test_file__")
    bad_file_name = "___surely_there_is_no_such_file___"

    def setUp(self):
        self._chunker = chunker.Chunker(1000, 7000)

    def _testChunking(self, cont):
        with open(self.file_name, "w") as tfile:
            tfile.write(cont)
        try:
            ncont = "".join(
                [chunk.get() for chunk in self._chunker.chunkData(
                    self.file_name)])
        finally:
            os.remove(self.file_name)
        self.assertEqual(cont, ncont)

    def testFileWithData(self):
        cont = ",".join([str(i) for i in xrange(15000)])
        self._testChunking(cont)

    def testEmptyFile(self):
        self._testChunking("")

    def testSmallFile(self):
        self._testChunking("a")

    def testBadFile(self):
        """Testing chunker's behaviour after passing nonexistent file."""
        with self.assertRaises(chunker.ChunkerException):
            list(self._chunker.chunkData(self.bad_file_name))

if __name__ == "__main__":
    unittest.main()
