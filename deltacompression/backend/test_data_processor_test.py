"""Tests for directory_processor.py"""

import os
import os.path as op
import shutil

import unittest

from deltacompression.backend import directory_processor
from deltacompression.backend import test_data_processor
from deltacompression.backend import data_updater
from deltacompression.backend import storage
from deltacompression.backend import chunk_hash
from deltacompression.backend import compression_algorithm


class DirectoryProcessorTest(unittest.TestCase):
    """Test for class D-irectoryProcessor."""

    test_dir_name = op.join(op.abspath(op.dirname(__file__)), "__test_dir__")

    def setUp(self):
        _storage = storage.Storage(chunk_hash.HashSHA256(), None)
        _data_updater = data_updater.DummyUpdater(_storage)
        _compression_algorithm = compression_algorithm \
            .DummyCompressionAlgorithm()
        self._directory_processor = directory_processor.DirectoryProcessor(
            _data_updater, _compression_algorithm, 1000, 7000)
        self._test_data_processor = test_data_processor.TestDataProcessor(
            self._directory_processor)

    def testDupa(self):
        directory = '/home/pkura/code/zpp/test'
        #return
        for x, y in self._test_data_processor.runSimulation(directory):
            print x, len(y)
