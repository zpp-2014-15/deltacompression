"""Class responsible for saving number of reads and writes."""

class IOLogger(object):

    def __init__(self):
        self._read_counter = 0
        self._write_counter = 0
        self._dedup = 0

    def getReads(self):
        return self._read_counter

    def getWrites(self):
        return self._write_counter

    def getDedup(self):
        return self._dedup

    def incReads(self, by=1):
        self._read_counter += by

    def incWrites(self, by=1):
        self._write_counter += by

    def incDedup(self):
        self._dedup += 1
