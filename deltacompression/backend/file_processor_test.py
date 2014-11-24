"""Tests for file_processor.py"""

import unittest

from deltacompression.backend import file_processor


class FileProcessorTest(unittest.TestCase):

    def setUp(self):
        self._file_processor = file_processor.FileProcessor()
