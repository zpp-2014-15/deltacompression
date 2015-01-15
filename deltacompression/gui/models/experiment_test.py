"""Test for experiment.py"""

import unittest
import mock

from deltacompression.backend import directory_processor
from deltacompression.chunker_adapter import chunker
from deltacompression.gui.models import experiment

class ExperimentTest(unittest.TestCase):
    """Tests of Experiment class"""

    def setUp(self):
        self._dir_name = "/home/me/test/"

    @mock.patch("deltacompression.backend.versions_processor.VersionsProcessor",
                autospec=True)
    def testCreatingVersionsProcessor(self, mock_versions_processor):
        """Tests running a single test."""
        mock_versions_processor(directory_processor.DirectoryProcessor). \
            runSimulation.return_value = (("/v1/", "data1"), ("/v2/", "data2"))

        exp = experiment.Experiment(self._dir_name)
        exp.setChunkerParameters(chunker.ChunkerParameters(1, 10, 7))

        result = exp.run()

        self.assertItemsEqual(result.versions_with_results, [("/v1/", 5),
                                                             ("/v2/", 5)])
        self.assertEqual(result.algorithm_name, exp.def_alg)
        self.assertEqual(result.compression_name, exp.def_compr)
        self.assertEqual(result.min_chunk, 1)
        self.assertEqual(result.max_chunk, 10)
        self.assertEqual(result.avg_chunk, 7)
