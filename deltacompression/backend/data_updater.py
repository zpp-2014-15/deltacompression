"""This module contains class responsible for adding chunks to the storage."""

from deltacompression.backend import chunk_update

class DataUpdater(object):
    """Class responsible for adding new chunks to the storage."""

    def __init__(self, storage_object):
        """Creates DataUpdater object.

        Args:
            storageObject: instance of Storage
        """
        self._storage = storage_object

    def update(self, chunk):
        """Adds chunk to the storage.

        Args:
            chunk: instance of Chunk that will be added to the storage
        Returns:
            ChunkUpdate object for the given chunk
        """
        raise NotImplementedError

    def getName(self):
        """
        Returns:
            the name of the data updater algorithm
        """
        raise NotImplementedError

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
            return None

    def getName(self):
        return "Dummy Updater"

    def addReceivedData(self, data):
        while data:
            update = chunk_update.DummyChunkUpdate.deserialize(data)
            self._storage.addChunk(update.getChunk())
            data = data[update.getBinarySize():]
