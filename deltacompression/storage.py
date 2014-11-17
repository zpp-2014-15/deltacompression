"""Module contains all classes responsible for storing data."""


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
    """
    if hash_value not in self._storage:
      raise KeyError
    return self._storage[hash_value]

  def addChunk(self, chunk):
    """Adds new chunk to storage.

    Args:
      chunk: instance of Chunk.
    Returns:
      hash of given chunk.
    """
    hash_value = self._hash_function.computeHash(chunk)
    if hash_value in self._storage:
      raise KeyError
    self._storage[hash_value] = chunk
    return hash_value
