import numpy as np
import math
from random import randint
from random_cache import RandomCache

cache = RandomCache(20)  
  
def get(i, num_hits, num_misses, data_size):
	assert i >= 0 and i < data_size

	x = cache.lookup(i)

	#cache miss
	if (x < 0):
		num_misses += 1
		x = data[i]
		cache.replace(i, x)
	#cache hit
	else:
		num_hits += 1

	return num_hits, num_misses
  
data_size = 1000

data = [0] * data_size
for i in range(data_size):
  data[i] = randint(1,1000)
  
move_size1 = [-3, -2, -1, 0, 0, 0, 0, 1, 2, 3]
move_size2 = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
  
num_hits = 0
num_misses = 0
num_acc = 10000
  
j = (int)(data_size/2)
for i in range(num_acc):
	delta = move_size1[randint(0, len(move_size1)-1)]
	j += delta
	if (j < 0): j = 0
	elif (j >= data_size): j = data_size-1

	num_hits, num_misses = get(j, num_hits, num_misses, data_size)

print("hits: " + str(num_hits))
print('misses: ' + str(num_misses))