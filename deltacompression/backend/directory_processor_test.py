"""Tests for directory_processor.py"""

import os.path as op
import unittest

import mock
import testfixtures

from deltacompression.backend import directory_processor
from deltacompression.backend import test_utils


class DirectoryProcessorTest(unittest.TestCase):
    """Test for class DirectoryProcessor."""

    def setUp(self):
        self._file_patcher = mock.patch("deltacompression.backend."
                                        "file_processor.FileProcessor",
                                        autospec=True)
        self._compression_patcher = mock.patch("deltacompression.backend."
                                               "compression.DummyCompression",
                                               autospec=True)
        self.addCleanup(self._file_patcher.stop)
        self.addCleanup(self._compression_patcher.stop)
        self._file_mock = self._file_patcher.start().return_value
        self._compression_mock = self._compression_patcher.start().return_value

        self._directory_processor = directory_processor.DirectoryProcessor(
            self._file_mock, self._compression_mock)

    def _testProcessDirectory(self, files, contents):
        with testfixtures.TempDirectory() as tmp_dir:
            dir_content = zip(files, contents)
            test_utils.fillTempDirectoryWithContent(tmp_dir, dir_content)

            self._directory_processor.processDirectory(tmp_dir.path)
            args = self._file_mock.processFiles.call_args
            self.assertEqual(
                set(args[0][0]), set([op.join(tmp_dir.path, f) for f in files]))

    def testEmptyDirectory(self):
        contents = []
        files = []
        self._testProcessDirectory(files, contents)

    def testDirectoryWithOneFile(self):
        contents = ["a" * 10]
        files = ["file.txt"]
        self._testProcessDirectory(files, contents)

    def testDirectoryWithSomeFiles(self):
        contents = ["a" * 10] * 4
        files = ["file.txt", "file2.avi", "file3", "aaa"]
        self._testProcessDirectory(files, contents)

    def testDirectoryWithSubdirectories(self):
        contents = ["a" * 10] * 5
        files = ["file.txt", "A/file2.avi", "B/file3", "C/aaa", "A/B/C/bbb"]
        self._testProcessDirectory(files, contents)
