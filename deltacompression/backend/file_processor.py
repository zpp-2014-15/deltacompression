"""
Module contains class needed for adding and compressing data from single files.
"""

from deltacompression.chunker_adapter import chunker


class FileProcessor(object):
    """Class responsible for adding and compressing data from single files."""

    def __init__(self, data_updater, compression, min_chunk,
                 max_chunk):
        """Creates FileProcessor object.

        Args:
            data_updater: instance of DataUpdater.
            compression: instance of Compression.
            min_chunk: minimal chunk's size.
            max_chunk: maximal chunk's size.
        Raises:
            ChunkerException, if the needed adapter binary is not present.
        """
        self._chunker = chunker.Chunker(min_chunk, max_chunk)
        self._data_updater = data_updater
        self._compression = compression

    def setDataUpdater(self, data_updater):
        self._data_updater = data_updater

    def setCompression(self, compression):
        self._compression = compression

    def processFile(self, file_name):
        """Processes a single file.

        Args:
            file_name: path to the file to be processed.
        Returns:
            compressed data representing given file.
        Raises:
            ChunkerException in case of errors during communication.
            OSError
            IOError
        """
        data = []
        for chunk in self._chunker.chunkData(file_name):
            update = self._data_updater.update(chunk)
            if update:
                data.append(update.serialize())

        return self._compression.compress("".join(data))
