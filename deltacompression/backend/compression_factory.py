"""This module is responsible for creating algorithms."""

from deltacompression.backend import compression_algorithm


class CompressionFactory(object):

    DUMMY_COMPRESSION = "No compression"

    ALL_COMPRESSIONS = [
        DUMMY_COMPRESSION
    ]

    def getCompressions(self):
        return self.ALL_COMPRESSIONS

    def getCompressionFromName(self, name):
        if name == self.DUMMY_COMPRESSION:
            return compression_algorithm.DummyCompressionAlgorithm()
