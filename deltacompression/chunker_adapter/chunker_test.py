"""Tests for chunker.py"""

import unittest
from deltacompression.chunker_adapter.chunker import Chunker
import os
import os.path as op

class ChunkerTest(unittest.TestCase):
    """ Test for the Chunker class. """

    file_name = op.join(op.abspath(op.dirname(__file__)), '__test_file__')

    def __init__(self, *args, **kwargs):
        super(ChunkerTest, self).__init__(*args, **kwargs)
        self._chunker = None

    def setUp(self):
        self._chunker = Chunker(1000, 7000)

    def testChunking(self):
        with open(self.file_name, 'w') as tfile:
            cont = ",".join([str(i) for i in xrange(15000)])
            tfile.write(cont)
        try:
            ncont = "".join(
                [chunk.get() for chunk in self._chunker.chunkData(
                    self.file_name)])
        finally:
            os.remove(self.file_name)
        self.assertEqual(cont, ncont)


if __name__ == '__main__':
    unittest.main()
