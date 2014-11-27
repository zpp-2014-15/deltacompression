"""Tests for chunk_update.py."""

import unittest

from deltacompression.backend import storage, chunk_update

class DummyChunkUpdateTest(unittest.TestCase):

    def testSerialization(self):
        chunk = storage.Chunk("ni knights")
        update = chunk_update.DummyChunkUpdate(chunk)
        self.assertEqual(update.serialize(),
                         "{}{}".format("\n\x00\x00\x00", chunk.get()))

    def testDeserialization(self):
        data = "this parrot is no more"
        update = chunk_update.DummyChunkUpdate.deserialize(
            "{}{}".format("\x16\x00\x00\x00", data))
        self.assertEqual(update.getChunk().get(), data)

    def testSerializationAndDeserialization(self):
        for data in ["King Arthur", "Brian"]:
            update1 = chunk_update.DummyChunkUpdate(storage.Chunk(data))
            update2 = update1.deserialize(update1.serialize())
            self.assertEqual(update2.getChunk().get(), data)

if __name__ == "__main__":
    unittest.main()
