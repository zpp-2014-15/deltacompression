"""Contains experiment and experiment result classes."""

from deltacompression.backend import algorithm_factory
from deltacompression.backend import compression_factory
from deltacompression.backend import file_processor


class Experiment(object):
    """Hold information necessary to perform simulation.

    Attributes:
        algorithm_factory: Factory that holds all algorithms.
    """

    algorithm_factory = None
    compression_factory = None

    def __init__(self):
        self._algorithm_name = "None"
        self._compression_name = "None"
        # TODO: remove this when compression factory implemented
        self._file_list = []
        self._min_chunk = 1024 * 32
        self._max_chunk = 1024 * 64

        self.algorithm_factory = algorithm_factory.AlgorithmFactory()
        self.compression_factory = compression_factory.CompressionFactory()

    def setChunkSizeRange(self, min_chunk, max_chunk):
        self._min_chunk = min_chunk
        self._max_chunk = max_chunk

    def getChunkSizeRange(self):
        return (self._min_chunk, self._max_chunk)

    def setAlgorithmName(self, algorithm_name):
        self._algorithm_name = algorithm_name

    def getAlgorithmName(self):
        return self._algorithm_name

    def setCompressionName(self, compression_name):
        self._compression_name = compression_name

    def getCompressionName(self):
        return self._compression_name

    def addFileToList(self, file_name):
        self._file_list.append(file_name)

    def removeFileFromList(self, file_name):
        self._file_list.remove(file_name)

    def clearFileList(self):
        self._file_list = []

    def getFileList(self):
        return self._file_list

    def runExperiment(self):
        """Runs experiment.

        Returns:
            instance of ExperimentResult.
        """
        algorithm = self.algorithm_factory.getAlgorithmFromName(
            self._algorithm_name)
        # TODO: use compression from compression factory
        compression = self.compression_factory.getCompressionFromName(
            self._compression_name)
        file_proc = file_processor.FileProcessor(algorithm, compression,
                                                 self._min_chunk,
                                                 self._max_chunk)
        result = ExperimentResult(self._algorithm_name,
                                  self._compression_name,
                                  self._min_chunk, self._max_chunk)

        print self._file_list
        for file_name in self._file_list:
            returned_data = file_proc.processFile(file_name)
            result.addResult(file_name, len(returned_data))

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

    files_with_results = None

    def __init__(self, algorithm, compression, min_chunk, max_chunk):
        self.algorithm_name = algorithm
        self.compression_name = compression
        self.min_chunk = min_chunk
        self.max_chunk = max_chunk
        self.files_with_results = []

    def addResult(self, file_name, data_to_send):
        self.files_with_results.append((file_name, data_to_send))
