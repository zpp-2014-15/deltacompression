"""Tests for directory_processor.py"""

import os
import os.path as op
import shutil

import unittest

from deltacompression.backend import directory_processor
from deltacompression.backend import data_updater
from deltacompression.backend import storage
from deltacompression.backend import chunk_hash
from deltacompression.backend import compression_algorithm


class DirectoryProcessorTest(unittest.TestCase):
    """Test for class DirectoryProcessor."""

    test_dir_name = op.join(op.abspath(op.dirname(__file__)), "__test_dir__")

    def setUp(self):
        _storage = storage.Storage(chunk_hash.HashSHA256(), None)
        _data_updater = data_updater.DummyUpdater(_storage)
        _compression_algorithm = compression_algorithm \
            .DummyCompressionAlgorithm()
        self._directory_processor = directory_processor.DirectoryProcessor(
            _data_updater, _compression_algorithm, 1000, 7000)

        if op.exists(self.test_dir_name):
            shutil.rmtree(self.test_dir_name)

        os.makedirs(self.test_dir_name)

    def tearDown(self):
        if op.exists(self.test_dir_name):
            shutil.rmtree(self.test_dir_name)

    def _createDirectory(self, dir_name, files):
        """Creates directory with subdirectories and files.
        Args:
            files: a list of pairs (file_name, file_content)
        """

        if not op.exists(self.test_dir_name):
            os.makedirs(self.test_dir_name)

        dir_full_name = op.join(self.test_dir_name, dir_name)

        if op.exists(dir_full_name):
            shutil.rmtree(dir_full_name)

        os.makedirs(dir_full_name)

        for name, content in files:
            file_name = op.join(dir_full_name, name)
            file_dir_name = op.dirname(file_name)

            if not op.exists(file_dir_name):
                os.makedirs(file_dir_name)
            with open(file_name, "w") as tfile:
                tfile.write(content)

    def _processDirectories(self, dirs_content):
        """Creates directories with given content and then processes them.
        Args:
            dirs_content: a list of pairs (dir_path, dir_content),
                          where dir_content is a list of pairs
                          (file_name, file_content)
        Returns:
            a list of results for every directory.
        """

        data = []
        for dir_path, dir_content in dirs_content:
            self._createDirectory(dir_path, dir_content)
            full_path = op.join(self.test_dir_name, dir_path)
            data.append(self._directory_processor.processDirectory(full_path))

        return data


    def testTheSameDirectories(self):
        """Adding a directory which is a copy of the previously added directory
        should return empty string to send."""

        content = [",".join([str(i) for i in xrange(15000)]),
                   ",".join([str(i) for i in xrange(15000, 35000)]),
                   ",".join([str(i) for i in xrange(10000, 35000)]),
                   ",".join([
                       str(i) for i in xrange(20000, 45000)])]

        files = ["1.txt",
                 "A/2.pdf",
                 "A/B/3",
                 "C/D/E/4.avi"]

        dir_content = zip(files, content)

        data = self._processDirectories(zip(["v1", "v2"],
                                            [dir_content, dir_content]))

        self.assertNotEqual(data[0], "")
        self.assertEqual(data[1], "")

    def testTheSameContent(self):
        """Adding a directory with the same content as previously added
        directory but with different names of files should return empty string
        to send."""

        files1 = ["1.txt",
                  "A/2.pdf",
                  "A/B/3",
                  "C/D/E/4.avi"]

        files2 = ["Program Files/foo.ff",
                  "home/jack/.vimrc",
                  "qqqqqq",
                  "lorem/ipsum/dolor sit amet"]

        content = ["0" * 15000,
                   " ".join([str(i) for i in xrange(15000, 35000)]),
                   "abb".join([str(i) for i in xrange(1111, 33033)]),
                   ",".join([str(i) for i in xrange(20000, 45000)])]

        dir_content1 = zip(files1, content)
        dir_content2 = zip(files2, content)

        data = self._processDirectories([("v1", dir_content1),
                                         ("v2", dir_content2)])

        self.assertNotEqual(data[0], "")
        self.assertEqual(data[1], "")
