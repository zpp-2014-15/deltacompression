# -*- coding: utf-8 -*-
"""Tests for chunker.py"""

import os
import os.path as op
import unittest
import shutil

from deltacompression.chunker_adapter import chunker


class ChunkerTest(unittest.TestCase):
    """ Test for the Chunker class. """

    cur_dir = op.abspath(op.dirname(__file__))
    file_name = op.join(cur_dir, "__test_file__")
    dir_name = op.join(cur_dir, "___secret_test_directory___")
    bad_file_name = "___surely_there_is_no_such_file___"

    def setUp(self):
        self._chunker = chunker.Chunker(
            chunker.ChunkerParameters(1000, 13000, 7000))

    def _testChunking(self, cont, file_name=None):
        if file_name is None:
            file_name = self.file_name
        with open(file_name, "w") as tfile:
            tfile.write(cont)
        try:
            ncont = "".join(
                [chunk.get() for chunk in self._chunker.chunkData([file_name])])
        finally:
            os.remove(file_name)
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

    def testFileWithSpecialCharacters(self):
        file_names = [u"__tęst_filęs__",
                      u"__teśt_fileś__",
                      u"__tesß_fiπœs__",
                      u"__≠€½«…→þþż↓←ę§³¢²«·§»__"]
        for file_name in file_names:
            self._testChunking("a", file_name)

    def test_many_files(self):
        files = [op.join(self.dir_name, n) for n in ["a", "b", "c"]]
        conts = ["aaaa", "bbbb", "cccc"]
        try:
            os.mkdir(self.dir_name)
            for file_name, cont in zip(files, conts):
                with open(file_name, "w") as fil:
                    fil.write(cont)
            ncont = "".join(
                [chunk.get() for chunk in self._chunker.chunkData(files)])
            cont = "".join(conts)
            self.assertEqual(cont, ncont)
        finally:
            shutil.rmtree(self.dir_name)


if __name__ == "__main__":
    unittest.main()
