"""Tests for directory_processor.py"""

import itertools
import os.path as op
import unittest

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
        _storage = storage.Storage(chunk_hash.HashSHA256(), None)
        _data_updater = data_updater.DummyUpdater(_storage)
        _compression_algorithm = compression_algorithm \
            .DummyCompressionAlgorithm()
        self._directory_processor = directory_processor.DirectoryProcessor(
            _data_updater, _compression_algorithm, 1000, 7000)

    def _processDirectories(self, tmp_dir, dirs_content):
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

    def testProcessDirectory(self):
        combinations = itertools.product(
            test_utils.EXAMPLE_CONTENTS, test_utils.EXAMPLE_CONTENTS,
            test_utils.EXAMPLE_FILES, test_utils.EXAMPLE_FILES)

        for cont1, cont2, files1, files2 in combinations:
            self.setUp()
            with testfixtures.TempDirectory() as tmp_dir:
                dir_content1 = zip(
                    [op.join("v1", file_name) for file_name in files1], cont1)
                dir_content2 = zip(
                    [op.join("v2", file_name) for file_name in files2], cont2)

                data = self._processDirectories(tmp_dir,
                                                [("v1", dir_content1),
                                                 ("v2", dir_content2)])

                self.assertNotEqual(data[0], "")
                if cont1 == cont2:
                    self.assertEqual(data[1], "")
                else:
                    self.assertNotEqual(data[1], "")
