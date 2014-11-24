"""Module contains compression algorithms."""


class CompressionAlgorithm(object):
    def compress(self, data):
        raise NotImplementedError

    def getName(self):
        raise NotImplementedError


class DummyCompressionAlgorithm(CompressionAlgorithm):
    def compress(self, data):
        return "".join(data)

    def getName(self):
        return "Dummy Compression Algorithm"
