import unittest

from bitmap_set import BitmapSet

_shape = (2, 3, 4)
_a = (0, 0, 1)  # elem 1
_b = (0, 2, 0)  # elem 8
_c = (1, 0, 2)  # elem 14
_d = (1, 1, 3)  # elem 19


class BitmapSetTest(unittest.TestCase):

    maxDiff = None

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.addTypeEqualityFunc(BitmapSet, 'assertBitmapSetEqual')

    def assertBitmapSetEqual(self, bitmap_set1, bitmap_set2, msg=None):
        self.assertIsInstance(bitmap_set1, BitmapSet,
                              'First argument is not a BitmapSet')
        self.assertIsInstance(bitmap_set2, BitmapSet,
                              'Second argument is not a BitmapSet')
        self.assertSetEqual(bitmap_set1, bitmap_set2, msg)

    # ------- init methods -----------------------------------------------------

    def test_invalid_size(self):
        # size must by an integer...
        with self.assertRaises(TypeError):
            _ = BitmapSet(size=24.0)
        with self.assertRaises(TypeError):
            _ = BitmapSet(size='24')
        with self.assertRaises(TypeError):
            _ = BitmapSet(size=(24,))
        # ...greater than zero...
        with self.assertRaises(ValueError):
            _ = BitmapSet(size=0)
        # ...and equal to the product of the dimension lengths in shape
        with self.assertRaises(ValueError):
            _ = BitmapSet(size=4, shape=((2, 3, 4)))

    def test_size_init(self):
        bitmap_set = BitmapSet(size=4)
        self.assertEqual(bitmap_set.size, 4)
        self.assertTupleEqual(bitmap_set.shape, (4,))

    def test_invalid_shape(self):
        # shape must be a tuple...
        with self.assertRaises(TypeError):
            _ = BitmapSet(shape=24)
        with self.assertRaises(TypeError):
            _ = BitmapSet(shape=[2, 3, 4])
        # ...whose elements are all integers...
        with self.assertRaises(TypeError):
            _ = BitmapSet(shape=(2.0, 3.0, 4.0))
        with self.assertRaises(TypeError):
            _ = BitmapSet(shape=('2', '3', '4'))
        with self.assertRaises(TypeError):
            _ = BitmapSet(shape=((2, 3, 4),))
        # ...with positive values
        with self.assertRaises(ValueError):
            _ = BitmapSet(shape=(2, 3, 4, 0))

    def test_shape_init(self):
        bitmap_set = BitmapSet(shape=(2, 3, 4))
        self.assertEqual(bitmap_set.size, 24)
        self.assertTupleEqual(bitmap_set.shape, (2, 3, 4))

    def test_size_shape_init(self):
        bitmap_set = BitmapSet(size=24, shape=(2, 3, 4))
        self.assertEqual(bitmap_set.size, 24)
        self.assertTupleEqual(bitmap_set.shape, (2, 3, 4))

    def test_invalid_elems(self):
        # elems must be an int or iterable
        with self.assertRaises(TypeError):
            _ = BitmapSet(shape=_shape, elems=524546.0)


if __name__ == '__main__':
    unittest.main()
