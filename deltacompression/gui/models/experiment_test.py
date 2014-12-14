"""Tests for experiment.py"""

import unittest
import mock

from deltacompression.gui.models import experiment
from deltacompression.chunker_adapter import chunker


class ExperimentTest(unittest.TestCase):
    """Tests of Experiment class."""

    def setUp(self):
        self._experiment = experiment.Experiment()

    @mock.patch("deltacompression.backend.algorithm_factory.AlgorithmFactory",
                autospec=True)
    @mock.patch(
        "deltacompression.backend.compression_factory.CompressionFactory",
        autospec=True)
    @mock.patch("deltacompression.backend.file_processor.FileProcessor",
                autospec=True)
    def testCreatingFileProcessor(self, mock_file_processor,
                                  mock_compression_factory,
                                  mock_algorithm_factory):
        """Tests running experiment."""
        alg_factory_instance = mock_algorithm_factory.return_value
        alg_factory_instance.getAlgorithmFromName.return_value = "Ret alg"
        compr_factory_instance = mock_compression_factory.return_value
        compr_factory_instance.getCompressionFromName.return_value = "Ret comp"
        self._experiment = experiment.Experiment()

        self._experiment.setChunkerParameters(
            chunker.ChunkerParameters(1, 10, 7))
        self._experiment.setAlgorithmName("MyAlg")
        self._experiment.setCompressionName("Compr")
        self._experiment.addFileToList("D:/asd.asd")
        self._experiment.addFileToList("D:/asd.2")

        file_proc_instance = mock_file_processor.return_value
        file_proc_instance.processFiles.return_value = "asddsa"
        result = self._experiment.runExperiment()

        alg_factory_instance.getAlgorithmFromName.assert_called_with("MyAlg")

        self.assertItemsEqual(result.files_with_results, [("D:/asd.asd", 6),
                                                          ("D:/asd.2", 6)])
        self.assertEqual(result.algorithm_name, "MyAlg")
        self.assertEqual(result.compression_name, "Compr")
        self.assertEqual(result.min_chunk, 1)
        self.assertEqual(result.max_chunk, 10)
        self.assertEqual(result.avg_chunk, 7)

    def testSetChunkerParameters(self):
        self._experiment.setChunkerParameters(
            chunker.ChunkerParameters(1, 10, 7))
        params = self._experiment.getChunkerParameters()
        self.assertEqual(params.getMinChunk(), 1)
        self.assertEqual(params.getMaxChunk(), 10)
        self.assertEqual(params.getAvgChunk(), 7)

    def testGetSetAlgorithmAndCompression(self):
        self.assertEqual(self._experiment.getAlgorithmName(), "None")
        self._experiment.setAlgorithmName("asd")
        self.assertEqual(self._experiment.getAlgorithmName(), "asd")

        self.assertEqual(self._experiment.getCompressionName(), "None")
        self._experiment.setCompressionName("dsa")
        self.assertEqual(self._experiment.getCompressionName(), "dsa")

    def testFileList(self):
        self.assertEqual(self._experiment.getFileList(), [])
        self._experiment.addFileToList("D:/some/file.asd")
        self.assertEqual(self._experiment.getFileList(), ["D:/some/file.asd"])
        self._experiment.addFileToList("D:/some/file.asd")
        self.assertEqual(self._experiment.getFileList(), ["D:/some/file.asd",
                                                          "D:/some/file.asd"])
        self._experiment.removeFileFromList("D:/some/file.asd")
        self.assertEqual(self._experiment.getFileList(), ["D:/some/file.asd"])
        self._experiment.clearFileList()
        self.assertEqual(self._experiment.getFileList(), [])
