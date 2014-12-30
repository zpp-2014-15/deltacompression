"""Tests for experiment.py"""

import unittest

from deltacompression.gui.models import experiment
from deltacompression.gui.models import test
from deltacompression.chunker_adapter import chunker


class ExperimentTest(unittest.TestCase):
    """Tests of Experiment class."""

    def setUp(self):
        self._experiment = experiment.Experiment()

    def testGetSetChunkerParameters(self):
        self._experiment.setChunkerParameters(
            chunker.ChunkerParameters(1, 10, 7))
        params = self._experiment.getChunkerParameters()
        self.assertEqual(params.getMinChunk(), 1)
        self.assertEqual(params.getMaxChunk(), 10)
        self.assertEqual(params.getAvgChunk(), 7)

    def testTestsList(self):
        """Tests if adding to/removing from tests list works properly."""
        test1 = test.Test("path1", self._experiment)
        test2 = test.Test("path2", self._experiment)
        test3 = test.Test("path3", self._experiment)
        test1.setAlgorithmName("algorithmus1")
        test2.setAlgorithmName("algorithmus2")
        test2.setCompressionName("compressionus2")
        test3.setCompressionName("compressionus3")

        self.assertEqual(self._experiment.getTestsList(), [])
        self._experiment.addTestToList(test1)
        self.assertEqual(self._experiment.getTestsList(), [test1])
        self._experiment.addTestToList(test2)
        self.assertEqual(self._experiment.getTestsList(), [test1, test2])
        self.assertEqual(self._experiment.getTest(1), test2)
        self._experiment.addTestToList(test3)
        self.assertEqual(self._experiment.getTestsList(), [test1, test2, test3])

        self.assertNotEqual(self._experiment.getTest(0).getAlgorithmName(),
                            self._experiment.getTest(1).getAlgorithmName())
        self.assertNotEqual(self._experiment.getTest(1).getCompressionName(),
                            self._experiment.getTest(2).getCompressionName())

        self._experiment.removeTestFromList(1)
        self.assertEqual(self._experiment.getTestsList(), [test1, test3])
        self.assertEqual(self._experiment.getTest(1), test3)
        self._experiment.removeTestFromList(1)
        self.assertEqual(self._experiment.getTestsList(), [test1])
        self._experiment.removeTestFromList(0)
        self.assertEqual(self._experiment.getTestsList(), [])
