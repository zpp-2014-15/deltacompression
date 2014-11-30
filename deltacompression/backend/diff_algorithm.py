"""Module contains DiffAlgorithm interface and various its implementations."""

import struct

import xdelta3

from deltacompression.backend import storage


class DiffException(Exception):
    """An exception during executing the diff algorithm."""

class DiffAlgorithm(object):
    """Diff algorithm interface."""

    def calculateDiff(self, base_chunk, new_chunk):
        """Calculates the diff between base_chunk and new_chunk."""
        raise NotImplementedError

    def applyDiff(self, base_chunk, diff):
        """Applies diff to the base_chunk.
        Args:
            base_chunk: Chunk
            diff: String
        Returns:
            Chunk
        """
        raise NotImplementedError


class XDelta3Diff(DiffAlgorithm):
    """Diff from xdelta3."""

    FMT = "<i"
    SIZE = struct.Struct(FMT).size

    def calculateDiff(self, base_chunk, new_chunk):
        result, patch = xdelta3.xd3_encode_memory(new_chunk.get(),
                                                  base_chunk.get(),
                                                  len(new_chunk.get()))
        if result:
            raise DiffException("Error, {} returned".format(result))
        return struct.pack(self.FMT, len(new_chunk.get())) + patch


    def applyDiff(self, base_chunk, diff):
        if len(diff) < self.SIZE:
            raise DiffException("Diff too short")
        size, = struct.unpack(self.FMT, diff[:self.SIZE])
        result, target = xdelta3.xd3_decode_memory(diff[self.SIZE:],
                                                   base_chunk.get(),
                                                   size)
        if result:
            raise DiffException("Error, {} returned".format(result))
        return storage.Chunk(target)
