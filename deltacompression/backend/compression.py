"""Module contains compression algorithms."""
import lzo
import pylzma
import zlib


class Compression(object):
    """Compression interface."""

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


class LzoCompression(Compression):

    def compress(self, data):
        return lzo.compress(data, 9)

    def decompress(self, compressed_data):
        return lzo.decompress(compressed_data)


class ZipCompression(Compression):

    def compress(self, data):
        return zlib.compress(data, 9)

    def decompress(self, compressed_data):
        return zlib.decompress(compressed_data)


class LzmaCompression(Compression):

    def compress(self, data):
        return pylzma.compress(data)

    def decompress(self, compressed_data):
        return pylzma.decompress(compressed_data)
