# pylint: disable=E1120
# no-value-for-parameter - pylint don't know how mocks work

"""Tests for directory_processor.py"""

import os.path as op
import unittest

import mock
import testfixtures

from deltacompression.backend import directory_processor
from deltacompression.backend import data_updater
from deltacompression.backend import storage
from deltacompression.backend import chunk_hash
from deltacompression.backend import compression_algorithm
from deltacompression.backend import test_utils


class DirectoryProcessorTest(unittest.TestCase):
    """Test for class DirectoryProcessor."""

    def setUp(self):
        storage_instance = storage.Storage(chunk_hash.HashSHA256(), None)
        data_updater_instance = data_updater.DummyUpdater(storage_instance)
        compression_algorithm_instance = compression_algorithm \
            .DummyCompressionAlgorithm()
        self._directory_processor = directory_processor.DirectoryProcessor(
            data_updater_instance, compression_algorithm_instance, 1000, 7000)

    def _processDirectory(self, tmp_dir, dir_path):
        data = []

        full_path = op.join(tmp_dir.path, dir_path)
        data.append(self._directory_processor.processDirectory(full_path))

        return data

    @mock.patch("deltacompression.backend.file_processor.FileProcessor",
                autospec=True)
    def _testProcessDirectory(self, files, contents, mock_file_processor):
        self.setUp()
        with testfixtures.TempDirectory() as tmp_dir:
            files = [op.join("some_dir", f) for f in files]
            dir_content = zip(files, contents)
            test_utils.fillTempDirectoryWithContent(tmp_dir, dir_content)

            self._processDirectory(tmp_dir, "some_dir")
            args = mock_file_processor.return_value.processFiles.call_args
            self.assertEqual(
                set(args[0][0]), set([op.join(tmp_dir.path, f)
                                      for f in files]))

    def testEmptyDirectory(self):
        contents = []
        files = []
        self._testProcessDirectory(files, contents)

    def testDirectoryWithOneFile(self):
        contents = [",".join([str(i) for i in xrange(15000)])]
        files = ["file.txt"]
        self._testProcessDirectory(files, contents)

    def testDirectoryWithSomeFiles(self):
        contents = [",".join([str(i) for i in xrange(15000)])] * 4
        files = ["file.txt", "file2.avi", "file3", "aaa"]
        self._testProcessDirectory(files, contents)

    def testDirectoryWithSubdirectories(self):
        contents = [",".join([str(i) for i in xrange(15000)])] * 5
        files = ["file.txt", "A/file2.avi", "B/file3", "C/aaa", "A/B/C/bbb"]
        self._testProcessDirectory(files, contents)
