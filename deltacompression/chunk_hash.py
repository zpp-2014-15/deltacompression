"""This module contains all hash functions available for Chunk."""

import hashlib


class HashFunction(object):

  def calculateHash(self, chunk):
    """Abstract method for calculating hash."""
    raise NotImplementedError


class HashSHA256(HashFunction):

  def calculateHash(self, chunk):
    hasher = hashlib.sha256()
    hasher.update(chunk.get())
    return hasher.hexdigest()
