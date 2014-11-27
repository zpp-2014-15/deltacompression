"""Tests for chunk_update.py."""

import unittest

from deltacompression.backend import storage, chunk_update
from deltacompression.backend import chunk_hash


class DummyChunkUpdateTest(unittest.TestCase):

    def testSerialization(self):
        chunk = storage.Chunk("this parrot is no more")
        update = chunk_update.DummyChunkUpdate(chunk)
        self.assertEqual(update.serialize(),
                         "{}{}".format("\x16\x00\x00\x00", chunk.get()))

    def testDeserialization(self):
        data = "it has ceased to be"
        update = chunk_update.DummyChunkUpdate.deserialize(
            "{}{}".format("\x16\x00\x00\x00", data))
        self.assertEqual(update.getChunk().get(), data)

    def testSerializationAndDeserialization(self):
        """A black box test for DummyChunkUpdate."""
        data = "this is an ex-parrot"
        update1 = chunk_update.DummyChunkUpdate(storage.Chunk(data))
        update2 = update1.deserialize(update1.serialize())
        self.assertEqual(update2.getChunk().get(), data)


class DeltaChunkUpdateTest(unittest.TestCase):
    """DeltaChunkUpdate testing."""

    def setUp(self):
        self._hasher = chunk_hash.HashSHA256()

    def testSerialization(self):
        chunk = storage.Chunk("Bravely bold sir Robin")
        diff = "Rode forth from Camelot"
        hash_value = self._hasher.calculateHash(chunk)
        update = chunk_update.DeltaChunkUpdate(hash_value, diff)

        self.assertEqual(update.serialize(),
                         "{}{}{}".format("\x17\x00\x00\x00", hash_value, diff))

    def testDeserialization(self):
        chunk = storage.Chunk("He was not afraid to die")
        hash_value = self._hasher.calculateHash(chunk)
        diff = "Oh brave Sir Robin"
        update = chunk_update.DeltaChunkUpdate.deserialize(
            "{}{}{}".format("\x16\x00\x00\x00", hash_value, diff),
            self._hasher.getHashSize())
        self.assertEqual(update.getHash(), hash_value)
        self.assertEqual(update.getDiff(), diff)

    def testSerializationAndDeserialization(self):
        """A black box test for DeltaChunkUpdate."""
        chunk = storage.Chunk("He was not afraid at all")
        hash_value = self._hasher.calculateHash(chunk)
        diff = "To be killed in nasty ways"
        update = chunk_update.DeltaChunkUpdate(hash_value, diff)
        binary = update.serialize()
        nupdate = chunk_update.DeltaChunkUpdate.deserialize(
            binary, self._hasher.getHashSize())
        self.assertEqual(update.getDiff(), nupdate.getDiff())
        self.assertEqual(update.getHash(), nupdate.getHash())


if __name__ == "__main__":
    unittest.main()
