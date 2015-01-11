"""Test for experiment.py"""

import unittest
import mock

from deltacompression.backend import directory_processor
from deltacompression.chunker_adapter import chunker
from deltacompression.gui.models import experiment
from deltacompression.gui.models import queue

class ExperimentTest(unittest.TestCase):
    """Tests of Test class"""

    def setUp(self):
        self._dir_name = "/home/me/test/"
        self._exp_queue = queue.ExperimentQueue()
        self._experiment = experiment.Experiment(self._exp_queue,
                                                 self._dir_name,
                                                 self._exp_queue.def_alg,
                                                 self._exp_queue.def_compr)

    @mock.patch("deltacompression.backend.algorithm_factory.AlgorithmFactory",
                autospec=True)
    @mock.patch(
        "deltacompression.backend.compression_factory.CompressionFactory",
        autospec=True)
    @mock.patch("deltacompression.backend.versions_processor.VersionsProcessor",
                autospec=True)
    def testCreatingVersionsProcessor(self, mock_versions_processor,
                                      mock_compr_factory, mock_alg_factory):
        """Tests running a single test."""
        mock_alg_factory().getAlgorithmFromName.return_value = "Ret alg"
        mock_compr_factory().getCompressionFromName.return_value = "Ret compr"
        mock_versions_processor(directory_processor.DirectoryProcessor). \
            runSimulation.return_value = (("/v1/", "data1"), ("/v2/", "data2"))

        self._exp_queue = queue.ExperimentQueue()
        self._exp_queue.setChunkerParameters(
            chunker.ChunkerParameters(1, 10, 7))

        self._experiment = experiment.Experiment(self._exp_queue,
                                                 self._dir_name,
                                                 self._exp_queue.def_alg,
                                                 self._exp_queue.def_compr)
        self._experiment.setAlgorithmName("MyAlg")
        self._experiment.setCompressionName("Compr")

        result = self._experiment.run()

        mock_alg_factory().getAlgorithmFromName.assert_called_with("MyAlg")
        mock_compr_factory().getCompressionFromName.assert_called_with("Compr")

        self.assertItemsEqual(result.versions_with_results, [("/v1/", 5),
                                                             ("/v2/", 5)])
        self.assertEqual(result.algorithm_name, "MyAlg")
        self.assertEqual(result.compression_name, "Compr")
        self.assertEqual(result.min_chunk, 1)
        self.assertEqual(result.max_chunk, 10)
        self.assertEqual(result.avg_chunk, 7)

    def testGetSetAlgorithmAndCompression(self):
        self.assertEqual(self._experiment.getAlgorithmName(),
                         self._exp_queue.def_alg)
        self._experiment.setAlgorithmName("asd")
        self.assertEqual(self._experiment.getAlgorithmName(), "asd")

        self.assertEqual(self._experiment.getCompressionName(),
                         self._exp_queue.def_compr)
        self._experiment.setCompressionName("dsa")
        self.assertEqual(self._experiment.getCompressionName(), "dsa")
