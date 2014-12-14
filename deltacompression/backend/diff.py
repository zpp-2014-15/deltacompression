"""Module contains Diff interface and its various implementations."""

import os

import xdelta3

from deltacompression.backend import storage


class DiffException(Exception):
    """An exception during executing the diff."""


class Diff(object):
    """Diff interface."""

    def calculateDiff(self, base_chunk, new_chunk):
        """Calculates the diff between base_chunk and new_chunk."""
        raise NotImplementedError

    def applyDiff(self, base_chunk, diff):
        """Applies diff to the base_chunk.
        Args:
            base_chunk: Chunk.
            diff: String.
        Returns:
            Chunk.
        """
        raise NotImplementedError


class XDelta3Diff(Diff):
    """Diff from xdelta3."""

    # maximum available amount of bytes that can be used underneath
    MAX_SIZE = 500 * 1000 * 1000

    def calculateDiff(self, base_chunk, new_chunk):
        result, patch = xdelta3.xd3_encode_memory(new_chunk.get(),
                                                  base_chunk.get(),
                                                  self.MAX_SIZE)
        if result:
            raise DiffException("Error: '{}'".format(os.strerror(result)))
        return patch

    def applyDiff(self, base_chunk, diff):
        result, target = xdelta3.xd3_decode_memory(diff,
                                                   base_chunk.get(),
                                                   self.MAX_SIZE)
        if result:
            raise DiffException("Error: '{}'".format(os.strerror(result)))
        return storage.Chunk(target)
