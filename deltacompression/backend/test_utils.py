"""Classes used in many other modules - e.g. mockup classes for tests."""

import struct

from deltacompression.backend import diff
from deltacompression.backend import storage
from deltacompression.backend import chunk_hash


class MockupDiff(diff.Diff):
    """Dummy diff algorithm which just doesn't use the base chunk."""

    def calculateDiff(self, base_chunk, new_chunk):
        return new_chunk.get()

    def applyDiff(self, base_chunk, diff_function):
        return storage.Chunk(diff_function)


class PrefixDiff(diff.Diff):
    """A diff algorithm which compares prefixes of chunks."""

    FMT = "<i"
    SIZE = struct.calcsize(FMT)

    def calculateDiff(self, base_chunk, new_chunk):
        prefix = 0
        base = base_chunk.get()
        new = new_chunk.get()
        mini = min(len(base), len(new))
        while prefix < mini and base[prefix] == new[prefix]:
            prefix += 1
        return struct.pack(self.FMT, prefix) + new[prefix:]

    def applyDiff(self, base_chunk, diff_value):
        prefix, = struct.unpack(self.FMT, diff_value[:self.SIZE])
        rest = diff_value[self.SIZE:]
        return storage.Chunk(base_chunk.get()[:prefix] + rest)


class PrefixHash(chunk_hash.HashFunction):

    LEN = 10

    def calculateHash(self, chunk):
        return chunk.get()[:self.LEN].zfill(self.LEN)

    def getHashSize(self):
        return self.LEN
