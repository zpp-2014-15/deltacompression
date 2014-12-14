"""Module contains compression algorithms."""


class Compression(object):
    """Class representing compression algorithm."""

    def compress(self, data):
        """
        Args:
            data: data to be compressed.
        Returns:
            compressed data.
        """
        raise NotImplementedError

    def decompress(self, compressed_data):
        """
        Args:
            compressed_data: data to be decompressed.
        Returns:
            decompressed data.
        """
        raise NotImplementedError


class DummyCompression(Compression):

    def compress(self, data):
        return data

    def decompress(self, compressed_data):
        return compressed_data
