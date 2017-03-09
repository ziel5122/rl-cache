import numpy as np
import math

# a cache with a reinforcement learning replacement policy
class ReCachedData:
    def __init__(self, data_size, cache_size):
        self.nhits = 0
        self.nmisses = 0
        self.data_size = data_size
        self.cache_size = cache_size
        self.cache_data = [0] * cache_size
        self.cache_addr = [-1] * cache_size
        self.cache_age = [0] * cache_size   # time since last access
        self.data = [0] * data_size
        for i in range(data_size):
            self.data[i] = i

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
        num_age_vals = 3
        cache_ages = [0] * num_age_vals
        for j in range(len(ages)):
            age = 0 if ages[j] < 2 else 1 if ages[j] < 5 else 2
            cache_ages[age] = cache_ages[age] + 1
        return tuple(cache_ages)

    # return the reinforcement learning state for this cache state
    # the state is a tuple with one element for each "abstract" cache age value
    def re_state(self):
        return ReCachedData.abst_state(self.cache_age)

    # update value at source state, using temporal differencing method TD(0)
    # - source, destination are abstract states
    # - reward is the reward associated with an action leading from source to destination
    def re_update(self, source, reward, destination):
        src_val = self.st_val[source]
        dest_val = self.st_val[destination]
        self.st_val[source] = src_val + self.alpha * (reward + self.gamma * dest_val - src_val)

    # return a list of the abstract states that can be reached from this
    # state by a cache replacement operation.  The first element in the
    # returned list is the abstract state obtained by replacing cache line 0.
    def successors(self):
        succs = list()
        for j in range(self.cache_size):
            ages = map(lambda x: x + 1, self.cache_age)
            ages[j] = 0
            succs[j] = ReCachedData.abst_state(ages)
        return succs

    # get data at index i, cached version
    def get(self, i):
        assert i >= 0 and i < self.data_size

        # get RL source state
        source = self.re_state()

        # increment time since last access for each cache element
        for j in range(self.cache_size):
            self.cache_age[j] = self.cache_age[j] + 1

        # is the value in the cache?
        for j in range(self.cache_size):
            if self.cache_addr[j] == i:
                # cache hit
                self.nhits = self.nhits + 1
                # cache line that was hit has age 0
                self.cache_age[j] = 0
                # get RL destination state, and update value of source state
                dest = self.re_state()
                self.re_update(source, self.hit_reward, dest)
                return self.cache_data[j]

        # cache miss
        self.nmisses = self.nmisses + 1
        x = self.data[i]

        # cache replacement policy -- uses reinforcement learning
        if np.random.rand < self.rand_frac:
            j = np.random.randint(0, self.cache_size)
        else:
            # use highest value successor
            succs = self.successors()
            max_val = None
            max_ind = 0
            for k in range(len(succs)):
                x = self.st_val[succs[k]]    # value of the kth successor
                if max_val is None or x > max_val:
                    max_val = max_val
                    max_ind = k
            j = max_ind
            self.re_update(source, self.miss_reward, succs[j])

        self.cache_addr[j] = i
        self.cache_data[j] = x
        self.cache_age[j] = 0

        return x

def main():
    data_size = 1000
    cache_size = 20

    move_size = [-3,-2,-1,0,0,0,0,1,2,3]
    cd = ReCachedData(data_size, cache_size)
    num_accesses = 10000
    j = math.floor(data_size/2)
    for _ in range(num_accesses):
        delta = move_size[np.random.randint(0, len(move_size))]
        j = j + delta
        if j < 0:
            j = 0
        elif j >= data_size:
            j = data_size - 1
        cd.get(j)

    print("hit ratio: ", cd.nhits/(cd.nhits + cd.nmisses))

if __name__ == '__main__':
    main()
