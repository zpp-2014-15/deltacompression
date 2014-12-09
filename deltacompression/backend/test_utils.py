"""Classes used in many other modules - e.g. mockup classes for tests."""

import os
import os.path as op
import shutil
import struct

from deltacompression.backend import diff_algorithm
from deltacompression.backend import storage
from deltacompression.backend import chunk_hash

TEST_DIR_PATH = op.join(op.abspath(op.dirname(__file__)), "__test_dir__")
TEST_FILE_PATH = op.join(op.abspath(op.dirname(__file__)), "__test_file__")


class MockupDiff(diff_algorithm.DiffAlgorithm):
    """Dummy diff algorithm which just doesn't use the base chunk."""

    def calculateDiff(self, base_chunk, new_chunk):
        return new_chunk.get()

    def applyDiff(self, base_chunk, diff):
        return storage.Chunk(diff)


class PrefixDiff(diff_algorithm.DiffAlgorithm):
    """A diff algorithm which compares prefixes of chunks."""

    FMT = "<i"
    SIZE = struct.calcsize(FMT)

    def calculateDiff(self, base_chunk, new_chunk):
        prefix = 0
        base = base_chunk.get()
        new = new_chunk.get()
        mini = min(len(base), len(new))
        while prefix < mini and base[prefix] == new[prefix]:
            prefix += 1
        return struct.pack(self.FMT, prefix) + new[prefix:]

    def applyDiff(self, base_chunk, diff):
        prefix, = struct.unpack(self.FMT, diff[:self.SIZE])
        rest = diff[self.SIZE:]
        return storage.Chunk(base_chunk.get()[:prefix] + rest)


class PrefixHash(chunk_hash.HashFunction):

    LEN = 10

    def calculateHash(self, chunk):
        return chunk.get()[:self.LEN].zfill(self.LEN)

    def getHashSize(self):
        return self.LEN


def createDirectoryWithContent(dir_name, files):
    """Creates directory with subdirectories and files.
    Args:
        dir_name: name of the directory.
        files: a list of pairs (file_name, file_content).
    """

    if not op.exists(TEST_DIR_PATH):
        os.makedirs(TEST_DIR_PATH)

    dir_path = op.join(TEST_DIR_PATH, dir_name)

    if op.exists(dir_path):
        shutil.rmtree(dir_path)

    os.makedirs(dir_path)

    for name, content in files:
        file_name = op.join(dir_path, name)
        file_dir_name = op.dirname(file_name)

        if not op.exists(file_dir_name):
            os.makedirs(file_dir_name)
        with open(file_name, "w") as tfile:
            tfile.write(content)
