"""Tests for chunk_update.py."""

import unittest

from deltacompression.backend import storage
from deltacompression.backend import chunk_update
from deltacompression.backend import test_utils


class DummyChunkUpdateTest(unittest.TestCase):

    def testSerialization(self):
        data = "this parrot is no more"
        chunk = storage.Chunk(data)
        update = chunk_update.DummyChunkUpdate(chunk)
        self.assertEqual(update.serialize(),
                         "{}{}".format("\x16\x00\x00\x00", data))

    def testDeserialization(self):
        data = "it has ceased to be"
        update = chunk_update.DummyChunkUpdate.deserialize(
            "{}{}".format("\x16\x00\x00\x00", data))
        self.assertEqual(update.getNewChunk().get(), data)

    def testGetNewChunk(self):
        """A black box test for DummyChunkUpdate."""
        data = "this is an ex-parrot"
        update1 = chunk_update.DummyChunkUpdate(storage.Chunk(data))
        update2 = update1.deserialize(update1.serialize())
        self.assertEqual(update2.getNewChunk().get(), data)



class DeltaChunkUpdateTest(unittest.TestCase):
    """DeltaChunkUpdate testing."""

    def setUp(self):
        self._hash_function = test_utils.PrefixHash()
        self._storage = storage.Storage(self._hash_function, None)
        self._diff_function = test_utils.MockupDiff()

    def testSerializationWithHash(self):
        hash_value = "Bravely bold sir Robin"
        diff = "Rode forth from Camelot"
        update = chunk_update.DeltaChunkUpdate(hash_value, diff)
        self.assertEqual(update.serialize(),
                         "{}{}{}".format("\x17\x00\x00\x00\x01",
                                         hash_value, diff))

    def testSerializationWithoutHash(self):
        hash_value = None
        diff = "Brave, brave, brave, brave Sir Robin!"
        update = chunk_update.DeltaChunkUpdate(hash_value, diff)
        self.assertEqual(update.serialize(),
                         "{}{}".format("\x25\x00\x00\x00\x00", diff))

    def testDeserializationWithHash(self):
        hash_value = "He was not afraid to die"
        diff = "Oh brave Sir Robin"
        update = chunk_update.DeltaChunkUpdate.deserialize(
            "{}{}{}".format("\x16\x00\x00\x00\x01", hash_value, diff),
            hash_size=len(hash_value))
        self.assertEqual(update.getHash(), hash_value)
        self.assertEqual(update.getDiff(), diff)

    def testDeserializationWithoutHash(self):
        hash_value = None
        diff = "He was not in the least bit scared to be mashed into pulp"
        update = chunk_update.DeltaChunkUpdate.deserialize(
            "{}{}".format("\x3A\x00\x00\x00\x00", diff))
        self.assertEqual(update.getHash(), hash_value)
        self.assertEqual(update.getDiff(), diff)

    def testBothEndsWithHash(self):
        hash_value = "He was not afraid at all"
        diff = "To be killed in nasty ways"
        update = chunk_update.DeltaChunkUpdate(hash_value, diff)
        binary = update.serialize()
        nupdate = chunk_update.DeltaChunkUpdate.deserialize(
            binary, hash_size=len(hash_value))
        self.assertEqual(nupdate.getDiff(), diff)
        self.assertEqual(nupdate.getHash(), hash_value)

    def testBothEndsWithoutHash(self):
        hash_value = None
        diff = "Or to have his eyes gouged out, and his elbows broken"
        update = chunk_update.DeltaChunkUpdate(hash_value, diff)
        binary = update.serialize()
        nupdate = chunk_update.DeltaChunkUpdate.deserialize(binary)
        self.assertEqual(nupdate.getDiff(), diff)
        self.assertIs(nupdate.getHash(), None)

    def testGetNewChunkWithHash(self):
        base = "To have his kneecap split, and his body burned away"
        base_chunk = storage.Chunk(base)
        target = "And his limbs all hacked and mangled, brave Sir Robin!"
        target_chunk = storage.Chunk(target)
        hash_value = self._hash_function.calculateHash(base_chunk)
        self._storage.addChunk(base_chunk)
        diff = self._diff_function.calculateDiff(base_chunk, target_chunk)
        update = chunk_update.DeltaChunkUpdate(hash_value, diff)
        ntarget = update.getNewChunk(storage=self._storage,
                                     diff_algorithm=self._diff_function)
        self.assertEqual(ntarget.get(), target)

    def testGetNewChunkWithoutHash(self):
        target = "And his limbs all hacked and mangled, brave Sir Robin!"
        update = chunk_update.DeltaChunkUpdate(None, target)
        ntarget = update.getNewChunk(storage=self._storage,
                                     diff_algorithm=self._diff_function)
        self.assertEqual(ntarget.get(), target)

if __name__ == "__main__":
    unittest.main()
