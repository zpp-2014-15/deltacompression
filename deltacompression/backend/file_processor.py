"""
Module contains class needed for adding and compressing data from single files.
"""

import cStringIO

from deltacompression.chunker_adapter import chunker


class FileProcessor(object):
    """Class responsible for adding and compressing data from single files."""

    def __init__(self, data_updater, chunker_params):
        """Creates FileProcessor object.

        Args:
            data_updater: instance of DataUpdater.
            chunker_params: instance of ChunkerParameters
        Raises:
            ChunkerException, if the needed adapter binary is not present.
        """
        self._chunker = chunker.Chunker(chunker_params)
        self._data_updater = data_updater

    def setDataUpdater(self, data_updater):
        self._data_updater = data_updater

    def getLogger(self):
        return self._data_updater.getLogger()

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
        buf = cStringIO.StringIO()
        for chunk in self._chunker.chunkData(files):
            update = self._data_updater.update(chunk)
            if update:
                buf.write(update.serialize())
        return buf.getvalue()
