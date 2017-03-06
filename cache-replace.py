from cache import Cache
from math import floor
from random import randint

cache_size = 10
data_size = 1000
num_accesses = 100000
num_hits = 0
num_misses = 0

data = []
move_size1 = [-3, -2, -1, 0, 0, 0, 0, 1, 2, 3]
move_size2 = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]

i=2
cache = Cache(cache_size, (i,i*2,cache_size-i-i*2))

def get(i, num_hits, num_misses, data_size):
	assert i >= 0 and i < data_size

	x = cache.lookup(i)

	#cache miss
	if (x < 1):
		num_misses += 1
		x = data[i]
		cache.insert(i, x)
	#cache hit
	else:
		num_hits += 1

	return num_hits, num_misses

for i in range(data_size):
	data.append(i / 2.0)

j = (int)(data_size/2)
for i in range(num_accesses):
	delta = move_size1[randint(0, len(move_size1)-1)]
	j += delta
	if (j < 0): j = 0
	elif (j >= data_size): j = data_size-1

	num_hits, num_misses = get(j, num_hits, num_misses, data_size)

print("hits: " + str(num_hits))
print('misses: ' + str(num_misses))
