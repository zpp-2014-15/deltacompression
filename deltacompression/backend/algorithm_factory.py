"""This module is responsible for creating algorithms."""

import pyprimes
import random

from deltacompression.backend import chunk_hash
from deltacompression.backend import data_updater
from deltacompression.backend import diff
from deltacompression.backend import storage


def generate_prime(beg, end):
    cand = random.randrange(beg, end)
    while not pyprimes.isprime(cand):
        cand = random.randrange(beg, end)
    return cand


def generate_primes(amount, beg, end):
    primes = []
    for _ in xrange(amount):
        primes.append(generate_prime(beg, end))
    return primes


class AlgorithmFactory(object):

    DUMMY_ALGORITHM = "No delta encoding"
    OPTIMAL_ALGORITHM = "Optimal delta encoding"
    SIMILARITY_INDEX_ALGORITHM = "Similarity index delta encoding"

    ALL_ALGORITHMS = [
        DUMMY_ALGORITHM,
        OPTIMAL_ALGORITHM,
        SIMILARITY_INDEX_ALGORITHM
    ]

    def getAlgorithms(self):
        return self.ALL_ALGORITHMS

    def getAlgorithmFromName(self, name, storage_instance=None):
        if storage_instance is None:
            storage_instance = storage.Storage(chunk_hash.HashSHA256(), None)
        if name == self.DUMMY_ALGORITHM:
            return data_updater.DummyUpdater(storage_instance)
        elif name == self.OPTIMAL_ALGORITHM:
            diff_inst = diff.XDelta3Diff()
            return data_updater.OptimalDeltaUpdater(storage_instance, diff_inst)
        elif name == self.SIMILARITY_INDEX_ALGORITHM:
            diff_inst = diff.XDelta3Diff()
            par = data_updater.SimilarityIndexParams()
            par.fmod = 2 ** 20
            snum = 4
            par.ssize = 2
            par.win = 16

            random.seed(99453459353)
            beg = 1000000000
            end = 100000000000
            par.qmod = generate_prime(beg, end)
            par.prim = generate_prime(beg, end)
            primes = generate_primes(snum * par.ssize, beg, end)
            par.pis = [tuple(primes[x:x+2]) for x in xrange(0, len(primes), 2)]
            return data_updater.SimilarityIndexDeltaUpdater(storage_instance,
                                                            diff_inst,
                                                            par)
