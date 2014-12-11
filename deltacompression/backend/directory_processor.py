"""
Module contains class needed for adding and compressing data from directory.
"""

import os

from deltacompression.backend import file_processor


class DirectoryProcessor(object):
    """Class responsible for adding and compressing data from files inside
    a single directory."""

    def __init__(self, data_updater, compression_algorithm, min_chunk,
                 max_chunk):
        """Creates DirectoryProcessor object.

        Args:
            data_updater: instance of DataUpdater.
            compression_algorithm: instance of CompressionAlgorithm.
            min_chunk: minimal chunk's size.
            max_chunk: maximal chunk's size.
        Raises:
            ChunkerException, if the needed adapter binary is not present.
        """
        self._compression_algorithm = compression_algorithm
        self._file_processor = file_processor.FileProcessor(
            data_updater, min_chunk, max_chunk)

    def setDataUpdater(self, data_updater):
        self._file_processor.setDataUpdater(data_updater)

    def setCompressionAlgorithm(self, compression_algorithm):
        self._compression_algorithm = compression_algorithm

    def processDirectory(self, directory):
        """Processes all files in given directory.

        Args:
            directory: directory with files.
        Returns:
            compressed data representing given directory.
        Raises:
            ChunkerException in case of errors during communication.
            OSError
            IOError
        """
        all_files = []
        for dir_name, _, files in os.walk(directory):
            for file_name in files:
                file_path = os.path.join(dir_name, file_name)
                all_files.append(file_path)

        data = self._file_processor.processFiles(all_files)
        return self._compression_algorithm.compress(data)
