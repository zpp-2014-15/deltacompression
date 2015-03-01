"""This module contains class responsible for adding chunks to the storage."""

from deltacompression.backend import chunk_update

class DataUpdater(object):
    """Class responsible for adding new chunks to the storage."""

    def __init__(self, storage_object):
        """Creates DataUpdater object.

        Args:
            storageObject: instance of Storage.
        """
        self._storage = storage_object

    def update(self, chunk):
        """Adds chunk to the storage.

        Args:
            chunk: instance of Chunk that will be added to the storage.
        Returns:
            ChunkUpdate object for the given chunk.
        """
        raise NotImplementedError

    def getLogger(self):
        return self._storage.getLogger()

    def addReceivedData(self, decompressed_data):
        """Updates the storage with the decompressed data received from another
        storage."""
        raise NotImplementedError


class DummyUpdater(DataUpdater):

    def update(self, chunk):
        if not self._storage.containsChunk(chunk):
            self._storage.addChunk(chunk)
            return chunk_update.DummyChunkUpdate(chunk)
        else:
            self._storage.incDedup()

    def addReceivedData(self, data):
        while data:
            update = chunk_update.DummyChunkUpdate.deserialize(data)
            self._storage.addChunk(update.getNewChunk())
            data = data[update.getBinarySize():]


class DeltaUpdater(DataUpdater):

    def __init__(self, storage_obj, diff):
        super(DeltaUpdater, self).__init__(storage_obj)
        self._diff = diff

    def addReceivedData(self, data):
        while data:
            update = chunk_update.DeltaChunkUpdate.deserialize(
                data, hash_size=self._storage.getHashFunction().getHashSize())
            new_chunk = update.getNewChunk(storage=self._storage,
                                           diff=self._diff)
            self._storage.addChunk(new_chunk)
            data = data[update.getBinarySize():]


class OptimalDeltaUpdater(DeltaUpdater):

    def update(self, chunk):
        if self._storage.containsChunk(chunk):
            self._storage.incDedup()
            return None

        best_update = chunk_update.DeltaChunkUpdate(None, chunk.get())
        for base in self._storage.getChunks():
            diff = self._diff.calculateDiff(base, chunk)
            hash_value = self._storage.getHashOfChunk(base)
            update = chunk_update.DeltaChunkUpdate(hash_value, diff)
            if update.getBinarySize() < best_update.getBinarySize():
                best_update = update
        self._storage.addChunk(chunk)
        return best_update
