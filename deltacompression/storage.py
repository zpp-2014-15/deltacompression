"""Module contains all classes responsible for storing data."""


class Storage(object):
    """Class responsible for managing data chunks."""

    def __init__(self, hash_function, logger):
        """Creates Storage object.

        Args:
            hash_function: instance of HashFunction.
            logger: instance of DriveLogger.
        """

    def getChunk(self, hash_value):
        """Retrieves Chunk.

        Args:
            hash_value: hash value of chunk.
        Returns:
            instance of Chunk corresponding to given hash.
        """


    def addChunk(self, chunk):
        """Adds new chunk to storage.

        Args:
            chunk: instance of Chunk.
        Returns:
            hash of given chunk.
        """


class Chunk(object):
    """Class responsible for storing one data chunk."""

    def __init__(self, data):
        """Creates data chunk.

        Args:
            data: chunk of data.
        """
        self._data = data

    def get(self):
        return self._data
