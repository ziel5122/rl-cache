from cache import Cache
from random import randint
        
# a cache with a reinforcement learning replacement policy 

class RandomCache(Cache):

    def replace(self, index, data):
        replace = randint(0, self.size - 1)
        self.addr[replace] = index
        self.data[replace] = data