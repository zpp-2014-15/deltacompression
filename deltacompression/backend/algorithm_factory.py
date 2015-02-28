"""This module is responsible for creating algorithms."""

from deltacompression.backend import chunk_hash
from deltacompression.backend import data_updater
from deltacompression.backend import diff
from deltacompression.backend import storage


class AlgorithmFactory(object):

    DUMMY_ALGORITHM = "No delta encoding"
    OPTIMAL_ALGORITHM = "Optimal delta encoding"
    SIMILARITY_INDEX_ALGORITHM = "Similarity index delta encoding"

    ALL_ALGORITHMS = [
        DUMMY_ALGORITHM,
        OPTIMAL_ALGORITHM,
        SIMILARITY_INDEX_ALGORITHM
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
        elif name == self.SIMILARITY_INDEX_ALGORITHM:
            diff_inst = diff.XDelta3Diff()
            par = data_updater.SimilarityIndexParams()
            par.fmod = 2 ** 20
            # TODO it should be more flexible
            par.ssize = 4
            par.win = 16
            par.qmod = 982451653
            par.prim = 613651369
            par.pis = [(32452867, 633910099),
                       (512927377, 49979687),
                       (413158523, 879190841),
                       (472882027, 899809363),
                       (15485867, 817504243),
                       (334214467, 179424673),
                       (838041647, 353868019),
                       (756065179, 533000389)]
            return data_updater.SimilarityIndexDeltaUpdater(storage_instance,
                                                            diff_inst,
                                                            par)
