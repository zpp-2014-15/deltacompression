"""This module is responsible for creating compression algorithms."""

from deltacompression.backend import compression


class CompressionFactory(object):

    DUMMY_COMPRESSION = "No compression"
    LZO_COMPRESSION = "Lzo compression"
    ZIP_COMPRESSION = "Zip compression"

    ALL_COMPRESSIONS = [
        DUMMY_COMPRESSION,
        LZO_COMPRESSION,
        ZIP_COMPRESSION
    ]

    def getCompressions(self):
        return self.ALL_COMPRESSIONS

    def getCompressionFromName(self, name):
        if name == self.DUMMY_COMPRESSION:
            return compression.DummyCompression()
        elif name == self.LZO_COMPRESSION:
            return compression.LzoCompression()
        elif name == self.ZIP_COMPRESSION:
            return compression.ZipCompression()
