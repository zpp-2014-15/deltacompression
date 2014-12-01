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

    @classmethod
    def deserialize(cls, data, **kwargs):
        """Creates a ChunkUpdate object from the given data.
        Args:
            data: String to be deserialized.
            kwargs: additional, implementation specific arguments.
        Returns:
            deserialized ChunkUpdate object.
        """
        raise NotImplementedError

    def getNewChunk(self, **kwargs):
        """Creates a new Chunk object using implementation specific
        arguments."""
        raise NotImplementedError


class DummyChunkUpdate(ChunkUpdate):
    """ChunkUpdate containing the whole new Chunk."""

    # format for the length of the chunk - it's 32-bit integer, little-endian
    FMT = "<i"
    # size of length variable in bytes, used in binary representation
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

    def getNewChunk(self):
        return self._chunk


class DeltaChunkUpdate(ChunkUpdate):
    """ChunkUpdate containing a hash of a base Chunk and the diff value
    between the base and the final Chunk or the whole content of the
    new chunk. The difference will be reflected in the binary representation.
    """

    # format:  32-bit, little-endian size of diff and distinction byte
    FMT = "<ib"
    # size of signature in bytes
    LEN_SIZE = struct.Struct(FMT).size

    def __init__(self, hash_value, diff):
        """Creates a new DeltaChunkUpdate object.
        Args:
            hash_value: String, iff there is some corresponding base chunk or
                None, if we create a chunk from scratch.
            diff: String, content used in creating a new Chunk.
        """
        self._hash = hash_value
        self._diff = diff

    def serialize(self):
        dist_byte = int(bool(self._hash))
        signature = struct.pack(self.FMT, len(self._diff), dist_byte)
        segments = [signature, self._hash if self._hash else "", self._diff]
        return "".join(segments)

    def getBinarySize(self):
        ans = self.LEN_SIZE + len(self._diff)
        if self._hash:
            ans += len(self._hash)
        return ans

    @classmethod
    def deserialize(cls, data, **kwargs):
        size, dist_byte = struct.unpack(cls.FMT, data[:cls.LEN_SIZE])
        diff_beg = cls.LEN_SIZE
        if dist_byte:
            hash_size = kwargs.pop('hash_size')
            hash_value = data[cls.LEN_SIZE:cls.LEN_SIZE + hash_size]
            diff_beg += hash_size
        else:
            hash_value = None
        diff = data[diff_beg:diff_beg + size]
        return DeltaChunkUpdate(hash_value, diff)

    def getHash(self):
        return self._hash

    def getDiff(self):
        return self._diff

    def getNewChunk(self, **kwargs):
        diff_algorithm = kwargs.pop('diff_algorithm')
        storage_obj = kwargs.pop('storage')
        if self._hash:
            base_chunk = storage_obj.getChunk(self._hash)
            return diff_algorithm.applyDiff(base_chunk, self._diff)
        else:
            return storage.Chunk(self._diff)
