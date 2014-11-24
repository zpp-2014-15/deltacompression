"""Tests for file_processor.py"""

import unittest

from deltacompression.backend import file_processor
from deltacompression.backend import data_updater
from deltacompression.backend import storage
from deltacompression.backend import chunk_hash
from deltacompression.backend import compression_algorithm


class FileProcessorTest(unittest.TestCase):

    def setUp(self):
        self._storage = storage.Storage(chunk_hash.HashSHA256(), None)
        self._data_updater = data_updater.DummyUpdater(self._storage)
        self._compression_algorithm = compression_algorithm \
            .DummyCompressionAlgorithm()
        self._file_processor = file_processor.FileProcessor(
            self._data_updater, self._compression_algorithm, 1000, 2000)

