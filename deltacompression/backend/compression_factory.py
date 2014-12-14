"""This module is responsible for creating compression algorithms."""

from deltacompression.backend import compression


class CompressionFactory(object):

    DUMMY_COMPRESSION = "No compression"

    ALL_COMPRESSIONS = [
        DUMMY_COMPRESSION
    ]

    def getCompressions(self):
        return self.ALL_COMPRESSIONS

    def getCompressionFromName(self, name):
        if name == self.DUMMY_COMPRESSION:
            return compression.DummyCompressionAlgorithm()
