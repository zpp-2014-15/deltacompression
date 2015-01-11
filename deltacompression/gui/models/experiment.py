"""Contains experiment class."""

from deltacompression.backend import file_processor
from deltacompression.backend import directory_processor
from deltacompression.backend import versions_processor
from deltacompression.gui.models import experiment_result


class Experiment(object):
    """Holds information about a single experiment (a single test case)."""

    def __init__(self, experiment_queue, dir_name, alg_name, compr_name):
        self._experiment_queue = experiment_queue
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

    def run(self):
        """Runs the experiment.

        Returns:
            instance of ExperimentResult.
        """
        algorithm = self._experiment_queue.algorithm_factory. \
            getAlgorithmFromName(self._algorithm_name)
        compression = self._experiment_queue.compression_factory. \
            getCompressionFromName(self._compression_name)

        file_proc = file_processor.FileProcessor(
            algorithm, self._experiment_queue.getChunkerParameters())
        dir_proc = directory_processor.DirectoryProcessor(file_proc,
                                                          compression)
        versions_proc = versions_processor.VersionsProcessor(dir_proc)

        result = experiment_result.ExperimentResult(
            self._dir_name, self._algorithm_name, self._compression_name,
            self._experiment_queue.getChunkerParameters())

        simulation_data = list(versions_proc.runSimulation(self._dir_name))
        for version_dir, data in simulation_data:
            result.addVersionResult(version_dir, len(data))

        return result
