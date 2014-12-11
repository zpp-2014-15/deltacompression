"""
Module contains class needed for adding and compressing data from single files.
"""

from deltacompression.chunker_adapter import chunker


class FileProcessor(object):
    """Class responsible for adding and compressing data from single files."""

    def __init__(self, data_updater, min_chunk, max_chunk):
        """Creates FileProcessor object.

        Args:
            data_updater: instance of DataUpdater.
            min_chunk: minimal chunk's size.
            max_chunk: maximal chunk's size.
        Raises:
            ChunkerException, if the needed adapter binary is not present.
        """
        self._chunker = chunker.Chunker(min_chunk, max_chunk)
        self._data_updater = data_updater

    def setDataUpdater(self, data_updater):
        self._data_updater = data_updater

    def processFiles(self, files):
        """Processes a list of files.

        Args:
            files: paths to the files to be processed.
        Returns:
            data representing given files.
        Raises:
            ChunkerException in case of errors during communication.
            OSError
            IOError
        """
        data = []
        for chunk in self._chunker.chunkData(files):
            update = self._data_updater.update(chunk)
            if update:
                data.append(update.serialize())

        return "".join(data)
