"""Module contains classes responsible for representing a chunk's update."""

import struct

from deltacompression.backend import storage


class ChunkUpdate(object):
    """Abstract class representing a Chunk's update."""

    def serialize(self):
        """Serializes this object.

        Returns:
            String with binary representation of object.
        """
        raise NotImplementedError

    def getBinarySize(self):
        raise NotImplementedError


class DummyChunkUpdate(ChunkUpdate):
    """ChunkUpdate containing the whole new Chunk."""

    # format for the size of the chunk - it's 32-bit integer, little-endian
    FMT = "<i"
    # size of len variable in bytes, used in binary representation
    LEN_SIZE = struct.Struct(FMT).size

    def __init__(self, chunk):
        self._chunk = chunk

    def serialize(self):
        return (struct.pack(self.FMT, len(self._chunk.get())) +
                self._chunk.get())

    @classmethod
    def deserialize(cls, data):
        size, = struct.unpack(cls.FMT, data[:cls.LEN_SIZE])
        return cls(storage.Chunk(data[cls.LEN_SIZE:(cls.LEN_SIZE + size)]))

    def getBinarySize(self):
        return self.LEN_SIZE + len(self._chunk.get())

    def getChunk(self):
        return self._chunk


class DeltaChunkUpdate(ChunkUpdate):
    """ChunkUpdate a hash of a base Chunk and the diff value between the base
    and final Chunk. """

    # format for the size of the chunk - it's 32-bit integer, little-endian
    FMT = "<i"
    # size of len variable in bytes, used in binary representation
    LEN_SIZE = struct.Struct(FMT).size


    def __init__(self, hash_value, diff):
        self._hash = hash_value
        self._diff = diff

    def serialize(self):
        return "{}{}{}".format(struct.pack(self.FMT, len(self._diff)),
                               self._hash, self._diff)

    def getBinarySize(self):
        return self.LEN_SIZE + len(self._hash) + len(self._diff)

    @classmethod
    def deserialize(cls, data, hash_size):
        size, = struct.unpack(cls.FMT, data[:cls.LEN_SIZE])
        return DeltaChunkUpdate(
            data[cls.LEN_SIZE:cls.LEN_SIZE + hash_size],
            data[cls.LEN_SIZE + hash_size:cls.LEN_SIZE + hash_size + size])

    def getHash(self):
        return self._hash

    def getDiff(self):
        return self._diff
