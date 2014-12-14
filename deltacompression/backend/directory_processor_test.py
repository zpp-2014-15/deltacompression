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

    def _createAndProcessDirectories(self, tmp_dir, dirs_content):
        """Creates directories with given content and then processes them.
        Args:
            tmp_dir: instance of TempDirectory.
            dirs_content: a list of pairs (dir_path, dir_content),
                          where dir_content is a list of pairs
                          (file_name, file_content)
        Returns:
            a list of results for every directory.
        """

        data = []
        for dir_path, dir_content in dirs_content:
            test_utils.fillTempDirectoryWithContent(tmp_dir, dir_content)
            full_path = op.join(tmp_dir.path, dir_path)
            data.append(self._directory_processor.processDirectory(full_path))

        return data

    @mock.patch("deltacompression.backend.file_processor.FileProcessor",
                autospec=True)
    def testEmptyDirectory(self, mock_file_processor):
        self.setUp()
        with testfixtures.TempDirectory() as tmp_dir:
            contents = []
            files = []
            dir_content = zip(
                [op.join("v1", file_name) for file_name in files], contents)
            self._createAndProcessDirectories(tmp_dir, [("v1", dir_content)])

            args = mock_file_processor.return_value.processFiles.call_args
            self.assertEqual(args[0][0], [])

    @mock.patch("deltacompression.backend.file_processor.FileProcessor",
                autospec=True)
    def testDirectoryWithOneFile(self, mock_file_processor):
        self.setUp()
        with testfixtures.TempDirectory() as tmp_dir:
            contents = [",".join([str(i) for i in xrange(15000)])]
            files = ["file.txt"]
            dir_content = zip(
                [op.join("v1", file_name) for file_name in files], contents)
            self._createAndProcessDirectories(tmp_dir, [("v1", dir_content)])

            args = mock_file_processor.return_value.processFiles.call_args
            self.assertEqual(
                args[0][0], [op.join(tmp_dir.path,
                                     op.join("v1", f)) for f in files])

    @mock.patch("deltacompression.backend.file_processor.FileProcessor",
                autospec=True)
    def testDirectoryWithSomeFiles(self, mock_file_processor):
        self.setUp()
        with testfixtures.TempDirectory() as tmp_dir:
            contents = [",".join([str(i) for i in xrange(15000)])] * 4
            files = ["file.txt", "file2.avi", "file3", "aaa"]
            dir_content = zip(
                [op.join("v1", file_name) for file_name in files], contents)
            self._createAndProcessDirectories(tmp_dir, [("v1", dir_content)])

            args = mock_file_processor.return_value.processFiles.call_args
            self.assertEqual(
                set(args[0][0]), set([op.join(tmp_dir.path, op.join("v1", f))
                                      for f in files]))

    @mock.patch("deltacompression.backend.file_processor.FileProcessor",
                autospec=True)
    def testDirectoryWithSubdirectories(self, mock_file_processor):
        self.setUp()
        with testfixtures.TempDirectory() as tmp_dir:
            contents = [",".join([str(i) for i in xrange(15000)])] * 5
            files = ["file.txt", "A/file2.avi", "B/file3", "C/aaa", "A/B/C/bbb"]
            dir_content = zip(
                [op.join("v1", file_name) for file_name in files], contents)
            self._createAndProcessDirectories(tmp_dir, [("v1", dir_content)])

            args = mock_file_processor.return_value.processFiles.call_args
            self.assertEqual(
                set(args[0][0]), set([op.join(tmp_dir.path, op.join("v1", f))
                                      for f in files]))
