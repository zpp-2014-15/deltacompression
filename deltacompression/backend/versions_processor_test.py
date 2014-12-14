"""Tests for versions_processor.py"""

import os.path as op
import itertools
import unittest

import testfixtures

from deltacompression.backend import directory_processor
from deltacompression.backend import versions_processor
from deltacompression.backend import data_updater
from deltacompression.backend import storage
from deltacompression.backend import chunk_hash
from deltacompression.backend import compression_algorithm
from deltacompression.backend import test_utils


class VersionsProcessorTest(unittest.TestCase):
    """Test for class VersionsProcessor."""

    def setUp(self):
        storage_instance = storage.Storage(chunk_hash.HashSHA256(), None)
        data_updater_instance = data_updater.DummyUpdater(storage_instance)
        compression_algorithm_instance = compression_algorithm \
            .DummyCompressionAlgorithm()
        self._directory_processor = directory_processor.DirectoryProcessor(
            data_updater_instance, compression_algorithm_instance, 1000, 7000)
        self._version_processor = versions_processor.VersionsProcessor(
            self._directory_processor)

    def testNoVersion(self):
        with testfixtures.TempDirectory() as tmp_dir:
            dir_content = []

            test_utils.fillTempDirectoryWithContent(tmp_dir.path, dir_content)
            data = list(self._version_processor.runSimulation(tmp_dir.path))
            self.assertEqual(len(data), 0)

    def testOneVersion(self):
        with testfixtures.TempDirectory() as tmp_dir:
            dir_content = zip(
                [op.join("v1", file_path) for file_path in
                 test_utils.EXAMPLE_FILES[0]],
                test_utils.EXAMPLE_CONTENTS[0])

            test_utils.fillTempDirectoryWithContent(tmp_dir, dir_content)
            data = list(self._version_processor.runSimulation(tmp_dir.path))

            self.assertEqual(len(data), 1)
            self.assertEqual(data[0][0], op.join(tmp_dir.path, "v1"))
            self.assertNotEqual(data[0][1], "")

    def testTwoVersions(self):
        combinations = itertools.product(
            test_utils.EXAMPLE_CONTENTS, test_utils.EXAMPLE_CONTENTS,
            test_utils.EXAMPLE_FILES, test_utils.EXAMPLE_FILES)

        for cont1, cont2, files1, files2 in combinations:
            self.setUp()
            with testfixtures.TempDirectory() as tmp_dir:
                dir_content1 = zip(
                    [op.join("v1", file_path) for file_path in files1], cont1)
                dir_content2 = zip(
                    [op.join("v2", file_path) for file_path in files2], cont2)

                test_utils.fillTempDirectoryWithContent(
                    tmp_dir, dir_content1 + dir_content2)

                data = list(self._version_processor.runSimulation(
                    tmp_dir.path))

                self.assertEqual(len(data), 2)
                self.assertEqual(data[0][0], op.join(tmp_dir.path, "v1"))
                self.assertNotEqual(data[0][1], "")
                self.assertEqual(data[1][0], op.join(tmp_dir.path, "v2"))
                if cont1 == cont2:
                    self.assertEqual(data[1][1], "")
                else:
                    self.assertNotEqual(data[1][1], "")
