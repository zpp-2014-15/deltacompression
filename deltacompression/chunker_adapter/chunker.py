"""Python adapter for the external chunking module."""

import os.path as op
import subprocess
import cStringIO

from deltacompression.backend import storage


class ChunkerException(Exception):
    """Exception thrown by Chunker."""


class Chunker(object):
    """Python adapter for the external chunker module."""

    path = op.join(op.abspath(op.dirname(__file__)), "adapter")
    no_file_msg = "There is no '{}' file"

    def __init__(self, min_chunk, max_chunk):
        """Creates a Chunker object.

        Args:
            min_chunk: minimal chunk's size.
            max_chunk: maximal chunk's size.
        Raises:
            ChunkerException, if the needed adapter binary is not present.
        """
        if not op.isfile(self.path):
            raise ChunkerException(self.no_file_msg.format(self.path))
        self._min_chunk = min_chunk
        self._max_chunk = max_chunk

    def chunkData(self, files):
        """Chunks files into smaller pieces.

        Args:
            files: absolute or relative paths to files.
        Returns:
            an iterable with Chunk objects
        Raises:
            ChunkerException in case of errors during communication.
            OSError
            IOError
        """
        for file_name in files:
            if not op.isfile(file_name):
                raise ChunkerException(self.no_file_msg.format(file_name))

        process = subprocess.Popen([self.path, str(self._min_chunk),
                                    str(self._max_chunk)],
                                   stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
        out, err = process.communicate("\n".join(files).encode('utf-8'))
        retcode = process.wait()
        if retcode:
            raise ChunkerException(err)
        buf = cStringIO.StringIO(out)

        chunks = []
        file_num = 0
        for line in buf:
            num = int(line.strip())
            if num == -1:
                with open(files[file_num], "r") as fil:
                    for chunk in chunks:
                        yield storage.Chunk(fil.read(chunk))
                file_num += 1
                chunks = []
            else:
                chunks.append(num)
