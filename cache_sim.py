from argparse import ArgumentParser
from cachetools import LFUCache, LRUCache, RRCache
from random import randint, random
from rl_cache import Cache as RLCache

#one memory access
def get(cache, data, j, num_hits, num_misses):
    assert j >= 0 and j < len(data)

    b = cache.__contains__(j)

    if b:
        x = cache.__getitem__(j)
        num_hits += 1
    else:
        cache.__setitem__(j, data[j])
        x = data[j]
        num_misses += 1

    #print(x)
    #print(j)
    #print(data[j])
    #print('\n')

    ''''
	#cache miss
	if (x < 0):
		num_misses += 1
		x = data[j]
		cache.replace(j, x)
	#cache hit
	else:
		num_hits += 1
    '''

    return num_hits, num_misses

#parse command line argumenrs
def get_args():
    parser = ArgumentParser(description='Simulate a cache replacement policy.')
    #cache type/replacement policy (e.g. random, lru, rl)
    parser.add_argument('type', metavar='type',
                        help='Type of cache/policy to use')
    #cache size
    parser.add_argument('-c', '--cache_size', type=int, default=50,
                        help='Number of lines in the cache')
    #data size
    parser.add_argument('-d', '--data_size', type=int, default=1000,
                        help='Number of data items in memory')
    #number of memory accesses
    parser.add_argument('-n', '--num_accesses', type=int, default=10000,
                        help='Number of memory accesses to execute')
    #if set: non-localized workload, else localized
    parser.add_argument('-w', '--workload', choices=[1, 2],
                        help='Localized workload')
    return parser.parse_args()

#initialize <cache_type> cache of size <cache_size>
def get_cache(cache_type, cache_size):
    caches = {
        'lfu': LFUCache(cache_size),
        'lru': LRUCache(cache_size),
        #'rl' : RLCache(cache_size),
        'rr' : RRCache(cache_size)
    }

    try:
        return caches[cache_type]
    except KeyError:
        return default()

#initialize data array
def get_data(data_size):
    #random values [0.0, 1.0)
    return [random() for i in range(data_size)], data_size

#determine workload
def get_workload(workload):
    if workload == 2:
        move_size = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
    else:
        move_size = [-3, -2, -1, 0, 0, 0, 0, 1, 2, 3]

    return move_size, len(move_size)

def main():
    num_hits = 0
    num_misses = 0

    args = get_args(); #get cl args

    cache = get_cache(args.type, args.cache_size) #initialze cache

    data, data_size = get_data(args.data_size) #initialize data

    move_size, move_len = get_workload(args.workload) #pick workload

    j = int(data_size / 2)
    #run trials
    for i in range(args.num_accesses):
    	j += move_size[randint(0, move_len-1)]

    	if (j < 0): j = 0
    	elif (j >= data_size): j = data_size-1

    	num_hits, num_misses = get(cache, data, j, num_hits, num_misses)

    print("hits: " + str(num_hits))
    print('misses: ' + str(num_misses))
    print('hit ratio: ' + str(float(num_hits)/args.num_accesses))

if __name__ == '__main__':
	main()
