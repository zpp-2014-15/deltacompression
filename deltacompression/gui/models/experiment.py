"""Contains experiment and experiment result classes."""

from deltacompression.backend import algorithm_factory
from deltacompression.backend import compression_factory
from deltacompression.backend import file_processor
from deltacompression.backend import directory_processor
from deltacompression.backend import versions_processor
from deltacompression.backend import utils
from deltacompression.chunker_adapter import chunker


class Experiment(object):
    """Holds information necessary to perform simulation.

    Attributes:
        algorithm_factory: Factory that holds all algorithms.
        compression_factory: Factory that holds all compressions
    """

    algorithm_factory = None
    compression_factory = None

    def __init__(self):
        self._algorithm_name = "None"
        self._compression_name = "None"
        self._versions_dir = ""
        self._chunker_params = chunker.ChunkerParameters(1024 * 32, 1024 * 96,
                                                         1024 * 64)

        self.algorithm_factory = algorithm_factory.AlgorithmFactory()
        self.compression_factory = compression_factory.CompressionFactory()

    def setChunkerParameters(self, chunker_params):
        self._chunker_params = chunker_params

    def getChunkerParameters(self):
        return self._chunker_params

    def setAlgorithmName(self, algorithm_name):
        self._algorithm_name = algorithm_name

    def getAlgorithmName(self):
        return self._algorithm_name

    def setCompressionName(self, compression_name):
        self._compression_name = compression_name

    def getCompressionName(self):
        return self._compression_name

    def setVersionsDir(self, versions_dir):
        self._versions_dir = versions_dir

    def clearVersionsDir(self):
        self._versions_dir = ""

    def getVersionsList(self):
        try:
            return utils.getAllDirectories(self._versions_dir)
        except OSError:
            return []


    def runExperiment(self):
        """Runs experiment.

        Returns:
            instance of ExperimentResult.
        """
        algorithm = self.algorithm_factory.getAlgorithmFromName(
            self._algorithm_name)

        compression = self.compression_factory.getCompressionFromName(
            self._compression_name)

        file_proc = file_processor.FileProcessor(algorithm,
                                                 self._chunker_params)
        dir_proc = directory_processor.DirectoryProcessor(file_proc,
                                                          compression)
        versions_proc = versions_processor.VersionsProcessor(dir_proc)

        result = ExperimentResult(self._algorithm_name,
                                  self._compression_name,
                                  self._chunker_params)

        returned_data = list(versions_proc.runSimulation(self._versions_dir))
        for version_dir, data in returned_data:
            result.addResult(version_dir, len(data))

        return result


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
