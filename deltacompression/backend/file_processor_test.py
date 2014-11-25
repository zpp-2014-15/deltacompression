"""Tests for file_processor.py"""

import os
import os.path as op

import unittest

from deltacompression.backend import file_processor
from deltacompression.backend import data_updater
from deltacompression.backend import storage
from deltacompression.backend import chunk_hash
from deltacompression.backend import compression_algorithm


class FileProcessorTest(unittest.TestCase):
    """Test for class FileProcessor."""

    file_name = op.join(op.abspath(op.dirname(__file__)), "__test_file__")

    def setUp(self):
        self._storage = storage.Storage(chunk_hash.HashSHA256(), None)
        self._data_updater = data_updater.DummyUpdater(self._storage)
        self._compression_algorithm = compression_algorithm \
            .DummyCompressionAlgorithm()
        self._file_processor = file_processor.FileProcessor(
            self._data_updater, self._compression_algorithm, 1000, 7000)

    def testFileProcessor(self):
        with open(self.file_name, "w") as tfile:
            cont = ",".join([str(i) for i in xrange(15000)])
            tfile.write(cont)

        try:
            compressed_data = self._file_processor.processFile(self.file_name)
            self.assertEqual(compressed_data, cont)
        finally:
            os.remove(self.file_name)
