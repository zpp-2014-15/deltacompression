"""
Module contains class needed for adding and compressing data from directory.
"""

from deltacompression.backend import utils


class VersionsProcessor(object):

    def __init__(self, directory_processor):
        self._directory_processor = directory_processor

    def setDirectoryProcessor(self, directory_processor):
        self._directory_processor = directory_processor

    def runSimulation(self, directory):
        """Processes directory with versions as subdirectories.

        Args:
            directory: directory with versions.
        Returns:
            pairs (version directory, compressed data representing the version)
        Raises:
            ChunkerException in case of errors during communication.
            OSError
            IOError
        """
        all_dirs = utils.getAllDirectories(directory)

        for version_dir in all_dirs:
            yield (version_dir, self._directory_processor.processDirectory(
                version_dir))
