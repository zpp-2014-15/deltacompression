"""Module contains all classes responsible for storing data."""


class Storage(object):
  """Class responsible for managing data chunks."""

  def __init__(self, hash_function, logger):
    """Creates Storage object.

    Args:
      hash_function: instance of HashFunction
      logger: instance of DriveLogger
    """

  def getChunk(self, hash_value):
    """Retrieves Chunk.

    Args:
      hash_value: hash value of chunk
    Returns:
      instance of Chunk corresponding to given hash."""


  def addChunk(self, chunk):
    """Adds new chunk to storage.

    Args:
      chunk: instance of Chunk.
    """
