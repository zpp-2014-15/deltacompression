class ExperimentResult(object):
    """This is result of one experiment.

    Attributes:
        versions_with_results: list of pairs like (version_dir_name, integer).
        algorithm_name: name of used algorithm.
        compression_name: name of used compression.
        min_chunk: minimal size of chunk.
        max_chunk: maximal size of chunk.
    """

    def __init__(self, dir_name, algorithm, compression, chunker_params):
        self.dir_name = dir_name
        self.algorithm_name = algorithm
        self.compression_name = compression
        self.min_chunk = chunker_params.getMinChunk()
        self.max_chunk = chunker_params.getMaxChunk()
        self.avg_chunk = chunker_params.getAvgChunk()
        self.versions_with_results = []

    def getAlgorithmName(self):
        return self.algorithm_name

    def getCompressionName(self):
        return self.compression_name

    def getDirName(self):
        return self.dir_name

    def addVersionResult(self, dir_name, data_to_send):
        self.versions_with_results.append((dir_name, data_to_send))


class ExperimentResultSet(object):
    
    def __init__(self):
        self._result_list = []
