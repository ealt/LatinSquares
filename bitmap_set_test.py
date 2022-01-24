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
        # bin(16642) = '000000000100000100000010'
        # indicies of ones: ^19  ^14   ^8     ^1
        bitmap_set = BitmapSet(shape=_shape, elems=16642)
        self.assertListEqual(list(bitmap_set), [_a, _b, _c])
        # bin(7) = '0111'
        # indicies of ones: 2, 1, 0
        bitmap_set = BitmapSet(size=4, elems=7)
        self.assertListEqual(list(bitmap_set), [0, 1, 2])

    # ------- container methods ------------------------------------------------

    def test_len(self):
        bitmap_set = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        self.assertEqual(len(bitmap_set), 3)
        bitmap_set_1d = BitmapSet(size=4, elems=[0, 1, 2])
        self.assertEqual(len(bitmap_set_1d), 3)

    def test_reversed(self):
        bitmap_set = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        self.assertListEqual(list(reversed(bitmap_set)), [_c, _b, _a])
        bitmap_set_1d = BitmapSet(size=4, elems=[0, 1, 2])
        self.assertListEqual(list(reversed(bitmap_set_1d)), [2, 1, 0])

    def test_repr(self):
        bitmap_set = BitmapSet(shape=_shape,
                               elems=[(0, 0, 1), (0, 2, 0), (1, 1, 3)])
        self.assertMultiLineEqual(repr(bitmap_set),
                                  '{(0, 0, 1), (0, 2, 0), (1, 1, 3)}')
        bitmap_set_1d = BitmapSet(size=4, elems=[0, 1, 2])
        self.assertMultiLineEqual(repr(bitmap_set_1d), '{0, 1, 2}')

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
        self.assertTrue(bitmap_set[_b])
        self.assertTrue(bitmap_set_1d[(1,)])
        self.assertTrue(_b in bitmap_set)
        self.assertTrue(1 in bitmap_set_1d)
        # does not contain
        self.assertFalse(bitmap_set[_d])
        self.assertFalse(bitmap_set_1d[3])
        self.assertFalse(_d in bitmap_set)
        self.assertFalse((3,) in bitmap_set_1d)

    def test_set_item(self):
        bitmap_set = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        bitmap_set_1d = BitmapSet(size=4, elems=[0, 1, 2])
        # `True` and `1` are equivalent in the bitmap
        # new element set to True
        bitmap_set[_d] = True
        bitmap_set_1d[(3,)] = 1
        # was already True in set
        bitmap_set[_b] = 1
        bitmap_set_1d[1] = True
        # `False` and `0` are equivalent in the bitmap
        # existing element set to False
        bitmap_set[_c] = False
        bitmap_set_1d[(2,)] = 0
        # was already False in set
        bitmap_set[_c] = 0
        bitmap_set_1d[2] = False
        self.assertListEqual(list(bitmap_set), [_a, _b, _d])
        self.assertListEqual(list(bitmap_set_1d), [0, 1, 3])

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

    def test_remove(self):
        bitmap_set = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        bitmap_set_1d = BitmapSet(size=4, elems=[0, 1, 2])
        # remove elements in set
        bitmap_set.remove(_c)
        bitmap_set_1d.remove(2)
        del bitmap_set[_b]
        del bitmap_set_1d[(1,)]
        self.assertListEqual(list(bitmap_set), [_a])
        self.assertListEqual(list(bitmap_set_1d), [0])
        # elements not in set
        with self.assertRaises(KeyError):
            bitmap_set.remove(_d)
        with self.assertRaises(KeyError):
            bitmap_set_1d.remove((3,))
        with self.assertRaises(KeyError):
            del bitmap_set[_d]
        with self.assertRaises(KeyError):
            del bitmap_set_1d[3]

    def test_discard(self):
        bitmap_set = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        bitmap_set_1d = BitmapSet(size=4, elems=[0, 1, 2])
        # remove elements in set
        bitmap_set.discard(_c)
        bitmap_set_1d.discard((2,))
        # elements not in set
        bitmap_set.discard(_d)
        bitmap_set_1d.discard(3)
        self.assertListEqual(list(bitmap_set), [_a, _b])
        self.assertListEqual(list(bitmap_set_1d), [0, 1])

    def test_pop(self):
        bitmap_set = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        bitmap_set_1d = BitmapSet(size=4, elems=[0, 1, 2])
        elem = bitmap_set.pop()
        elem_1d = bitmap_set_1d.pop()
        self.assertTupleEqual(elem, _a)
        self.assertEqual(elem_1d, 0)
        self.assertListEqual(list(bitmap_set), [_b, _c])
        self.assertListEqual(list(bitmap_set_1d), [1, 2])

    def test_clear(self):
        bitmap_set = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        bitmap_set_1d = BitmapSet(size=4, elems=[0, 1, 2])
        bitmap_set.clear()
        bitmap_set_1d.clear()
        self.assertListEqual(list(bitmap_set), [])
        self.assertListEqual(list(bitmap_set_1d), [])

    # ------- other methods ----------------------------------------------------

    def test_invalid_other(self):
        # other must be a BitmapSet...
        bitmap_set_1d = BitmapSet(size=4)
        other = set()
        with self.assertRaises(TypeError):
            bitmap_set_1d.isdisjoint(other)
        # ...with the same shape
        bitmap_set = BitmapSet(shape=(2, 3, 4))
        other = BitmapSet(shape=(4, 3, 2))
        with self.assertRaises(ValueError):
            bitmap_set.isdisjoint(other)

    def test_eq(self):
        bitmap_set = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        bitmap_set_1d = BitmapSet(size=4, elems=[0, 1, 2])
        # same sets
        other = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        self.assertTrue(bitmap_set.equals(other))
        self.assertTrue(bitmap_set == other)
        self.assertFalse(bitmap_set != other)
        other_1d = BitmapSet(size=4, elems=[0, 1, 2])
        self.assertTrue(bitmap_set_1d.equals(other_1d))
        self.assertTrue(bitmap_set_1d == other_1d)
        self.assertFalse(bitmap_set_1d != other_1d)
        # same elements, but different shape
        other = BitmapSet(shape=(3, 4, 5), elems=[_a, _b, _c])
        self.assertFalse(bitmap_set.equals(other))
        self.assertFalse(bitmap_set == other)
        self.assertTrue(bitmap_set != other)
        other_1d = BitmapSet(shape=(2, 2), elems=[(0, 0), (0, 1), (1, 0)])
        self.assertFalse(bitmap_set_1d.equals(other_1d))
        self.assertFalse(bitmap_set_1d == other_1d)
        self.assertTrue(bitmap_set_1d != other_1d)
        # same shape, but different elements
        other = BitmapSet(shape=_shape, elems=[_a, _d, _b])
        self.assertFalse(bitmap_set.equals(other))
        self.assertFalse(bitmap_set == other)
        self.assertTrue(bitmap_set != other)
        other_1d = BitmapSet(size=4, elems=[0, 3, 1])
        self.assertFalse(bitmap_set_1d.equals(other_1d))
        self.assertFalse(bitmap_set_1d == other_1d)
        self.assertTrue(bitmap_set_1d != other_1d)
        # different type
        other = set([_a, _b, _c])
        self.assertFalse(bitmap_set.equals(other))  # type: ignore
        self.assertFalse(bitmap_set == other)  # type: ignore
        self.assertTrue(bitmap_set != other)  # type: ignore
        other_1d = set([0, 1, 2])
        self.assertFalse(bitmap_set_1d.equals(other_1d))
        self.assertFalse(bitmap_set_1d == other_1d)
        self.assertTrue(bitmap_set_1d != other_1d)

    def test_isdisjoint(self):
        bitmap_set = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        bitmap_set_1d = BitmapSet(size=4, elems=[0, 1, 2])
        # same sets
        other = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        self.assertFalse(bitmap_set.isdisjoint(other))
        other_1d = BitmapSet(size=4, elems=[0, 1, 2])
        self.assertFalse(bitmap_set_1d.isdisjoint(other_1d))
        # different sets
        other = BitmapSet(shape=_shape, elems=[_a, _d, _b])
        self.assertTrue(bitmap_set.isdisjoint(other))
        other_1d = BitmapSet(size=4, elems=[0, 3, 1])
        self.assertTrue(bitmap_set_1d.isdisjoint(other_1d))

    def test_issubset(self):
        bitmap_set = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        bitmap_set_1d = BitmapSet(size=4, elems=[0, 1, 2])
        # proper subset
        other = BitmapSet(shape=_shape, elems=[_a, _b, _c, _d])
        self.assertTrue(bitmap_set.issubset(other))
        self.assertTrue(bitmap_set <= other)
        self.assertTrue(bitmap_set.ispropersubset(other))
        self.assertTrue(bitmap_set < other)
        other_1d = BitmapSet(size=4, elems=[0, 1, 2, 3])
        self.assertTrue(bitmap_set_1d.issubset(other_1d))
        self.assertTrue(bitmap_set_1d <= other_1d)
        self.assertTrue(bitmap_set_1d.ispropersubset(other_1d))
        self.assertTrue(bitmap_set_1d < other_1d)
        # equal sets
        other = BitmapSet(shape=_shape, elems=[_a, _b, _c])
        self.assertTrue(bitmap_set.issubset(other))
        self.assertTrue(bitmap_set <= other)
        self.assertFalse(bitmap_set.ispropersubset(other))
        self.assertFalse(bitmap_set < other)
        other_1d = BitmapSet(size=4, elems=[0, 1, 2])
        self.assertTrue(bitmap_set_1d.issubset(other_1d))
        self.assertTrue(bitmap_set_1d <= other_1d)
        self.assertFalse(bitmap_set_1d.ispropersubset(other_1d))
        self.assertFalse(bitmap_set_1d < other_1d)
        # proper superset
        other = BitmapSet(shape=_shape, elems=[_a, _b])
        self.assertFalse(bitmap_set.issubset(other))
        self.assertFalse(bitmap_set <= other)
        self.assertFalse(bitmap_set.ispropersubset(other))
        self.assertFalse(bitmap_set < other)
        other_1d = BitmapSet(size=4, elems=[0, 1])
        self.assertFalse(bitmap_set_1d.issubset(other_1d))
        self.assertFalse(bitmap_set_1d <= other_1d)
        self.assertFalse(bitmap_set_1d.ispropersubset(other_1d))
        self.assertFalse(bitmap_set_1d < other_1d)


if __name__ == '__main__':
    unittest.main()
