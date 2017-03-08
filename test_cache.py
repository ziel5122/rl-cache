from cache import Cache
import unittest

class TestCacheObject(unittest.TestCase):

    def test_constructor(self):
        self.assertRaises(AssertionError, Cache, 0, 2)
        self.assertRaises(AssertionError, Cache, 3, 0)
        self.assertRaises(AssertionError, Cache, 0, 0)

        cache0 = Cache(2, 3)
        self.assertEqual(cache0.levels, [2, 4, 8])
        self.assertEqual(cache0.level_ceilings, [2, 6, 14])
        self.assertEqual(cache0.tiers, [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2])
        self.assertEqual(cache0.state, (2, 4, 8))
        self.assertEqual(cache0.size, 14)
        init_value = cache0.init_value
        self.assertEqual(cache0.states, {
            (0, 0, 14): init_value,
            (0, 1, 13): init_value,
            (0, 2, 12): init_value,
            (0, 3, 11): init_value,
            (0, 4, 10): init_value,
            (1, 0, 13): init_value,
            (1, 1, 12): init_value,
            (1, 2, 11): init_value,
            (1, 3, 10): init_value,
            (1, 4, 9): init_value,
            (2, 0, 12): init_value,
            (2, 1, 11): init_value,
            (2, 2, 10): init_value,
            (2, 3, 9): init_value,
            (2, 4, 8): init_value
        })

        cache1 = Cache(1, 4)
        self.assertEqual(cache1.levels, [1, 2, 4, 8])
        self.assertEqual(cache1.level_ceilings, [1, 3, 7, 15])
        self.assertEqual(cache1.tiers, [0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3])
        self.assertEqual(cache1.state, (1, 2, 4, 8))
        self.assertEqual(cache1.size, 15)
        self.assertEqual(cache1.states, {
            (0, 0, 0, 15): init_value,
            (0, 0, 1, 14): init_value,
            (0, 0, 2, 13): init_value,
            (0, 0, 3, 12): init_value,
            (0, 0, 4, 11): init_value,
            (0, 1, 0, 14): init_value,
            (0, 1, 1, 13): init_value,
            (0, 1, 2, 12): init_value,
            (0, 1, 3, 11): init_value,
            (0, 1, 4, 10): init_value,
            (0, 2, 0, 13): init_value,
            (0, 2, 1, 12): init_value,
            (0, 2, 2, 11): init_value,
            (0, 2, 3, 10): init_value,
            (0, 2, 4, 9): init_value,
            (1, 0, 0, 14): init_value,
            (1, 0, 1, 13): init_value,
            (1, 0, 2, 12): init_value,
            (1, 0, 3, 11): init_value,
            (1, 0, 4, 10): init_value,
            (1, 1, 0, 13): init_value,
            (1, 1, 1, 12): init_value,
            (1, 1, 2, 11): init_value,
            (1, 1, 3, 10): init_value,
            (1, 1, 4, 9): init_value,
            (1, 2, 0, 12): init_value,
            (1, 2, 1, 11): init_value,
            (1, 2, 2, 10): init_value,
            (1, 2, 3, 9): init_value,
            (1, 2, 4, 8): init_value
        })

    def test_state_and_incAges(self):
        cache0 = Cache(2, 3)
        self.assertEqual((2, 4, 8), cache0.state)
        cache0.incAges()
        self.assertEqual((1, 4, 9), cache0.state)
        cache0.incAges()
        self.assertEqual((0, 4, 10), cache0.state)

if __name__ == '__main__':
    unittest.main()
