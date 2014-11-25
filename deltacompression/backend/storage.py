"""Module contains all classes responsible for storing data."""


class StorageException(Exception):
    """Exception thrown by Storage class."""


class Storage(object):
    """Class responsible for managing data chunks."""

    def __init__(self, hash_function, logger):
        """Creates Storage object.

        Args:
            hash_function: instance of HashFunction.
            logger: instance of DriveLogger.
        """
        self._hash_function = hash_function
        self._logger = logger
        self._storage = {}

    def getChunk(self, hash_value):
        """Retrieves Chunk.

        Args:
            hash_value: hash value of chunk.
        Returns:
            instance of Chunk corresponding to given hash.
        Raises:
            StorageException if chunk does not exist.
        """
        if hash_value not in self._storage:
            raise StorageException("Chunk does not exist.")
        return self._storage[hash_value]

    def containsHash(self, hash_value):
        """Checks if storage contains chunk with given hash_value.

        Args:
            hash_value: hash of chunk to check.
        Returns:
            True if contains hash and False if not.
        """
        return hash_value in self._storage

    def addChunk(self, chunk):
        """Adds new chunk to storage.

        Args:
            chunk: instance of Chunk.
        Returns:
            hash of given chunk.
        Raises:
            StorageException if chunk already exists.
        """
        hash_value = self._hash_function.calculateHash(chunk)
        if hash_value in self._storage:
            raise StorageException("Chunk with given hash already exists.")
        self._storage[hash_value] = chunk
        return hash_value

    def getCorrespondingHash(self, chunk):
        """
        Args:
            chunk: instance of Chunk.
        Returns:
            hash of the chunk if it is in the storage, None otherwise.
        """
        hash_value = self._hash_function.calculateHash(chunk)
        if hash_value in self._storage:
            return hash_value
        else:
            return None


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
