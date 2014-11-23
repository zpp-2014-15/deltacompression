"""Python adapter for the external chunking module."""

from subprocess import Popen, PIPE
import cStringIO
from deltacompression.storage import Chunk
import os.path as op

class ChunkerException(Exception):
    """Exception thrown by Chunker."""

class Chunker(object):
    """Python adapter for the external chunker module."""

    path = op.join(op.abspath(op.dirname(__file__)), 'adapter')

    def __init__(self, min_chunk, max_chunk):
        """Creates a Chunker object.

        Args:
            min_chunk: minimal chunk's size.
            max_chunk: maximal chunk's size.
        Raises:
            ChunkerException, if the needed adapter binary is not present.
        """
        if not op.isfile(self.path):
            raise ChunkerException("There is no '{}' file".format(self.path))
        self._min_chunk = min_chunk
        self._max_chunk = max_chunk

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
        process = Popen([self.path, str(self._min_chunk),
                         str(self._max_chunk), file_name], stdout=PIPE)
        out, err = process.communicate()
        retcode = process.wait()
        if retcode:
            raise ChunkerException(err)
        buf = cStringIO.StringIO(out)
        chunks = []
        for line in buf:
            chunks.append(int(line.strip()))
        with open(file_name, 'r') as fil:
            for chunk in chunks:
                yield Chunk(fil.read(chunk))
