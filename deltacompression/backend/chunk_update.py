"""Module contains ChunkUpdate class."""

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

    @classmethod
    def deserialize(cls, data):
        """Deserializes data.
        Args:
            data: data to deserialize
        Returns:
            ChunkUpdate object
        """
        raise NotImplementedError

    def getBinarySize(self):
        raise NotImplementedError


class DummyChunkUpdate(ChunkUpdate):
    """ChunkUpdate containing the whole new Chunk."""

    # size of len variable in bytes, used in binary representation
    LEN_SIZE = 4

    def __init__(self, chunk):
        self._chunk = chunk

    def serialize(self):
        return struct.pack("<i", len(self._chunk.get())) + self._chunk.get()

    @classmethod
    def deserialize(cls, data):
        size, = struct.unpack("<i", data[:cls.LEN_SIZE])
        return cls(storage.Chunk(data[cls.LEN_SIZE:(cls.LEN_SIZE+size)]))

    def getBinarySize(self):
        return 4 + len(self._chunk.get())

    def getChunk(self):
        return self._chunk

class DeltaChunkUpdate(ChunkUpdate):
    def __init__(self, hash_value, diff):
        self._hash = hash_value
        self._diff = diff
