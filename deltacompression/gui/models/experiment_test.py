"""Tests for experiment.py"""

import unittest
import mock

from deltacompression.gui.models import experiment


class ExperimentTest(unittest.TestCase):
    """Tests of Experiment class."""

    def setUp(self):
        self._experiment = experiment.Experiment()

    @mock.patch("deltacompression.backend.file_processor.FileProcessor",
                autospec=True)
    def testCreatingDefaultFileProcessor(self, mock_file_processor):
        self._experiment.runExperiment()
        mock_file_processor.assert_called_with(None, None, 1024 * 32, 1024 * 64)

    @mock.patch("deltacompression.backend.algorithm_factory.AlgorithmFactory",
                autospec=True)
    @mock.patch("deltacompression.backend.compression_factory.CompressionFactory",
                autospec=True)
    @mock.patch("deltacompression.backend.file_processor.FileProcessor",
                autospec=True)
    def testCreatingFileProcessor(self, mock_file_processor,
                                  mock_compression_factory,
                                  mock_algorithm_factory):
        alg_factory_instance = mock_algorithm_factory.return_value
        alg_factory_instance.getAlgorithmFromName.return_value = "Ret alg"
        compr_factory_instance = mock_compression_factory.return_value
        compr_factory_instance.getCompressionFromName.return_value = "Ret comp"
        self._experiment = experiment.Experiment()

        self._experiment.setChunkSizeRange(1, 10)
        self._experiment.setAlgorithmName("MyAlg")
        self._experiment.setCompressionName("Compr")
        self._experiment.addFileToList("D:/asd.asd")
        self._experiment.addFileToList("D:/asd.2")

        file_proc_instance = mock_file_processor.return_value
        file_proc_instance.processFile.return_value = "asddsa"
        result = self._experiment.runExperiment()

        alg_factory_instance.getAlgorithmFromName.assert_called_with("MyAlg")
        compr_factory_instance.getCompressionFromName.assert_called_with(
            "Compr")

        self.assertItemsEqual(result.files_with_results, [("D:/asd.asd", 6),
                                                          ("D:/asd.2", 6)])
        self.assertEqual(result.algorithm_name, "MyAlg")
        self.assertEqual(result.compression_name, "Compr")
        self.assertEqual(result.min_chunk, 1)
        self.assertEqual(result.max_chunk, 10)

    def testSetChunkSizeRange(self):
        self._experiment.setChunkSizeRange(1, 10)
        self.assertEqual(self._experiment.getChunkSizeRange(), (1, 10))

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
