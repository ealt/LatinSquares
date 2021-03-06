import unittest

from latin_square_generator import LatinSquareGenerator


class LatinSquareGeneratorTest(unittest.TestCase):

    def test_get_reduced_latin_squares(self):
        generator = LatinSquareGenerator(4, subset='reduced')
        actual = list(generator.get_latin_squares())
        expected = list([
            [[0, 1, 2, 3],
            [1, 0, 3, 2],
            [2, 3, 0, 1],
            [3, 2, 1, 0]],

            [[0, 1, 2, 3],
            [1, 0, 3, 2],
            [2, 3, 1, 0],
            [3, 2, 0, 1]],

            [[0, 1, 2, 3],
            [1, 2, 3, 0],
            [2, 3, 0, 1],
            [3, 0, 1, 2]],
            
            [[0, 1, 2, 3],
            [1, 3, 0, 2],
            [2, 0, 3, 1],
            [3, 2, 1, 0]],
        ])
        self.assertCountEqual(actual, expected)

    def test_get_symbol_isotropy_classes(self):
        generator = LatinSquareGenerator(3, subset='symbol_isotropy_classes')
        actual = list(generator.get_latin_squares())
        expected = list([
            [[0, 1, 2],
            [1, 2, 0],
            [2, 0, 1]],

            [[0, 1, 2],
            [2, 0, 1],
            [1, 2, 0]],
        ])
        self.assertCountEqual(actual, expected)

    def test_get_all_latin_squares(self):
        generator = LatinSquareGenerator(3, subset='all')
        actual = list(generator.get_latin_squares())
        expected = list([
            [[0, 1, 2],
            [1, 2, 0],
            [2, 0, 1]],

            [[0, 1, 2],
            [2, 0, 1],
            [1, 2, 0]],

            [[0, 2, 1],
            [2, 1, 0],
            [1, 0, 2]],

            [[0, 2, 1],
            [1, 0, 2],
            [2, 1, 0]],

            [[1, 0, 2],
            [0, 2, 1],
            [2, 1, 0]],

            [[1, 0, 2],
            [2, 1, 0],
            [0, 2, 1]],

            [[1, 2, 0],
            [2, 0, 1],
            [0, 1, 2]],

            [[1, 2, 0],
            [0, 1, 2],
            [2, 0, 1]],

            [[2, 0, 1],
            [0, 1, 2],
            [1, 2, 0]],

            [[2, 0, 1],
            [1, 2, 0],
            [0, 1, 2]],

            [[2, 1, 0],
            [1, 0, 2],
            [0, 2, 1]],

            [[2, 1, 0],
            [0, 2, 1],
            [1, 0, 2]],
        ])
        self.assertCountEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()