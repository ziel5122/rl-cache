from opt import OPTCache
from unittest import main, TestCase

class TestConstructor(TestCase):
    def test_init_error(self):
        self.assertRaises(TypeError, OPTCache, 'error not thrown with no args')

    def test_init(self):
        maxsize = 3
        accesses = [3, 4, 5]

        cache = OPTCache(maxsize, accesses)

        self.assertEqual(cache.get_access_count(), 0, '__access_count nonzeor')
        self.assertEqual(cache.get_accesses(), accesses, '__access nonzero')
        self.assertEqual(cache.get_data(), {}, '__data nonempty')
        self.assertEqual(cache.get_maxsize(), maxsize, '__maxsize incorrect')
        self.assertEqual(cache.get_size(), 0, '__size nonzero')

class TestMethods(TestCase):
    def setUp(self):
        self.cache = OPTCache(3, [1, 2, 3, 4, 1, 2])

    def test_set(self):
        self.cache[1] = 17
        self.cache[2] = 66
        self.cache[3] = 54
        temp = self.cache.get_data().copy()

        self.cache[4] = 7

        self.assertNotEqual(self.cache.get_data(), temp, 'cache contents unchanged')
        self.assertEqual(self.cache.get_size(), self.cache.get_maxsize())
        self.assertEqual(self.cache.get_size(), 3)

    def test_replacement(self):
        self.cache[1] = 17
        self.cache[2] = 66
        self.cache[3] = 54

        self.cache[4] = 7

        self.assertEqual(self.cache.get_data(), {1: 17, 2:66, 4: 7},
          'incorrect key removed')



if __name__ == '__main__':
    main()
