"""Contains test and test result classes"""

from deltacompression.backend import file_processor
from deltacompression.backend import directory_processor
from deltacompression.backend import versions_processor

class Test(object):
    """Holds information about a single test case."""

    def __init__(self, dir_name, experiment):
        self._dir_name = dir_name
        self._experiment = experiment
        self._algorithm_name = experiment.def_alg
        self._compression_name = experiment.def_compr

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

    def runTest(self):
        """Runs the test.

        Returns:
            instance of TestResult.
        """
        algorithm = self._experiment.algorithm_factory.getAlgorithmFromName(
            self._algorithm_name)
        compression = self._experiment.compression_factory. \
            getCompressionFromName(self._compression_name)

        file_proc = file_processor.FileProcessor(
            algorithm, self._experiment.getChunkerParams())
        dir_proc = directory_processor.DirectoryProcessor(file_proc,
                                                          compression)
        versions_proc = versions_processor.VersionsProcessor(dir_proc)

        result = TestResult(self._algorithm_name,
                            self._compression_name,
                            self._experiment.getChunkerParams())

        returned_data = list(versions_proc.runSimulation(self._dir_name))
        for version_dir, data in returned_data:
            result.addResult(version_dir, len(data))

        return result


class TestResult(object):
    """This is result of one test.

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

    versions_with_results = None

    def __init__(self, algorithm, compression, chunker_params):
        self.algorithm_name = algorithm
        self.compression_name = compression
        self.min_chunk = chunker_params.getMinChunk()
        self.max_chunk = chunker_params.getMaxChunk()
        self.avg_chunk = chunker_params.getAvgChunk()
        self.versions_with_results = []

    def addResult(self, dir_name, data_to_send):
        self.versions_with_results.append((dir_name, data_to_send))
