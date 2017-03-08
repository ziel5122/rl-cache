from math import pow
from numpy import arange
from numpy import cumsum
from numpy import random
from random import randint

class Cache:

	def __init__(self, level_min, num_levels):
		self.levels = [level_min * 2 ** i for i in range(num_levels)]
		self.level_ceilings = cumsum(self.levels)

		self.size = sum(self.levels)
		self.indices = [-1] * self.size
		self.values = [0.0] * self.size
		self.ages = range(self.size)

		#reinforcement learning
		self.frac_rand = 0.1
		self.hit_reward = 2.0
		self.miss_reward = 0.0
		self.init_value = 1.0
		self.alpha = 0.2
		self.gamma = 0.2

		self.states = {}
		self.buildStates(num_levels)

		print(self.states)

	def applyState(self, old_state, new_state, index, value):
		if (old_state == new_state): return
		start = randint(0, len(self.ages)-1)
		if (new_state[1] < old_state[1]):
			while(True):
				if (self.ages[start] >= self.level_ceilings[0] and self.ages[start] < self.level_ceilings[1]):
					self.indices[start] = index
					self.values[start] = value
					self.ages[start] = 0
					return
				start += 1
				start %= len(self.ages)
		while(True):
			if (self.ages[start] >= self.level_ceilings[1]):
				self.indices[start] = index
				self.values[start] = value
				self.ages[start] = 0
				return
			start += 1
			start %= len(self.ages)

	def buildStates(self, num_levels, level=0, state=[]):
		if (level == num_levels-1):
			state.append(self.size - sum(state))
			self.states[tuple(state)] = self.init_value
			print(state)
			return

		for i in range(self.levels[level]+1):
			state_copy = state + [i]
			self.buildStates(num_levels, level+1, state_copy)

	def incAges(self):
		self.ages = list(map(lambda x: x+1, self.ages))

	def insert(self, index, value):
		self.incAges()
		state0 = self.state()
		new_states = [state0]
		for i in range(len(self.levels)):
			if (state0[i] == 0 or state0[0] == self.levels[0]): continue
			state_copy = list(state0)
			state_copy[i] -= 1
			state_copy[0] += 1
			new_states.append(tuple(state_copy))

		print(new_states)
		probs = [self.states[new_states[i]] for i in range(len(new_states))]
		probs_total = sum(probs)
		probs = list(map(lambda x: x/probs_total, probs))
		new_index = random.choice(range(len(new_states)), p=probs)
		print(new_states[new_index])
		self.applyState(state0, new_states[new_index], index, value)

	def lookup(self, i):
		try:
			index = self.indices.index(i)
			self.ages[index] = 0
			return self.values[index]
		except ValueError:
			return -1

	def state(self):
		cache_ages = [0] * len(self.levels)
		for i in range(len(self.ages)):
			j = 0
			while (j < len(self.level_ceilings)):
				if (self.ages[i] < self.level_ceilings[j]):
					break
				j += 1
			cache_ages[min(j,len(self.levels)-1)] += 1
		return tuple(cache_ages)
