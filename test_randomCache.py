from random_cache import RandomCache
from unittest import main
from unittest import TestCase

class TestRandomCache(TestCase):
    
    def setUp(self):
        self.cache_size = 20
        self.cache = RandomCache(self.cache_size)
    
    def test_constructor(self):
        self.assertEqual(self.cache.size, self.cache_size)
        self.assertEqual(len(self.cache.addr), self.cache_size)
        self.assertEqual(len(self.cache.data), self.cache_size)
        
        self.assertEqual(self.cache.addr, [-1] * self.cache_size)
        self.assertEqual(self.cache.data, [0] * self.cache_size)
        
    def test_lookup(self):
        self.assertEqual(self.cache.lookup(-1), 0)
        self.assertEqual(self.cache.lookup(1), -1)

    def test_replace(self):
        self.assertEqual(self.cache.lookup(1), -1)
        self.cache.replace(1, 0.5)
        self.assertEqual(self.cache.lookup(1), 0.5)
        
if __name__ == '__main__':
    main()
        