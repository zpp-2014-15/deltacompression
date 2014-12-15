"""Tests for versions_processor.py"""

import os.path as op
import unittest

import mock
import testfixtures

from deltacompression.backend import versions_processor
from deltacompression.backend import test_utils


class VersionsProcessorTest(unittest.TestCase):
    """Test for class VersionsProcessor."""

    EXAMPLE_CONTENTS = [""] * 4

    EXAMPLE_FILES = ["1.txt",
                     "A/2.pdf",
                     "A/B/3",
                     "C/D/E/4.avi"
                    ]

    def setUp(self):
        self._patcher = mock.patch("deltacompression.backend."
                                   "directory_processor.DirectoryProcessor",
                                   autospec=True)
        self.addCleanup(self._patcher.stop)
        self._mock = self._patcher.start()
        self._dir_mock = self._mock.return_value
        self._versions_processor = versions_processor.VersionsProcessor(
            self._dir_mock)

    def _testRunSimulation(self, dirs_content):
        with testfixtures.TempDirectory() as tmp_dir:
            for dir_name, dir_content in dirs_content:
                files = [(op.join(dir_name, file_name), content)
                         for file_name, content in dir_content]
                test_utils.fillTempDirectoryWithContent(tmp_dir, files)

            ret = list(self._versions_processor.runSimulation(tmp_dir.path))
            processed_versions = [op.basename(path) for path, _ in ret]
            expected_versions = [dir_name for dir_name, _ in dirs_content]
            self.assertEqual(processed_versions, expected_versions)

            args = self._dir_mock.processDirectory.call_args_list
            passed_paths = [args[x][0][0] for x in xrange(len(args))]
            expected_paths = [op.join(tmp_dir.path, dir_name)
                              for dir_name, _ in dirs_content]
            self.assertEqual(passed_paths, expected_paths)

    def testNoVersion(self):
        self._testRunSimulation([])

    def testOneVersion(self):

        self._testRunSimulation([("v1", zip(self.EXAMPLE_FILES,
                                            self.EXAMPLE_CONTENTS))])

    def testTwoVersions(self):
        self._testRunSimulation([("v1", zip(self.EXAMPLE_FILES,
                                            self.EXAMPLE_CONTENTS)),
                                 ("v2", zip(self.EXAMPLE_FILES,
                                            self.EXAMPLE_CONTENTS))])

    def testManyVersions(self):
        dir_contents = []
        for i in xrange(10):
            dir_contents.append(("v" + str(i),
                                 zip(self.EXAMPLE_FILES,
                                     self.EXAMPLE_CONTENTS)))
        self._testRunSimulation(dir_contents)
