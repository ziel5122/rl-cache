from cachetools import LFUCache, LRUCache, RRCache
from collections import Counter
import numpy as np
import math
from random import randint
from random import random
from sets import Set
import sys

# a cache with a reinforcement learning replacement policy
class RLCache:
    def __init__(self, cache_size, data_size):
        self.min_pos = 100
        self.min_neg = -100
        self.nhits = 0
        self.nmisses = 0
        self.data_size = data_size
        self.cache_size = cache_size
        self.cache_data = [0.0] * cache_size
        self.cache_addr = [-1] * cache_size
        self.cache_age = [0] * cache_size   # time since last access
        self.data = [random() for i in range(data_size)]

        # reinforcement learning
        # table of state values for reinforcement learning
        self.st_val = dict()    # table of state values
        self.frac_rand = 0.1    # fraction of time to choose random replacement
        self.hit_reward = 1.0
        self.miss_reward = -1.0
        self.init_value = 0.0
        self.alpha = 0.2
        self.gamma = 0.2

    # given a list of concrete ages, return a tuple of abstract age counts
    @staticmethod
    def abst_state(ages):
        '''
        num_age_vals = 3
        cache_ages = [0] * num_age_vals
        for j in range(len(ages)):
            age = 0 if ages[j] < 2 else 1 if ages[j] < 5 else 2
            cache_ages[age] = cache_ages[age] + 1
        return tuple(cache_ages)
        '''
        return max(ages)

    # return the reinforcement learning state for this cache state
    # the state is a tuple with one element for each "abstract" cache age value
    def re_state(self):
        return RLCache.abst_state(self.cache_age)

    # update value at source state, using temporal differencing method TD(0)
    # - source, destination are abstract states
    # - reward is the reward associated with an action leading from source to destination
    def re_update(self, source, reward, destination):
        src_val = self.st_val.get(source, self.init_value)
        dest_val = self.st_val.get(destination, self.init_value)
        future_val = src_val + self.alpha * (reward + self.gamma * dest_val - src_val)
        self.st_val[source] = future_val
        diff = future_val - src_val
        '''
        if diff > 0:
            if diff < self.min_pos:
                self.min_pos = diff
                print(self.min_pos)
                print(self.min_neg)
                print(source)
                print()
        elif diff > self.min_neg:
            self.min_neg = diff
            print(self.min_pos)
            print(self.min_neg)
            print(source)
            print()
        '''
        print("{0:.2f}".format(diff), source)
        #self.st_val[source] = src_val + self.alpha * (reward + self.gamma * dest_val - src_val)

    # return a list of the abstract states that can be reached from this
    # state by a cache replacement operation.  The first element in the
    # returned list is the abstract state obtained by replacing cache line 0.
    def successors(self):
        succs = list()
        for j in range(self.cache_size):
            ages_copy = list(self.cache_age)
            ages_copy[j] = 0
            succs.append(RLCache.abst_state(ages_copy))
        return set(succs)

    # get data at index i, cached version
    def get(self, j):
        assert j >= 0 and j < self.data_size

        # get RL source state
        source = self.re_state()

        # increment time since last access for each cache element
        self.cache_age = list(map(lambda x: x + 1, self.cache_age))

        # is the value in the cache?
        try:
            index = self.cache_addr.index(j)
            # cache hit
            self.nhits += 1
            # cache line that was hit has age 0
            self.cache_age[index] = 0
            # get RL destination state, and update value of source state
            dest = self.re_state()
            self.re_update(source, self.hit_reward, dest)
            return self.data[index]
        except ValueError:
            # cache miss
            self.nmisses +=  1
            x = self.data[j]

            i = 0
            # cache replacement policy -- uses reinforcement learning
            if (random() < self.frac_rand):
                i = randint(0, self.cache_size-1)
            else:
                # use highest value successor
                succs = self.successors()
                max_val = None
                succ = None
                for k in succs:
                    x = self.st_val.get(k, self.init_value)    # value of the kth successor
                    if max_val is None or x > max_val:
                        max_val = max_val
                        succ = k
                self.re_update(source, self.miss_reward, succ)

                i = self.cache_age.index(succ)
                self.cache_addr[i] = j
                self.cache_data[i] = x
                self.cache_age[i] = 0

                return x


def run_optimal(cache_size, data, moves):
    cache = [-1] * cache_size
    hits = 0
    data_size = len(data)
    index = randint(0, data_size-1)
    accesses = []
    for move in moves:
        index += move
        if (index < 0):
            index = 0
        elif (index >= data_size):
            index = data_size -1
        accesses.append(index)

    cache[0:cache_size] = accesses[0:cache_size]
    misses = cache_size

    for index, access in enumerate(accesses[cache_size:]):
        if access in cache:
            hits += 1
        else:
            misses += 1
            next_access_time = []
            for element in cache:
                try:
                    next_access_time.append(accesses[index:].index(element))
                except ValueError:
                    next_access_time.append(len(moves) + 1)
            cache[next_access_time.index(max(next_access_time))] = access

    print(hits, misses)

def init(data_size=100, num_accesses=1000, std_dev=1):
    moves = np.around(np.random.normal(0, std_dev, num_accesses)).astype(np.int)
    i = randint(0, data_size-1)
    accesses = []
    for move in moves:
        i = np.clip(i+move, 0, data_size-1)
        accesses.append(i)
    return accesses

def run_cache(cache, accesses):
    hits = 0
    misses = 0
    for access in accesses:
        try:
            cache[access]
            hits += 1
        except KeyError:
            misses += 1
            cache[access] = random()
    return hits, misses

def run_optimal(cache_size, accesses):
    hits = 0
    misses = 0
    cache = Set()
    for i, access in enumerate(accesses):
        if access in cache:
            hits += 1
        else:
            misses += 1
            if len(cache) < cache_size:
                cache.add(access)
            else:
                next_accesses = Counter()
                for line in cache:
                    try:
                        next_accesses[line] = accesses[i+1:].index(line)
                    except ValueError:
                        next_accesses[line] = len(accesses)+1
                index, next_access = next_accesses.most_common(1)[0]
                cache.remove(index)
                cache.add(access)
    return hits, misses

def main():
    cache_size = 5
    data_size = 100
    num_accesses = 1000
    std_dev = 3

    accesses = init(data_size, num_accesses, std_dev)

    optimal_hits, optimal_misses = run_optimal(cache_size, accesses)

    cache = RRCache(cache_size)
    cache_hits, cache_misses = run_cache(cache, accesses)

    print(optimal_hits, optimal_misses)
    print(cache_hits, cache_misses)

if __name__ == '__main__':
    main()
