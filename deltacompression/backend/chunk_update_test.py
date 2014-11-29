"""Tests for chunk_update.py."""

import unittest

from deltacompression.backend import storage, chunk_update


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

    def testSerialization(self):
        hash_value = "Bravely bold sir Robin"
        diff = "Rode forth from Camelot"
        update = chunk_update.DeltaChunkUpdate(hash_value, diff)
        self.assertEqual(update.serialize(),
                         "{}{}{}".format("\x17\x00\x00\x00", hash_value, diff))

    def testDeserialization(self):
        hash_value = "He was not afraid to die"
        diff = "Oh brave Sir Robin"
        update = chunk_update.DeltaChunkUpdate.deserialize(
            "{}{}{}".format("\x16\x00\x00\x00", hash_value, diff),
            hash_size=len(hash_value))
        self.assertEqual(update.getHash(), hash_value)
        self.assertEqual(update.getDiff(), diff)

    def testSerializationAndDeserialization(self):
        """A black box test for DeltaChunkUpdate."""
        hash_value = "He was not afraid at all"
        diff = "To be killed in nasty ways"
        update = chunk_update.DeltaChunkUpdate(hash_value, diff)
        binary = update.serialize()
        nupdate = chunk_update.DeltaChunkUpdate.deserialize(
            binary, hash_size=len(hash_value))
        self.assertEqual(diff, nupdate.getDiff())
        self.assertEqual(hash_value, nupdate.getHash())


if __name__ == "__main__":
    unittest.main()
