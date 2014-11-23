"""Tests for chunker.py"""

import os
import os.path as op
import unittest

from deltacompression.chunker_adapter.chunker import Chunker, ChunkerException


class ChunkerTest(unittest.TestCase):
    """ Test for the Chunker class. """

    file_name = op.join(op.abspath(op.dirname(__file__)), "__test_file__")
    bad_file_name = "___surely_there_is_no_such_file___"

    def setUp(self):
        self._chunker = Chunker(1000, 7000)

    def testChunking(self):
        # due to chunker module's limitations we can't actually test it on
        # smaller data
        with open(self.file_name, "w") as tfile:
            cont = ",".join([str(i) for i in xrange(15000)])
            tfile.write(cont)
        try:
            ncont = "".join(
                [chunk.get() for chunk in self._chunker.chunkData(
                    self.file_name)])
        finally:
            os.remove(self.file_name)
        self.assertEqual(cont, ncont)

    def testBadFile(self):
        """Testing chunker's behaviour after passing nonexistent file."""
        try:
            ret = [i for i in self._chunker.chunkData(self.bad_file_name)]
            self.assertFalse(ret)
        except ChunkerException:
            pass


if __name__ == "__main__":
    unittest.main()
