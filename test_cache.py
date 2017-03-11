from cache import Cache
import unittest

class TestCacheObject(unittest.TestCase):

    def test_constructor(self):
        self.assertRaises(AssertionError, Cache, 0, 2)
        self.assertRaises(AssertionError, Cache, 3, 0)
        self.assertRaises(AssertionError, Cache, 0, 0)

        cache0 = Cache(1, 3)
        self.assertEqual(cache0.levels, [1, 2, 4])
        self.assertEqual(cache0.level_ceilings, [1, 3, 7])
        self.assertEqual(cache0.tiers, [0, 1, 1, 2, 2, 2, 2])
        self.assertEqual(cache0.state, (1, 2, 4))
        self.assertEqual(cache0.size, 7)
        init_value = cache0.init_value
        self.assertEqual(cache0.states, {
            (0, 0, 7): init_value,
            (0, 1, 6): init_value,
            (0, 2, 5): init_value,
            (1, 0, 6): init_value,
            (1, 1, 5): init_value,
            (1, 2, 4): init_value
        })

    def test_state_and_incAges(self):
        cache0 = Cache(1, 3)
        self.assertEqual((1, 2, 4), cache0.state)
        cache0.incAges()
        cache0.updateTiers()
        cache0.updateState()
        self.assertEqual((0, 2, 5), cache0.state)
        cache0.incAges()
        cache0.updateTiers()
        cache0.updateState()
        self.assertEqual((0, 1, 6), cache0.state)
        cache0.incAges()
        cache0.updateTiers()
        cache0.updateState()
        self.assertEqual((0, 0, 7), cache0.state)
        cache0.incAges()
        cache0.updateTiers()
        cache0.updateState()
        self.assertEqual((0, 0, 7), cache0.state)

if __name__ == '__main__':
    unittest.main()
