"""
Module contains class needed for adding and compressing data from directory.
"""

import os
import os.path as op


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
        all_files = [(op.join(directory, file_name), file_name)
                     for file_name in os.listdir(directory)]
        all_dirs = sorted((x, y) for (x, y) in all_files if op.isdir(x))
        logger = self._directory_processor.getLogger()

        for full_path, version_dir in all_dirs:
            if logger:
                before_blocks = logger.getTotalBlocks()
                before_dedups = logger.getDeduplications()

            processed = self._directory_processor.processDirectory(full_path)

            if logger:
                new_blocks = logger.getTotalBlocks() - before_blocks
                dedups = logger.getDeduplications() - before_dedups
                percent = "{0:.2f}%".format(float(dedups) * 100 /
                                            (dedups + new_blocks))
                yield (version_dir + " " + percent +
                       " deduplications", processed)
            else:
                yield (version_dir, processed)
