"""This module contains class responsible for adding chunks to the storage."""


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
            data representing given chunk
        """
        raise NotImplementedError

    def getName(self):
        """
        Returns:
            the name of the data updater algorithm
        """
        raise NotImplementedError


class DummyUpdater(DataUpdater):

    def update(self, chunk):
        if self._storage.containsChunk(chunk):
            return self._storage.getHashOfChunk(chunk)
        else:
            self._storage.addChunk(chunk)
            return chunk.get()

    def getName(self):
        return "Dummy Updater"
