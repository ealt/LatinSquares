import unittest

from utils import to_orthogonal_array, from_orthogonal_array, Triple


class OperationsTest(unittest.TestCase):

    def test_to_orthogonal_array(self):
        latin_square = [
            [0, 1, 2],
            [1, 2, 0],
            [2, 0, 1],
        ]
        actual = to_orthogonal_array(latin_square)
        expected = [
            Triple(r=0, c=0, s=0),
            Triple(r=0, c=1, s=1),
            Triple(r=0, c=2, s=2),
            Triple(r=1, c=0, s=1),
            Triple(r=1, c=1, s=2),
            Triple(r=1, c=2, s=0),
            Triple(r=2, c=0, s=2),
            Triple(r=2, c=1, s=0),
            Triple(r=2, c=2, s=1),
        ]
        self.assertCountEqual(actual, expected)

    def test_from_orthogonal_array(self):
        orthogonal_array = [
            Triple(r=0, c=0, s=0),
            Triple(r=0, c=1, s=1),
            Triple(r=0, c=2, s=2),
            Triple(r=1, c=0, s=1),
            Triple(r=1, c=1, s=2),
            Triple(r=1, c=2, s=0),
            Triple(r=2, c=0, s=2),
            Triple(r=2, c=1, s=0),
            Triple(r=2, c=2, s=1),
        ]
        actual = from_orthogonal_array(orthogonal_array)
        expected = [
            [0, 1, 2],
            [1, 2, 0],
            [2, 0, 1],
        ]
        self.assertListEqual(actual, expected)        


if __name__ == '__main__':
    unittest.main()