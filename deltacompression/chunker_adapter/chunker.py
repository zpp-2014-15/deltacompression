"""Python adapter for the external chunking module."""

import os.path as op
import subprocess
import cStringIO
import collections

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


class StreamReader(object):
    """Class for convenient reading from a sequence of files.
    It lets us treat a sequence of files as a stream of data."""

    def __init__(self):
        self._queue = collections.deque()
        self._file = None

    def _prepareFile(self):
        if not self._file:
            filename = self._queue.popleft()
            self._file = open(filename, 'r')

    def getChunk(self, size):
        buf = cStringIO.StringIO()
        while size:
            self._prepareFile()
            part = self._file.read(size)
            if len(part) < size:
                self._file.close()
                self._file = None
            size -= len(part)
            buf.write(part)
        return storage.Chunk(buf.getvalue())

    def addFile(self, filename):
        self._queue.append(filename)

    def close(self):
        if self._file and not self._file.closed:
            self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, _type, value, traceback):
        self.close()


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
        out, err = process.communicate("\n".join(files).encode("utf-8"))
        retcode = process.wait()
        if retcode:
            raise ChunkerException(err)
        buf = cStringIO.StringIO(out)

        # format of communication: -1 when a new file begins and later the
        # sizes of chunks in the consecutive lines that use only the files that
        # we already have
        file_num = 0
        with StreamReader() as sreader:
            for line in buf:
                num = int(line.strip())
                if num == -1:
                    sreader.addFile(files[file_num])
                    file_num += 1
                else:
                    yield sreader.getChunk(num)
