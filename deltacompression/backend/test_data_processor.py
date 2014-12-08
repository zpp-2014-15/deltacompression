"""
Module contains class needed for adding and compressing data from directory.
"""

import os
import os.path as op

#from deltacompression.backend import directory_processor


class TestDataProcessor(object):

    def __init__(self, directory_processor):
        self._directory_processor = directory_processor

    def setDirectoryProcessor(self, directory_processor):
        self._directory_processor = directory_processor

    def runSimulation(self, directory):
        all_files = map(lambda(x): op.join(directory, x), os.listdir(directory))
        all_dirs = sorted(filter(op.isdir, all_files))

        for version_dir in all_dirs:
            yield (version_dir, self._directory_processor.processDirectory(version_dir))