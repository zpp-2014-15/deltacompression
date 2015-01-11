"""Contains queue of experiments"""

from deltacompression.backend import algorithm_factory
from deltacompression.backend import compression_factory
from deltacompression.chunker_adapter import chunker


class ExperimentQueue(object):
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

    def addExperiment(self, experiment):
        raise NotImplementedError


class DummyExperimentQueue(ExperimentQueue):
    """Performs experiments synchronically."""

    def addExperiment(self, experiment):
        self.addExperimentToList(experiment)
        exp_result = experiment.run()
        self.removeExperimentFromList(experiment)
        self._controller.onExperimentPerformed(exp_result)
        return exp_result
