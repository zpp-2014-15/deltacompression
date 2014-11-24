"""This module contains class responsible for adding chunks to the storage."""

from deltacompression.backend import storage


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
            data to be sent through the network
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
        try:
            self._storage.addChunk(chunk)
            return chunk
        except storage.StorageException:
            return self._storage.getHashFunction().calculateHash(chunk)

    def getName(self):
        return "Dummy Updater"
