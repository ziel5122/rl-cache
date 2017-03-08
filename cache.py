from math import pow
from numpy import arange
from numpy import cumsum
from numpy import random
from numpy import subtract
from random import randint

class Cache:

	def __init__(self, level_min, num_levels):
		assert num_levels > 0 and level_min > 0
		self.levels = [level_min * 2 ** i for i in range(num_levels)]
		self.level_ceilings = list(cumsum(self.levels))

		self.size = sum(self.levels)
		self.indices = [-1] * self.size
		self.values = [0.0] * self.size
		self.ages = range(self.size)
		self.tiers = list(map(self.getTier, self.ages))
		self.state = self.getState()

		#reinforcement learning
		self.frac_rand = 0.1
		self.hit_reward = 2.0
		self.miss_reward = 0.0
		self.init_value = 1.0
		self.alpha = 0.2
		self.gamma = 0.2

		self.states = {}
		self.buildStates(num_levels)

	def applyState(self, old_state, new_state, index, value):
		if (old_state == new_state): return
		diff = list(subtract(new_state, old_state))
		print(diff)
		tier = diff.index(-1)
		print(tier)
		is_tier = list(map(lambda x: 1 if x == tier else 0, self.tiers))
		print(self.tiers)
		print(is_tier)
		is_tier = list(map(lambda x: x / sum(is_tier), is_tier))
		replace = random.choice(
			range(len(self.ages)),
			p=is_tier
		)
		print(self.tiers)
		print(replace)
		self.indices[replace] = index
		self.values[replace] = value
		self.ages[replace] = 0
		print(self.ages)
		self.tiers = list(map(self.getTier, self.ages))
		self.state = self.getState()
		print(self.state)
		print()

	def buildStates(self, num_levels, level=0, state=[]):
		if (level == num_levels-1):
			state.append(self.size - sum(state))
			self.states[tuple(state)] = self.init_value
			return

		for i in range(self.levels[level]+1):
			state_copy = state + [i]
			self.buildStates(num_levels, level+1, state_copy)

	def getTier(self, x):
		i = 0
		while (i < len(self.level_ceilings)-1):
			if (x < self.level_ceilings[i]): break
			i += 1
		return i

	def getState(self):
		state = [0] * len(self.levels)
		for tier in self.tiers:
			state[tier] += 1
		return tuple(state)

	def incAges(self):
		self.ages = list(map(lambda x: x+1, self.ages))
		self.tiers = list(map(self.getTier, self.ages))
		self.state = self.getState()

	def insert(self, index, value):
		print(self.ages)
		self.incAges()
		state0 = self.state
		new_states = []
		print(state0)
		for i in range(len(self.levels)):
			if (state0[i] == 0): continue
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
		print()
		self.applyState(new_states[0], new_states[new_index], index, value)

	def lookup(self, i):
		try:
			index = self.indices.index(i)
			self.ages[index] = 0
			return self.values[index]
		except ValueError:
			return -1
