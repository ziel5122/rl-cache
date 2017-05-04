from cachetools import LFUCache, LRUCache, RRCache
import numpy as np
from random import randint

from cache.opt import OPTCache

def init(data_size=100, num_accesses=1000, std_dev=1):
    data = np.random.choice(range(data_size), size=data_size, replace=False)
    moves = np.around(np.random.normal(0, std_dev, num_accesses)).astype(np.int)
    i = randint(0, data_size-1)
    accesses = []

    for move in moves:
        i = np.clip(i+move, 0, data_size-1)
        accesses.append(i)

    return accesses, data


def run(cache, accesses, data):
    hits = 0
    misses = 0

    for access in accesses:
        try:
            cache[access]
            hits += 1
        except KeyError:
            misses += 1
            cache[access] = data[access]

    return hits, misses

def main():
    cache_size = 5
    data_size = 100
    num_accesses = 10000
    std_dev = 3

    accesses, data = init(data_size, num_accesses, std_dev)

    cache = OPTCache(cache_size, accesses)

    optimal_hits, optimal_misses = run(cache, accesses, data)

    cache = RRCache(cache_size)
    cache_hits, cache_misses = run(cache, accesses, data)

    print(optimal_hits, optimal_misses)
    print(cache_hits, cache_misses)

if __name__ == '__main__':
    main()
