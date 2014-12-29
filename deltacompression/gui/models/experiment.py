"""Contains experiment and experiment result classes."""

from deltacompression.backend import algorithm_factory
from deltacompression.backend import compression_factory
from deltacompression.backend import file_processor
from deltacompression.backend import directory_processor
from deltacompression.backend import versions_processor
from deltacompression.backend import utils
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

    def setChunkerParameters(self, chunker_params):
        self._chunker_params = chunker_params

    def getChunkerParameters(self):
        return self._chunker_params

    def getTest(self, index):
        return self._tests_list[index]

    def addTestToList(self, test):
        self._tests_list.append(test)

    def removeTestFromList(self, test_nr):
        self._tests_list.pop(test_nr)


class ExperimentResult(object):
    """This is result of one experiment.

    Attributes:
        files_with_results: list of pairs like (file, integer).
        algorithm_name: name of used algorithm.
        compression_name: name of used compression.
        min_chunk: minimal size of chunk.
        max_chunk: maximal size of chunk.
    """

    algorithm_name = None
    compression_name = None
    min_chunk = None
    max_chunk = None
    avg_chunk = None

    files_with_results = None

    def __init__(self, algorithm, compression, chunker_params):
        self.algorithm_name = algorithm
        self.compression_name = compression
        self.min_chunk = chunker_params.getMinChunk()
        self.max_chunk = chunker_params.getMaxChunk()
        self.avg_chunk = chunker_params.getAvgChunk()
        self.files_with_results = []

    def addResult(self, file_name, data_to_send):
        self.files_with_results.append((file_name, data_to_send))
