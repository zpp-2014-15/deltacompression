"""Tests for file_processor.py"""

import os
import os.path as op

import unittest

from deltacompression.backend import file_processor
from deltacompression.backend import data_updater
from deltacompression.backend import storage
from deltacompression.backend import chunk_hash


class FileProcessorTest(unittest.TestCase):
    """Test for class FileProcessor."""

    file_name = op.join(op.abspath(op.dirname(__file__)), "__test_file__")

    def setUp(self):
        self._storage = storage.Storage(chunk_hash.HashSHA256(), None)
        self._data_updater = data_updater.DummyUpdater(self._storage)
        self._file_processor = file_processor.FileProcessor(
            self._data_updater, 1000, 7000)

    def _sendDataTest(self, cont):
        """Testing sending data to a remote Storage."""

        with open(self.file_name, "w") as tfile:
            tfile.write(cont)
        try:
            remote_storage = storage.Storage(chunk_hash.HashSHA256(), None)
            remote_updater = data_updater.DummyUpdater(remote_storage)
            data = self._file_processor.processFiles([self.file_name])
            remote_updater.addReceivedData(data)
            self.assertEqual(
                set([ch.get() for ch in self._storage.getChunks()]),
                set([ch.get() for ch in remote_storage.getChunks()]))
        finally:
            os.remove(self.file_name)

    def testDifferentBlocks(self):
        self._sendDataTest(",".join([str(i) for i in xrange(15000)]))

    def testSameBlocks(self):
        self._sendDataTest("0" * 30000)
