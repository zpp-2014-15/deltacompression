"""
Module contains class needed for adding and compressing data from single files.
"""

from deltacompression.chunker_adapter import chunker


class FileProcessor(object):
    """Class responsible for adding and compressing data from single files."""

    def __init__(self, data_updater, compression_algorithm, min_chunk,
                 max_chunk):
        self._chunker = chunker.Chunker(min_chunk, max_chunk)
        self._data_updater = data_updater
        self._compression_algorithm = compression_algorithm

    def setDataUpdater(self, data_updater):
        self._data_updater = data_updater

    def setCompressionAlgorithm(self, compression_algorithm):
        self._compression_algorithm = compression_algorithm

    def processFile(self, file_name):
        """Processes a single file.

        Args:
            file_name: path to the file to pe processed.
        Returns:
            compressed data representing given file
        """
        data = []
        for chunk in self._chunker.chunkData(file_name):
            data.append(self._data_updater.update(chunk))

        return self._compression_algorithm.compress(data)
