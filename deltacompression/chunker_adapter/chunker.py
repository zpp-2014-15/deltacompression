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

        params = map(str, list(self._chunker_params.getParameters()))
        process = subprocess.Popen([self.path] + params,
                                   stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
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
