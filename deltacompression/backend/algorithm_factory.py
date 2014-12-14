"""This module is responsible for creating algorithms."""

from deltacompression.backend import chunk_hash
from deltacompression.backend import data_updater
from deltacompression.backend import diff
from deltacompression.backend import storage


class AlgorithmFactory(object):

    DUMMY_ALGORITHM = "No delta compression"
    OPTIMAL_ALGORITHM = "Optimal delta compression"

    ALL_ALGORITHMS = [
        DUMMY_ALGORITHM,
        OPTIMAL_ALGORITHM
    ]

    def getAlgorithms(self):
        return self.ALL_ALGORITHMS

    def getAlgorithmFromName(self, name, storage_instance=None):
        if storage_instance is None:
            storage_instance = storage.Storage(chunk_hash.HashSHA256(), None)
        if name == self.DUMMY_ALGORITHM:
            return data_updater.DummyUpdater(storage_instance)
        elif name == self.OPTIMAL_ALGORITHM:
            diff_inst = diff.XDelta3Diff()
            return data_updater.OptimalDeltaUpdater(storage_instance, diff_inst)
