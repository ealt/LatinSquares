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

    def test_empty_init(self):
        # default to empty set
        bitmap_set = BitmapSet(shape=_shape)
        self.assertListEqual(list(bitmap_set), [])
        # value of 0 corresponds to empty set
        bitmap_set = BitmapSet(shape=_shape, elems=0)
        self.assertListEqual(list(bitmap_set), [])
        # set explicity with an empty sequence
        bitmap_set = BitmapSet(shape=_shape, elems=[])
        self.assertListEqual(list(bitmap_set), [])

    def test_invalid_elems(self):
        # elems must be an int or iterable
        with self.assertRaises(TypeError):
            _ = BitmapSet(shape=_shape, elems=524546.0)

    def test_elems_sequence_init(self):
        bitmap_set = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        self.assertListEqual(list(bitmap_set), [_a, _b, _c])

    def test_elems_int_init(self):
        # bin(524546) = '000000000100000100000010'
        # indicies of ones:  ^19  ^14   ^8     ^1
        bitmap_set = BitmapSet(shape=_shape, elems=16642)
        self.assertListEqual(list(bitmap_set), [_a, _b, _c])

    # ------- container methods ------------------------------------------------

    def test_len(self):
        bitmap_set = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        self.assertEqual(len(bitmap_set), 3)

    # ------- single elem methods ----------------------------------------------

    def test_invalid_elem(self):
        bitmap_set = BitmapSet(shape=(2, 3, 4))
        bitmap_set_1d = BitmapSet(size=4)
        # if shape is not 1d, elem must be a tuple...
        with self.assertRaises(TypeError):
            1 in bitmap_set
        with self.assertRaises(TypeError):
            [0, 0, 1] in bitmap_set
        # ...if shape is 1d int is the only other acceptable type...
        with self.assertRaises(TypeError):
            1.0 in bitmap_set_1d
        with self.assertRaises(TypeError):
            '1' in bitmap_set_1d
        # ...tuple elements must have the same len as shape...
        with self.assertRaises(TypeError):
            (0, 1) in bitmap_set
        with self.assertRaises(TypeError):
            (0, 1) in bitmap_set_1d
        # ...and tuple values must all be integers...
        with self.assertRaises(TypeError):
            ('0', '0', '1') in bitmap_set
        with self.assertRaises(TypeError):
            (1.0,) in bitmap_set
        # ...that are non-negative...
        with self.assertRaises(ValueError):
            (0, 0, -1) in bitmap_set
        with self.assertRaises(ValueError):
            (-1,) in bitmap_set_1d
        # ...and less than the corresponding dimension length in shape
        with self.assertRaises(ValueError):
            (3, 0, 1) in bitmap_set
        with self.assertRaises(ValueError):
            (4,) in bitmap_set_1d

    def test_contains(self):
        bitmap_set = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        bitmap_set_1d = BitmapSet(size=4, elems=[0, 1, 2])
        # does contain
        self.assertTrue(_b in bitmap_set)
        self.assertTrue(1 in bitmap_set_1d)
        # does not contain
        self.assertFalse(_d in bitmap_set)
        self.assertFalse((3,) in bitmap_set_1d)

    def test_add(self):
        bitmap_set = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        bitmap_set_1d = BitmapSet(size=4, elems=[0, 1, 2])
        # new element added set
        bitmap_set.add(_d)
        bitmap_set_1d.add((3,))
        # was already in set
        bitmap_set.add(_b)
        bitmap_set_1d.add(1)
        self.assertListEqual(list(bitmap_set), [_a, _b, _c, _d])
        self.assertListEqual(list(bitmap_set_1d), [0, 1, 2, 3])


if __name__ == '__main__':
    unittest.main()
