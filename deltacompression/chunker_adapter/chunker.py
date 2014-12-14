"""Python adapter for the external chunking module."""

import os.path as op
import subprocess
import cStringIO

from deltacompression.backend import storage


class ChunkerParameters(object):
    """Class for holding Chunker's parameters."""

    def __init__(self, min_chunk, max_chunk, avg_chunk):
        self._min_chunk = min_chunk
        self._max_chunk = max_chunk
        self._avg_chunk = avg_chunk

    def getParameters(self):
        """Returns consecutive chunker's parameters. The order is important."""
        return (self._min_chunk, self._max_chunk, self._avg_chunk)

    def getMinChunk(self):
        return self._min_chunk

    def getMaxChunk(self):
        return self._max_chunk

    def getAvgChunk(self):
        return self._avg_chunk


class ChunkerException(Exception):
    """Exception thrown by Chunker."""


class Chunker(object):
    """Python adapter for the external chunker module."""

    path = op.join(op.abspath(op.dirname(__file__)), "adapter")
    no_file_msg = "There is no '{}' file"

    def __init__(self, chunker_params):
        """Creates a Chunker object.

        Args:
            chunker_params: ChunkerParameters' instance
        Raises:
            ChunkerException, if the needed adapter binary is not present.
        """
        if not op.isfile(self.path):
            raise ChunkerException(self.no_file_msg.format(self.path))
        self._chunker_params = chunker_params

    def chunkData(self, file_name):
        """Chunks file into smaller pieces.

        Args:
            file_name: absolute or relative path to a file.
        Returns:
            an iterable with Chunk objects
        Raises:
            ChunkerException in case of errors during communication.
            OSError
            IOError
        """
        if not op.isfile(file_name):
            raise ChunkerException(self.no_file_msg.format(file_name))

        params = map(str, list(self._chunker_params.getParameters()))
        process = subprocess.Popen([self.path] + params + [file_name],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = process.communicate()
        retcode = process.wait()
        if retcode:
            raise ChunkerException(err)
        buf = cStringIO.StringIO(out)
        chunks = []
        for line in buf:
            chunks.append(int(line.strip()))
        with open(file_name, "r") as fil:
            for chunk in chunks:
                yield storage.Chunk(fil.read(chunk))
