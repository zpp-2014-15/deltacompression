"""Tests for directory_processor.py"""

import itertools
import os
import os.path as op
import shutil
import unittest

from deltacompression.backend import directory_processor
from deltacompression.backend import data_updater
from deltacompression.backend import storage
from deltacompression.backend import chunk_hash
from deltacompression.backend import compression_algorithm
from deltacompression.backend import test_utils


class DirectoryProcessorTest(unittest.TestCase):
    """Test for class DirectoryProcessor."""

    def __init__(self, *args, **kwargs):
        super(DirectoryProcessorTest, self).__init__(*args, **kwargs)
        self._contents = [["0" * 15000,
                           " ".join([str(i) for i in xrange(15000, 35000)]),
                           "abb".join([str(i) for i in xrange(1111, 33033)]),
                           ",".join([str(i) for i in xrange(20000, 45000)])
                          ],
                          ["^%" * 15500,
                           "qq".join([str(i) for i in xrange(15000, 35000)]),
                           ";".join([str(i) for i in xrange(1111, 39033)]),
                           ",".join([str(i) for i in xrange(40000, 65000)])
                          ]
                         ]

        self._files = [["1.txt",
                        "A/2.pdf",
                        "A/B/3",
                        "C/D/E/4.avi"
                       ],
                       ["Program Files/foo.ff",
                        "home/jack/.vimrc",
                        "qqqqqq",
                        "lorem/ipsum/dolor sit amet"
                       ]
                      ]

    def setUp(self):
        _storage = storage.Storage(chunk_hash.HashSHA256(), None)
        _data_updater = data_updater.DummyUpdater(_storage)
        _compression_algorithm = compression_algorithm \
            .DummyCompressionAlgorithm()
        self._directory_processor = directory_processor.DirectoryProcessor(
            _data_updater, _compression_algorithm, 1000, 7000)

        if op.exists(test_utils.TEST_DIR_PATH):
            shutil.rmtree(test_utils.TEST_DIR_PATH)

        os.makedirs(test_utils.TEST_DIR_PATH)

    def tearDown(self):
        if op.exists(test_utils.TEST_DIR_PATH):
            shutil.rmtree(test_utils.TEST_DIR_PATH)

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
            test_utils.createDirectoryWithContent(dir_path, dir_content)
            full_path = op.join(test_utils.TEST_DIR_PATH, dir_path)
            data.append(self._directory_processor.processDirectory(full_path))

        return data

    def testProcessDirectory(self):
        combinations = itertools.product(self._contents, self._contents,
                                         self._files, self._files)

        for cont1, cont2, files1, files2 in combinations:
            self.setUp()
            dir_content1 = zip(files1, cont1)
            dir_content2 = zip(files2, cont2)

            data = self._processDirectories([("v1", dir_content1),
                                             ("v2", dir_content2)])

            self.assertNotEqual(data[0], "")
            if cont1 == cont2:
                self.assertEqual(data[1], "")
            else:
                self.assertNotEqual(data[1], "")
