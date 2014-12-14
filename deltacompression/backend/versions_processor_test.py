# pylint: disable=E1120
# no-value-for-parameter - pylint doesn't know how mocks work

"""Tests for versions_processor.py"""

import os.path as op
import unittest

import mock
import testfixtures

from deltacompression.backend import directory_processor
from deltacompression.backend import versions_processor
from deltacompression.backend import data_updater
from deltacompression.backend import storage
from deltacompression.backend import chunk_hash
from deltacompression.backend import compression
from deltacompression.backend import test_utils


class VersionsProcessorTest(unittest.TestCase):
    """Test for class VersionsProcessor."""

    EXAMPLE_CONTENTS = ["0" * 10,
                        " " * 20,
                        "a" * 30,
                        "," * 40
                       ]

    EXAMPLE_FILES = ["1.txt",
                     "A/2.pdf",
                     "A/B/3",
                     "C/D/E/4.avi"
                    ]

    def setUp(self):
        storage_instance = storage.Storage(chunk_hash.HashSHA256(), None)
        data_updater_instance = data_updater.DummyUpdater(storage_instance)
        compression_algorithm_instance = compression.DummyCompression()
        self._directory_processor = directory_processor.DirectoryProcessor(
            data_updater_instance, compression_algorithm_instance, 1000, 7000)
        self._version_processor = versions_processor.VersionsProcessor(
            self._directory_processor)

    @mock.patch("deltacompression.backend.directory_processor"
                ".DirectoryProcessor",
                autospec=True)
    def _testRunSimulation(self, dirs_content, mock_directory_processor):
        self.setUp()
        with testfixtures.TempDirectory() as tmp_dir:
            for dir_name, dir_content in dirs_content:
                files = [(op.join(dir_name, file_name), content)
                         for file_name, content in dir_content]
                test_utils.fillTempDirectoryWithContent(tmp_dir, files)

            list(self._version_processor.runSimulation(tmp_dir.path))
            args = mock_directory_processor.return_value.processDirectory. \
                call_args_list
            processed_paths = set(args[x][0][0] for x in xrange(len(args)))
            expected_paths = set(op.join(tmp_dir.path, dir_name)
                                 for dir_name, _ in dirs_content)
            self.assertEqual(processed_paths, expected_paths)

    def testNoVersion2(self):
        self._testRunSimulation([])

    def testOneVersion2(self):

        self._testRunSimulation([("v1", zip(self.EXAMPLE_FILES,
                                            self.EXAMPLE_CONTENTS))])

    def testTwoVersions(self):
        self._testRunSimulation([("v1", zip(self.EXAMPLE_FILES,
                                            self.EXAMPLE_CONTENTS)),
                                 ("v2", zip(self.EXAMPLE_FILES,
                                            self.EXAMPLE_CONTENTS))])

    def testManyVersions(self):
        dir_contents = []
        for i in xrange(100):
            dir_contents.append(("v" + str(i),
                                 zip(self.EXAMPLE_FILES,
                                     self.EXAMPLE_CONTENTS)))
        self._testRunSimulation(dir_contents)
