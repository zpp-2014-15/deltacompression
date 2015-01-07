"""Contains experiment and experiment set classes."""

from deltacompression.backend import algorithm_factory
from deltacompression.backend import compression_factory
from deltacompression.backend import file_processor
from deltacompression.backend import directory_processor
from deltacompression.backend import versions_processor
from deltacompression.chunker_adapter import chunker
from deltacompression.gui.models import experiment_result


class Experiment(object):
    """Holds information about a single test case."""

    def __init__(self, experiment_set, dir_name, alg_name, compr_name):
        self._experiment_set = experiment_set
        self._dir_name = dir_name
        self._algorithm_name = alg_name
        self._compression_name = compr_name

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

    def runExperiment(self):
        """Runs the test.

        Returns:
            instance of TestResult.
        """
        algorithm = self._experiment_set.algorithm_factory. \
            getAlgorithmFromName(self._algorithm_name)
        compression = self._experiment_set.compression_factory. \
            getCompressionFromName(self._compression_name)

        file_proc = file_processor.FileProcessor(
            algorithm, self._experiment_set.getChunkerParameters())
        dir_proc = directory_processor.DirectoryProcessor(file_proc,
                                                          compression)
        versions_proc = versions_processor.VersionsProcessor(dir_proc)

        result = experiment_result.ExperimentResult(self._dir_name,
            self._algorithm_name, self._compression_name,
            self._experiment_set.getChunkerParameters())

        simulation_data = list(versions_proc.runSimulation(self._dir_name))
        for version_dir, data in simulation_data:
            result.addVersionResult(version_dir, len(data))

        return result


class ExperimentSet(object):
    """Holds information about entire simulation
       (set of experiments to be performed)

    Attributes:
        algorithm_factory: Factory that holds all algorithms.
        compression_factory: Factory that holds all compressions.
        def_alg: Default delta compression algorithm's name.
        def_compr: Default compression's name.
    """

    algorithm_factory = None
    compression_factory = None
    def_alg = ""
    def_compr = ""

    def __init__(self):
        self._experiments_list = []
        self._chunker_params = chunker.ChunkerParameters(1024 * 32, 1024 * 96,
                                                         1024 * 64)

        self.algorithm_factory = algorithm_factory.AlgorithmFactory()
        self.def_alg = self.algorithm_factory.DUMMY_ALGORITHM

        self.compression_factory = compression_factory.CompressionFactory()
        self.def_compr = self.compression_factory.DUMMY_COMPRESSION

        self._controller = None

    def setChunkerParameters(self, chunker_params):
        self._chunker_params = chunker_params

    def getChunkerParameters(self):
        return self._chunker_params

    def setController(self, controller):
        self._controller = controller
    
    def addExperimentToList(self, test):
        self._experiments_list.append(test)

    def removeExperimentFromList(self, test):
        self._experiments_list.remove(test)

    def getExperimentsList(self):
        return self._experiments_list

    def runExperiments(self):
        result_list = []
        for experiment in self._experiments_list[:]:
            exp_result = experiment.runExperiment()
            result_list.append(exp_result)
            self.removeExperimentFromList(experiment)
            self._controller.onExperimentPerformed(exp_result)
        return result_list
