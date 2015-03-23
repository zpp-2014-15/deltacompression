"""Module responsible for logging storage events."""

class IOLogger(object):
    """Class responsible for counting read, writes and deduplications."""

    def __init__(self):
        self._reads = 0
        self._writes = 0
        self._duplicates = 0
        self._total_blocks = 0

    def getReads(self):
        return self._reads

    def getWrites(self):
        return self._writes

    def getDuplicates(self):
        return self._duplicates

    def getTotalBlocks(self):
        return self._total_blocks

    def incReads(self, increase_by=1):
        self._reads += increase_by

    def incWrites(self, increase_by=1):
        self._writes += increase_by

    def incDuplicates(self, increase_by=1):
        self._duplicates += increase_by

    def incTotalBlocks(self, increase_by=1):
        self._total_blocks += increase_by
