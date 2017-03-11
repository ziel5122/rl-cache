import numpy as np
import math
from random import randint
        
# a cache with a reinforcement learning replacement policy 

class RandomCache:
  
  def __init__(self, size):
    self.size = size
    self.data = [0] * self.size
    self.addr = [-1] * self.size
    
  def lookup(self, i):
    try:
      return self.data[self.addr.index(i)]
    except ValueError:
      return -1
  
  def replace(self, index, data):
    replaced = randint(0, self.size - 1)
    self.addr[replaced] = index
    self.data[replaced] = data