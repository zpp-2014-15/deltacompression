"""Tests for versions_processor.py"""

import os.path as op
import unittest

import mock
import testfixtures

from deltacompression.backend import versions_processor
from deltacompression.backend import directory_processor


class VersionsProcessorTest(unittest.TestCase):
    """Test for class VersionsProcessor."""

    def setUp(self):
        self._dir_mock = \
            mock.create_autospec(directory_processor.DirectoryProcessor) \
                .return_value
        self._versions_processor = versions_processor.VersionsProcessor(
            self._dir_mock)

    def _testRunSimulation(self, dirs):
        with testfixtures.TempDirectory() as tmp_dir:
            for dir_name in dirs:
                tmp_dir.makedir(dir_name)

            ret = list(self._versions_processor.runSimulation(tmp_dir.path))
            processed_versions = [op.basename(path) for path, _ in ret]
            self.assertEqual(processed_versions, dirs)

            args = self._dir_mock.processDirectory.call_args_list
            passed_paths = [args[x][0][0] for x in xrange(len(args))]
            expected_paths = [op.join(tmp_dir.path, dir_name)
                              for dir_name in dirs]
            self.assertEqual(passed_paths, expected_paths)

    def testNoVersion(self):
        self._testRunSimulation([])

    def testOneVersion(self):
        self._testRunSimulation(["v1"])

    def testTwoVersions(self):
        self._testRunSimulation(["v1", "v2"])

    def testManyVersions(self):
        self._testRunSimulation(["v" + str(i) for i in xrange(10)])
