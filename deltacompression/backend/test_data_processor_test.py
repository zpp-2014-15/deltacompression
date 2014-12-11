"""Tests for directory_processor.py"""

import os.path as op
import itertools
import unittest

import testfixtures

from deltacompression.backend import directory_processor
from deltacompression.backend import test_data_processor
from deltacompression.backend import data_updater
from deltacompression.backend import storage
from deltacompression.backend import chunk_hash
from deltacompression.backend import compression_algorithm
from deltacompression.backend import test_utils


class TestDataProcessorTest(unittest.TestCase):
    """Test for class TestDataProcessor."""

    def __init__(self, *args, **kwargs):
        super(TestDataProcessorTest, self).__init__(*args, **kwargs)
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
        storage_instance = storage.Storage(chunk_hash.HashSHA256(), None)
        data_updater_instance = data_updater.DummyUpdater(storage_instance)
        compression_algorithm_instance = compression_algorithm \
            .DummyCompressionAlgorithm()
        self._directory_processor = directory_processor.DirectoryProcessor(
            data_updater_instance, compression_algorithm_instance, 1000, 7000)
        self._test_data_processor = test_data_processor.TestDataProcessor(
            self._directory_processor)

    def testNoVersion(self):
        with testfixtures.TempDirectory() as tmp_dir:
            dir_content = []

            test_utils.fillTempDirectoryWithContent(tmp_dir.path, dir_content)
            data = list(self._test_data_processor.runSimulation(tmp_dir.path))
            self.assertEqual(len(data), 0)

    def testOneVersion(self):
        with testfixtures.TempDirectory() as tmp_dir:
            dir_content = zip(
                [op.join("v1", file_path) for file_path in self._files[0]],
                self._contents[0])

            test_utils.fillTempDirectoryWithContent(tmp_dir, dir_content)
            data = list(self._test_data_processor.runSimulation(tmp_dir.path))

            self.assertEqual(len(data), 1)
            self.assertEqual(data[0][0], op.join(tmp_dir.path, "v1"))
            self.assertNotEqual(data[0][1], "")

    def testTwoVersions(self):
        combinations = itertools.product(self._contents, self._contents,
                                         self._files, self._files)
        for cont1, cont2, files1, files2 in combinations:
            self.setUp()
            with testfixtures.TempDirectory() as tmp_dir:
                dir_content1 = zip(
                    [op.join("v1", file_path) for file_path in files1], cont1)
                dir_content2 = zip(
                    [op.join("v2", file_path) for file_path in files2], cont2)

                test_utils.fillTempDirectoryWithContent(
                    tmp_dir, dir_content1 + dir_content2)

                data = list(self._test_data_processor.runSimulation(
                    tmp_dir.path))

                self.assertEqual(len(data), 2)
                self.assertEqual(data[0][0], op.join(tmp_dir.path, "v1"))
                self.assertNotEqual(data[0][1], "")
                self.assertEqual(data[1][0], op.join(tmp_dir.path, "v2"))
                if cont1 == cont2:
                    self.assertEqual(data[1][1], "")
                else:
                    self.assertNotEqual(data[1][1], "")

    # def testLinux(self):
    #     path = "/home/pkura/code/zpp/test"
    #     data_sizes = []
    #     for version_dir, data in \
    #             self._test_data_processor.runSimulation(path):
    #         data_sizes.append(len(data))
    #     self.assertEqual(data_sizes, [539742497, 4119514])
