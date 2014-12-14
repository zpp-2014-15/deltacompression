"""Tests for the diff algorithms."""

import unittest

from deltacompression.backend import diff
from deltacompression.backend import storage


class XDelta3Test(unittest.TestCase):
    """Tests for class XDelta3Diff."""

    def setUp(self):
        self._diff = diff.XDelta3Diff()

    def testDiff(self):
        """Black-box tests."""
        data1 = "Always look on the light side of life"
        data2 = "Always look on the bright side of death"
        ch1 = storage.Chunk(data1)
        ch2 = storage.Chunk(data2)
        diff_value = self._diff.calculateDiff(ch1, ch2)
        nch = self._diff.applyDiff(ch1, diff_value)
        self.assertEqual(nch.get(), data2)
