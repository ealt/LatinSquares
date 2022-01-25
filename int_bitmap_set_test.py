import unittest

from int_bitmap_set import IntBitmapSet


class IntBitmapSetTest(unittest.TestCase):

    maxDiff = None

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.addTypeEqualityFunc(IntBitmapSet, 'assertIntBitmapSetEqual')

    def assertIntBitmapSetEqual(self, bitmap_set1, bitmap_set2, msg=None):
        self.assertIsInstance(bitmap_set1, IntBitmapSet,
                              'First argument is not a IntBitmapSet')
        self.assertIsInstance(bitmap_set2, IntBitmapSet,
                              'Second argument is not a IntBitmapSet')
        self.assertSetEqual(bitmap_set1, bitmap_set2, msg)

    # ------- init methods -----------------------------------------------------

    def test_invalid_size(self):
        # size must by an integer...
        with self.assertRaises(TypeError):
            _ = IntBitmapSet(24.0)
        with self.assertRaises(TypeError):
            _ = IntBitmapSet('24')
        with self.assertRaises(TypeError):
            _ = IntBitmapSet((24,))
        # ...greater than zero
        with self.assertRaises(ValueError):
            _ = IntBitmapSet(0)

    def test_size_init(self):
        bitmap_set = IntBitmapSet(4)
        self.assertEqual(bitmap_set.size, 4)

    def test_empty_init(self):
        # default to empty set
        bitmap_set = IntBitmapSet(4)
        self.assertListEqual(list(bitmap_set), [])
        # value of 0 corresponds to empty set
        bitmap_set = IntBitmapSet(4, elems=0)
        self.assertListEqual(list(bitmap_set), [])
        # set explicity with an empty sequence
        bitmap_set = IntBitmapSet(4, elems=[])
        self.assertListEqual(list(bitmap_set), [])

    def test_invalid_elems(self):
        # elems must be an int or iterable
        with self.assertRaises(TypeError):
            _ = IntBitmapSet(4, elems=524546.0)

    def test_elems_sequence_init(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        self.assertListEqual(list(bitmap_set), [0, 1, 2])

    def test_elems_int_init(self):
        # bin(7) = '0111'
        # indicies of ones: 2, 1, 0
        bitmap_set = IntBitmapSet(4, elems=7)
        self.assertListEqual(list(bitmap_set), [0, 1, 2])

    def test_copy(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        other = bitmap_set.copy()
        self.assertTrue(bitmap_set == other)
        # copy is a distinct object
        self.assertTrue(id(bitmap_set) != id(other))
        bitmap_set.add(3)
        other.remove(2)
        self.assertTrue(bitmap_set != other)

    # ------- container methods ------------------------------------------------

    def test_len(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        self.assertEqual(len(bitmap_set), 3)

    def test_reversed(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        self.assertListEqual(list(reversed(bitmap_set)), [2, 1, 0])

    def test_repr(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        self.assertMultiLineEqual(repr(bitmap_set), '{0, 1, 2}')

    # ------- single elem methods ----------------------------------------------

    def test_invalid_elem(self):
        bitmap_set = IntBitmapSet(4)
        # Int is the only other acceptable type...
        with self.assertRaises(TypeError):
            1.0 in bitmap_set
        with self.assertRaises(TypeError):
            '1' in bitmap_set
        # ...value must be non-negative...
        with self.assertRaises(ValueError):
            -1 in bitmap_set
        # ...and less than the size
        with self.assertRaises(ValueError):
            4 in bitmap_set

    def test_contains(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        # does contain
        self.assertTrue(bitmap_set[1])
        self.assertTrue(1 in bitmap_set)
        # does not contain
        self.assertFalse(bitmap_set[3])
        self.assertFalse(3 in bitmap_set)

    def test_set_item(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        # `True` and `1` are equivalent in the bitmap
        # new element set to True
        bitmap_set[3] = 1
        # was already True in set
        bitmap_set[1] = True
        # `False` and `0` are equivalent in the bitmap
        # existing element set to False
        bitmap_set[2] = 0
        # was already False in set
        bitmap_set[2] = False
        self.assertListEqual(list(bitmap_set), [0, 1, 3])

    def test_add(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        # new element added set
        bitmap_set.add(3)
        # was already in set
        bitmap_set.add(1)
        self.assertListEqual(list(bitmap_set), [0, 1, 2, 3])

    def test_remove(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        # remove elements in set
        bitmap_set.remove(2)
        del bitmap_set[1]
        self.assertListEqual(list(bitmap_set), [0])
        # elements not in set
        with self.assertRaises(KeyError):
            bitmap_set.remove(3)
        with self.assertRaises(KeyError):
            del bitmap_set[3]

    def test_discard(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        # remove elements in set
        bitmap_set.discard(2)
        # elements not in set
        bitmap_set.discard(3)
        self.assertListEqual(list(bitmap_set), [0, 1])

    def test_pop(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        elem = bitmap_set.pop()
        self.assertEqual(elem, 0)
        self.assertListEqual(list(bitmap_set), [1, 2])

    def test_clear(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        bitmap_set.clear()
        self.assertListEqual(list(bitmap_set), [])

    # ------- other methods ----------------------------------------------------

    def test_invalid_other(self):
        # other must be a IntBitmapSet...
        bitmap_set = IntBitmapSet(4)
        other = set()
        with self.assertRaises(TypeError):
            bitmap_set.isdisjoint(other)
        # ...with the same size
        other = IntBitmapSet(6)
        with self.assertRaises(ValueError):
            bitmap_set.isdisjoint(other)

    def test_eq(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        # same sets
        other = IntBitmapSet(4, elems=[0, 1, 2])
        self.assertTrue(bitmap_set.equals(other))
        self.assertTrue(bitmap_set == other)
        self.assertFalse(bitmap_set != other)
        # same elements, but different size
        other = IntBitmapSet(6, elems=[0, 1, 2])
        self.assertFalse(bitmap_set.equals(other))
        self.assertFalse(bitmap_set == other)
        self.assertTrue(bitmap_set != other)
        # same size, but different elements
        other = IntBitmapSet(4, elems=[0, 3, 1])
        self.assertFalse(bitmap_set.equals(other))
        self.assertFalse(bitmap_set == other)
        self.assertTrue(bitmap_set != other)
        # different type
        other = set([0, 1, 2])
        self.assertFalse(bitmap_set.equals(other))
        self.assertFalse(bitmap_set == other)
        self.assertTrue(bitmap_set != other)

    def test_isdisjoint(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        # same sets
        other = IntBitmapSet(4, elems=[0, 1, 2])
        self.assertFalse(bitmap_set.isdisjoint(other))
        # different sets
        other = IntBitmapSet(4, elems=[0, 3, 1])
        self.assertTrue(bitmap_set.isdisjoint(other))

    def test_issubset(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        # proper subset
        other = IntBitmapSet(4, elems=[0, 1, 2, 3])
        self.assertTrue(bitmap_set.issubset(other))
        self.assertTrue(bitmap_set <= other)
        self.assertTrue(bitmap_set.ispropersubset(other))
        self.assertTrue(bitmap_set < other)
        # equal sets
        other = IntBitmapSet(4, elems=[0, 1, 2])
        self.assertTrue(bitmap_set.issubset(other))
        self.assertTrue(bitmap_set <= other)
        self.assertFalse(bitmap_set.ispropersubset(other))
        self.assertFalse(bitmap_set < other)
        # proper superset
        other = IntBitmapSet(4, elems=[0, 1])
        self.assertFalse(bitmap_set.issubset(other))
        self.assertFalse(bitmap_set <= other)
        self.assertFalse(bitmap_set.ispropersubset(other))
        self.assertFalse(bitmap_set < other)

    def test_issuperset(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        # proper subset
        other = IntBitmapSet(4, elems=[0, 1, 2, 3])
        self.assertFalse(bitmap_set.issuperset(other))
        self.assertFalse(bitmap_set >= other)
        self.assertFalse(bitmap_set.ispropersuperset(other))
        self.assertFalse(bitmap_set > other)
        # equal sets
        other = IntBitmapSet(4, elems=[0, 1, 2])
        self.assertTrue(bitmap_set.issuperset(other))
        self.assertTrue(bitmap_set >= other)
        self.assertFalse(bitmap_set.ispropersuperset(other))
        self.assertFalse(bitmap_set > other)
        # proper superset
        other = IntBitmapSet(4, elems=[0, 1])
        self.assertTrue(bitmap_set.issuperset(other))
        self.assertTrue(bitmap_set >= other)
        self.assertTrue(bitmap_set.ispropersuperset(other))
        self.assertTrue(bitmap_set > other)

    def test_union(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        other = IntBitmapSet(4, elems=[1, 2, 3])
        expected = IntBitmapSet(4, elems=[0, 1, 2, 3])
        self.assertIntBitmapSetEqual(bitmap_set.union(other), expected)
        self.assertIntBitmapSetEqual(bitmap_set | other, expected)
        self.assertIntBitmapSetEqual(other | bitmap_set, expected)

    def test_union_multiple_others(self):
        bitmap_set = IntBitmapSet(4, elems=[0])
        others = [
            IntBitmapSet(4, elems=[1]),
            IntBitmapSet(4, elems=[2]),
            IntBitmapSet(4, elems=[3]),
        ]
        expected = IntBitmapSet(4, elems=[0, 1, 2, 3])
        self.assertIntBitmapSetEqual(bitmap_set.union(*others), expected)

    def test_update(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        other = IntBitmapSet(4, elems=[1, 2, 3])
        expected = IntBitmapSet(4, elems=[0, 1, 2, 3])
        actual = bitmap_set.copy()
        actual.update(other)
        self.assertTrue(actual == expected)
        actual = bitmap_set.copy()
        actual |= other
        self.assertIntBitmapSetEqual(actual, expected)

    def test_update_multiple_others(self):
        bitmap_set = IntBitmapSet(4, elems=[0])
        others = [
            IntBitmapSet(4, elems=[1]),
            IntBitmapSet(4, elems=[2]),
            IntBitmapSet(4, elems=[3]),
        ]
        expected = IntBitmapSet(4, elems=[0, 1, 2, 3])
        bitmap_set.update(*others)
        self.assertIntBitmapSetEqual(bitmap_set, expected)

    def test_intersection(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        other = IntBitmapSet(4, elems=[1, 2, 3])
        expected = IntBitmapSet(4, elems=[1, 2])
        self.assertIntBitmapSetEqual(bitmap_set.intersection(other), expected)
        self.assertIntBitmapSetEqual(bitmap_set & other, expected)
        self.assertIntBitmapSetEqual(other & bitmap_set, expected)

    def test_intersection_multiple_others(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        others = [
            IntBitmapSet(4, elems=[0, 1]),
            IntBitmapSet(4, elems=[0, 2]),
            IntBitmapSet(4, elems=[0, 3]),
        ]
        expected = IntBitmapSet(4, elems=[0])
        self.assertIntBitmapSetEqual(bitmap_set.intersection(*others), expected)

    def test_intersection_update(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        other = IntBitmapSet(4, elems=[1, 2, 3])
        expected = IntBitmapSet(4, elems=[1, 2])
        actual = bitmap_set.copy()
        actual.intersection_update(other)
        self.assertTrue(actual == expected)
        actual = bitmap_set.copy()
        actual &= other
        self.assertIntBitmapSetEqual(actual, expected)

    def test_intersection_update_multiple_others(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        others = [
            IntBitmapSet(4, elems=[0, 1]),
            IntBitmapSet(4, elems=[0, 2]),
            IntBitmapSet(4, elems=[0, 3]),
        ]
        expected = IntBitmapSet(4, elems=[0])
        bitmap_set.intersection_update(*others)
        self.assertIntBitmapSetEqual(bitmap_set, expected)

    def test_difference(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        other = IntBitmapSet(4, elems=[1, 2, 3])
        expected = IntBitmapSet(4, elems=[0])
        self.assertIntBitmapSetEqual(bitmap_set.difference(other), expected)
        self.assertIntBitmapSetEqual(bitmap_set - other, expected)
        expected = IntBitmapSet(4, elems=[3])
        self.assertIntBitmapSetEqual(other - bitmap_set, expected)

    def test_difference_multiple_others(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2, 3])
        others = [
            IntBitmapSet(4, elems=[0]),
            IntBitmapSet(4, elems=[2]),
            IntBitmapSet(4, elems=[3]),
        ]
        expected = IntBitmapSet(4, elems=[1])
        self.assertIntBitmapSetEqual(bitmap_set.difference(*others), expected)

    def test_difference_update(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        other = IntBitmapSet(4, elems=[1, 2, 3])
        expected = IntBitmapSet(4, elems=[0])
        actual = bitmap_set.copy()
        actual.difference_update(other)
        self.assertIntBitmapSetEqual(actual, expected)
        actual = bitmap_set.copy()
        actual -= other
        self.assertIntBitmapSetEqual(actual, expected)

    def test_difference_update_multiple_others(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2, 3])
        others = [
            IntBitmapSet(4, elems=[0]),
            IntBitmapSet(4, elems=[2]),
            IntBitmapSet(4, elems=[3]),
        ]
        bitmap_set.difference_update(*others)
        expected = IntBitmapSet(4, elems=[1])
        self.assertIntBitmapSetEqual(bitmap_set, expected)

    def test_symmetric_difference(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        other = IntBitmapSet(4, elems=[1, 2, 3])
        expected = IntBitmapSet(4, elems=[0, 3])
        self.assertIntBitmapSetEqual(bitmap_set.symmetric_difference(other),
                                     expected)
        self.assertIntBitmapSetEqual(bitmap_set ^ other, expected)
        self.assertIntBitmapSetEqual(other ^ bitmap_set, expected)

    def test_symmetric_difference_update(self):
        bitmap_set = IntBitmapSet(4, elems=[0, 1, 2])
        other = IntBitmapSet(4, elems=[1, 2, 3])
        expected = IntBitmapSet(4, elems=[0, 3])
        actual = bitmap_set.copy()
        actual.symmetric_difference_update(other)
        self.assertIntBitmapSetEqual(actual, expected)
        actual = bitmap_set.copy()
        actual ^= other
        self.assertIntBitmapSetEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
