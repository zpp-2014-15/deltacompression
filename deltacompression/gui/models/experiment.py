"""Contains experiment and experiment result classes."""

from wx.lib import pubsub

from deltacompression.backend import file_processor


class Experiment(object):

    ALGORITHM_CHANGED = "experiment.algorithm.changed"
    CHUNKS_CHANGED = "experiment.chunks.changed"
    COMPRESSION_CHANGED = "experiment.compression.changed"
    FILES_CHANGED = "experiment.files.changed"

    def __init__(self):
        self._algorithm = None
        self._compression = None
        self._file_list = []
        self._min_chunk = 1024
        self._max_chunk = 10240

    def setChunkSizeRange(self, min_chunk, max_chunk):
        self._min_chunk = min_chunk
        self._max_chunk = max_chunk
        pubsub.Publisher.sendMessage(self.CHUNKS_CHANGED, self._algorithm)

    def setAlgorithm(self, algorithm):
        self._algorithm = algorithm
        pubsub.Publisher.sendMessage(self.ALGORITHM_CHANGED, self._algorithm)

    def getAlgorithm(self):
        return self._algorithm

    def setCompression(self, compression):
        self._compression = compression
        pubsub.Publisher.sendMessage(self.COMPRESSION_CHANGED, self._compression)

    def getCompression(self):
        return self._compression

    def addFileToList(self, file_name):
        self._file_list.append(file_name)
        pubsub.Publisher.sendMessage(self.FILES_CHANGED, self._file_list)

    def removeFileFromList(self, file_name):
        self._file_list.append.remove(file_name)
        pubsub.Publisher.sendMessage(self.FILES_CHANGED, self._file_list)

    def clearFileList(self):
        self._file_list = []
        pubsub.Publisher.sendMessage(self.FILES_CHANGED, self._file_list)

    def runExperiment(self):
        file_proc = file_processor.FileProcessor(self._algorithm,
                                                      self._compression,
                                                      self._min_chunk,
                                                      self._max_chunk)
        result = ExperimentResult(self._algorithm.getName(),
                                  self._compression.getName(),
                                  self._min_chunk, self._max_chunk)

        for file_name in self._file_list:
            returned_data = file_proc.processFile(file_name)
            result.addResult(file_name, len(returned_data))

        return result


class ExperimentResult(object):

    EXPERIMENT_RESULT_CHANGED = "experiment.result.changed"

    algorithm_name = None
    compression_name = None
    min_chunk = None
    max_chunk = None

    files_with_results = []

    def __init__(self, algorithm, compression, min_chunk, max_chunk):
        self.algorithm_name = algorithm
        self.compression = compression
        self.min_chunk = min_chunk
        self.max_chunk = max_chunk

    def addResult(self, file_name, data_to_send):
        self.files_with_results.append((file_name, data_to_send))
