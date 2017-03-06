from numpy import arange
from numpy import random
from random import randint

class Cache:

	def __init__(self, size, levels):
		self.size = size
		self.indices = [-1] * size
		self.values = [0.0] * size
		self.ages = range(0, size)

		#reinforcement learning
		self.frac_rand = 0.1
		self.hit_reward = 1.0
		self.miss_reward = -1.0
		self.init_value = 0.0
		self.alpha = 0.2
		self.gamma = 0.2

		self.states = {}
		for i in range(0, levels[0]+1):
			for j in range(0, levels[1]+1):
				self.states[(i,j,size-i-j)] = self.init_value

		print(self.states)

	def insert(self, i, x):
		state = self.state()

		print(tuple([state[0]+1,state[1],state[2]-1]))

		new states = [state, tuple([state[0]+1,state[1]-1,state[2]]), tuple([state[0]+1,state[1],state[2]-1])]
		print(new_states)
		#new_state = self.states[random.choice(new_state,p=(self.states[new_states[0]],self.states[new_states[1]],self.states[new_states[2]]))]

		#indices = [i for i, x in enumerate(my_list) if x == 2 or x == 3 or x == 4 or x == 5]

		#print(indices)

	def lookup(self, i):
		try:
			return self.values[self.indices.index(i)]
		except ValueError:
			return -1

	def state(self):
		cache_ages = [0] * 3
		for i in range(len(self.ages)):
			age = 0 if self.ages[i] < 2 else 1 if self.ages[i] < 6 else 2
			cache_ages[age] += 1
		return tuple(cache_ages)
