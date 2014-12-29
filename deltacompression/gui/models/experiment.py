"""Contains experiment and experiment result classes."""

from deltacompression.backend import algorithm_factory
from deltacompression.backend import compression_factory
from deltacompression.chunker_adapter import chunker


class Experiment(object):
    """Holds information about entire simulation.

    Attributes:
        algorithm_factory: Factory that holds all algorithms
        compression_factory: Factory that holds all compressions
        def_alg: Default delta compression algorithm's name
        def_compr: Default compression's name
    """

    algorithm_factory = None
    compression_factory = None
    def_alg = ""
    def_compr = ""

    def __init__(self):
        self._tests_list = []
        self._chunker_params = chunker.ChunkerParameters(1024 * 32, 1024 * 96,
                                                         1024 * 64)

        self.algorithm_factory = algorithm_factory.AlgorithmFactory()
        self.def_alg = self.algorithm_factory.DUMMY_ALGORITHM

        self.compression_factory = compression_factory.CompressionFactory()
        self.def_compr = self.compression_factory.DUMMY_COMPRESSION

    def setChunkerParams(self, chunker_params):
        self._chunker_params = chunker_params

    def getChunkerParams(self):
        return self._chunker_params

    def getTest(self, index):
        return self._tests_list[index]

    def addTestToList(self, test):
        self._tests_list.append(test)

    def removeTestFromList(self, test_nr):
        self._tests_list.pop(test_nr)

    def runExperiment(self):
        for test in self._tests_list:
            yield test.runTest()
