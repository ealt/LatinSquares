import unittest

from possibility_set import PossibilitySet


class PossibilitySetTest(unittest.TestCase):

    def test_empty_init(self):
        # defaults to including all elements in the domain
        possibility_set = PossibilitySet((4,))
        actual = list(possibility_set)
        expected = [(0,), (1,), (2,), (3,)]
        self.assertListEqual(actual, expected)

    def test_elminiate(self):
        possibility_set = PossibilitySet((2, 3, 4))
        possibility_set.elminate((0, 1, 2))
        actual = list(possibility_set)
        expected = [
            (1, 0, 0),
            (1, 0, 1),
            (1, 0, 3),
            (1, 2, 0),
            (1, 2, 1),
            (1, 2, 3),
        ]
        self.assertListEqual(actual, expected)
        possibility_set.elminate((0, 0, 0))
        actual = list(possibility_set)
        expected = [
            (1, 2, 1),
            (1, 2, 3),
        ]
        self.assertListEqual(actual, expected)
        possibility_set.elminate((0, 1, 3))
        actual = list(possibility_set)
        expected = [(1, 2, 1)]
        self.assertListEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
