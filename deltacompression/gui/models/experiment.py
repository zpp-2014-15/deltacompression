"""Contains experiment and experiment result classes."""

from deltacompression.backend import algorithm_factory
from deltacompression.backend import compression_factory
from deltacompression.backend import file_processor
from deltacompression.backend import directory_processor
from deltacompression.backend import versions_processor
from deltacompression.chunker_adapter import chunker


class Experiment(object):
    """Holds information about a single experiment.

    Attributes:
        algorithm_factory: Factory that holds all algorithms.
        compression_factory: Factory that holds all compressions.
        def_alg: Default delta compression algorithm's name.
        def_compr: Default compression's name.
    """

    algorithm_factory = algorithm_factory.AlgorithmFactory()
    compression_factory = compression_factory.CompressionFactory()

    def_alg = algorithm_factory.DUMMY_ALGORITHM
    def_compr = compression_factory.DUMMY_COMPRESSION

    def __init__(self, dir_name, alg_name=def_alg, compr_name=def_compr):
        """Creates Experiment object.

        Args:
            dir_name: path to the directory with versions
            alg_name: name of the algorithm from AlgorithmFactory
            compr_name: name of the compression from CompressionFactory
        """
        self._chunker_params = chunker.ChunkerParameters(1024 * 32, 1024 * 96,
                                                         1024 * 64)
        self._dir_name = dir_name
        self._algorithm_name = alg_name
        self._compression_name = compr_name

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

    def getDirName(self):
        return self._dir_name

    def run(self):
        """Runs the experiment.

        Returns:
            instance of ExperimentResult.
        """
        algorithm = self.algorithm_factory. \
            getAlgorithmFromName(self._algorithm_name)
        compression = self.compression_factory. \
            getCompressionFromName(self._compression_name)

        file_proc = file_processor.FileProcessor(
            algorithm, self.getChunkerParameters())
        dir_proc = directory_processor.DirectoryProcessor(file_proc,
                                                          compression)
        versions_proc = versions_processor.VersionsProcessor(dir_proc)

        versions_with_results = []
        simulation_data = versions_proc.runSimulation(self._dir_name)
        for version_dir, data in simulation_data:
            versions_with_results.append((version_dir, len(data)))

        result = ExperimentResult(self._dir_name, self._algorithm_name,
                                  self._compression_name,
                                  self.getChunkerParameters(),
                                  versions_with_results)
        return result


class ExperimentResult(object):
    """This is result of one experiment."""

    def __init__(self, dir_name, algorithm, compression, chunker_params,
                 version_results):
        """Creates ExperimentResult object.

        Args:
            dir_name, algorithm, compression, chunker_params:
            same meaning as in Experiment class
            version_results: list of pairs like (version_dir_name, integer)
        """
        self.dir_name = dir_name
        self.algorithm_name = algorithm
        self.compression_name = compression
        self.min_chunk = chunker_params.getMinChunk()
        self.max_chunk = chunker_params.getMaxChunk()
        self.avg_chunk = chunker_params.getAvgChunk()
        self.versions_with_results = version_results

    def getAlgorithmName(self):
        return self.algorithm_name

    def getCompressionName(self):
        return self.compression_name

    def getDirName(self):
        return self.dir_name

    def printData(self):
        """Temporary method, to print out some info."""
        print self.dir_name
        print self.algorithm_name
        print self.compression_name
        print self.min_chunk
        print self.max_chunk
        print self.avg_chunk
        print self.versions_with_results
