"""Contains test and test result classes"""

class Test(object):
    """Holds information about a single test case"""
    
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
        algorithm = self._experiment.algorithm_factory.getAlgorithmFromName(self._algorithm_name)
        compression = self._experiment.compression_factory.getCompressionFromName(self._compression_name)

        file_proc = file_processor.FileProcessor(
            algorithm, self._experiment.getChunkerParams())
        dir_proc = directory_processor.DirectoryProcessor(file_proc,
                                                          compression)
        versions_proc = versions_processor.VersionsProcessor(dir_proc)

        result = ExperimentResult(self._algorithm_name,
                                  self._compression_name,
                                  self._experiment.getChunkerParams())
