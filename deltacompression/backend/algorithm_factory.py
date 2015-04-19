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

            # TODO the whole algorithm should be parametrized by the 2 values
            # below
            snum = 2
            ssize = 4
            random.seed(99453459353)
            beg = 10000000
            end = 1000000000
            qmod, prim = tuple([generate_prime(beg, end) for _ in xrange(2)])
            primes = generate_primes(2 * snum * ssize, beg, end)
            pis = [tuple(primes[x:x+2]) for x in xrange(0, len(primes), 2)]

            par = data_updater.SimilarityIndexParams(fmod=2 ** 20, ssize=ssize,
                                                     win=16, qmod=qmod, pis=pis,
                                                     prim=prim)
            return data_updater.SimilarityIndexDeltaUpdater(storage_instance,
                                                            diff_inst,
                                                            par)
