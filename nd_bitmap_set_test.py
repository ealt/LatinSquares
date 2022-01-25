import unittest

from nd_bitmap_set import NdBitmapSet

_shape = (2, 3, 4)
_a = (0, 0, 1)  # elem 1
_b = (0, 2, 0)  # elem 8
_c = (1, 0, 2)  # elem 14
_d = (1, 1, 3)  # elem 19


class NdBitmapSetTest(unittest.TestCase):

    maxDiff = None

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.addTypeEqualityFunc(NdBitmapSet, 'assertNdBitmapSetEqual')

    def assertNdBitmapSetEqual(self, bitmap_set1, bitmap_set2, msg=None):
        self.assertIsInstance(bitmap_set1, NdBitmapSet,
                              'First argument is not a NdBitmapSet')
        self.assertIsInstance(bitmap_set2, NdBitmapSet,
                              'Second argument is not a NdBitmapSet')
        self.assertSetEqual(bitmap_set1, bitmap_set2, msg)

    # ------- init methods -----------------------------------------------------

    def test_invalid_shape(self):
        # shape must be a tuple...
        with self.assertRaises(TypeError):
            _ = NdBitmapSet(24)
        with self.assertRaises(TypeError):
            _ = NdBitmapSet([2, 3, 4])
        # ...whose elements are all integers...
        with self.assertRaises(TypeError):
            _ = NdBitmapSet((2.0, 3.0, 4.0))
        with self.assertRaises(TypeError):
            _ = NdBitmapSet(('2', '3', '4'))
        with self.assertRaises(TypeError):
            _ = NdBitmapSet(((2, 3, 4),))
        # ...with positive values
        with self.assertRaises(ValueError):
            _ = NdBitmapSet((2, 3, 4, 0))

    def test_shape_init(self):
        bitmap_set = NdBitmapSet((2, 3, 4))
        self.assertEqual(bitmap_set.size, 24)
        self.assertTupleEqual(bitmap_set.shape, (2, 3, 4))

    def test_empty_init(self):
        # default to empty set
        bitmap_set = NdBitmapSet(_shape)
        self.assertListEqual(list(bitmap_set), [])
        # value of 0 corresponds to empty set
        bitmap_set = NdBitmapSet(_shape, elems=0)
        self.assertListEqual(list(bitmap_set), [])
        # set explicity with an empty sequence
        bitmap_set = NdBitmapSet(_shape, elems=[])
        self.assertListEqual(list(bitmap_set), [])

    def test_invalid_elems(self):
        # elems must be an int or iterable
        with self.assertRaises(TypeError):
            _ = NdBitmapSet(_shape, elems=524546.0)

    def test_elems_sequence_init(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        self.assertListEqual(list(bitmap_set), [_a, _b, _c])

    def test_elems_int_init(self):
        # bin(16642) = '000000000100000100000010'
        # indicies of ones: ^19  ^14   ^8     ^1
        bitmap_set = NdBitmapSet(_shape, elems=16642)
        self.assertListEqual(list(bitmap_set), [_a, _b, _c])

    def test_copy(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        other = bitmap_set.copy()
        self.assertTrue(bitmap_set == other)
        # copy is a distinct object
        self.assertTrue(id(bitmap_set) != id(other))
        bitmap_set.add(_d)
        other.remove(_c)
        self.assertTrue(bitmap_set != other)

    # ------- container methods ------------------------------------------------

    def test_len(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        self.assertEqual(len(bitmap_set), 3)

    def test_reversed(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        self.assertListEqual(list(reversed(bitmap_set)), [_c, _b, _a])

    def test_repr(self):
        bitmap_set = NdBitmapSet(_shape,
                                 elems=[(0, 0, 1), (0, 2, 0), (1, 1, 3)])
        self.assertMultiLineEqual(repr(bitmap_set),
                                  '{(0, 0, 1), (0, 2, 0), (1, 1, 3)}')

    # ------- single elem methods ----------------------------------------------

    def test_invalid_elem(self):
        bitmap_set = NdBitmapSet((2, 3, 4))
        # elem must be a tuple...
        with self.assertRaises(TypeError):
            1 in bitmap_set
        with self.assertRaises(TypeError):
            [0, 0, 1] in bitmap_set
        # ...tuple elements must have the same len as shape...
        with self.assertRaises(TypeError):
            (0, 1) in bitmap_set
        # ...and tuple values must all be integers...
        with self.assertRaises(TypeError):
            ('0', '0', '1') in bitmap_set
        with self.assertRaises(TypeError):
            (1.0,) in bitmap_set
        # ...that are non-negative...
        with self.assertRaises(ValueError):
            (0, 0, -1) in bitmap_set
        # ...and less than the corresponding dimension length in shape
        with self.assertRaises(ValueError):
            (3, 0, 1) in bitmap_set

    def test_contains(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        # does contain
        self.assertTrue(bitmap_set[_b])
        self.assertTrue(_b in bitmap_set)
        # does not contain
        self.assertFalse(bitmap_set[_d])
        self.assertFalse(_d in bitmap_set)

    def test_set_item(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        # `True` and `1` are equivalent in the bitmap
        # new element set to True
        bitmap_set[_d] = True
        # was already True in set
        bitmap_set[_b] = 1
        # `False` and `0` are equivalent in the bitmap
        # existing element set to False
        bitmap_set[_c] = False
        # was already False in set
        bitmap_set[_c] = 0
        self.assertListEqual(list(bitmap_set), [_a, _b, _d])

    def test_add(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        # new element added set
        bitmap_set.add(_d)
        # was already in set
        bitmap_set.add(_b)
        self.assertListEqual(list(bitmap_set), [_a, _b, _c, _d])

    def test_remove(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        # remove elements in set
        bitmap_set.remove(_c)
        del bitmap_set[_b]
        self.assertListEqual(list(bitmap_set), [_a])
        # elements not in set
        with self.assertRaises(KeyError):
            bitmap_set.remove(_d)
        with self.assertRaises(KeyError):
            del bitmap_set[_d]

    def test_discard(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        # remove elements in set
        bitmap_set.discard(_c)
        # elements not in set
        bitmap_set.discard(_d)
        self.assertListEqual(list(bitmap_set), [_a, _b])

    def test_pop(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        elem = bitmap_set.pop()
        self.assertTupleEqual(elem, _a)
        self.assertListEqual(list(bitmap_set), [_b, _c])

    def test_clear(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        bitmap_set.clear()
        self.assertListEqual(list(bitmap_set), [])

    # ------- other methods ----------------------------------------------------

    def test_invalid_other(self):
        # other must be a NdBitmapSet...
        bitmap_set = NdBitmapSet((2, 3, 4))
        other = set()
        with self.assertRaises(TypeError):
            bitmap_set.isdisjoint(other)
        # ...with the same shape
        other = NdBitmapSet((4, 3, 2))
        with self.assertRaises(ValueError):
            bitmap_set.isdisjoint(other)

    def test_eq(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        # same sets
        other = NdBitmapSet(_shape, elems=[_a, _b, _c])
        self.assertTrue(bitmap_set.equals(other))
        self.assertTrue(bitmap_set == other)
        self.assertFalse(bitmap_set != other)
        # same elements, but different shape
        other = NdBitmapSet((3, 4, 5), elems=[_a, _b, _c])
        self.assertFalse(bitmap_set.equals(other))
        self.assertFalse(bitmap_set == other)
        self.assertTrue(bitmap_set != other)
        # same shape, but different elements
        other = NdBitmapSet(_shape, elems=[_a, _d, _b])
        self.assertFalse(bitmap_set.equals(other))
        self.assertFalse(bitmap_set == other)
        self.assertTrue(bitmap_set != other)
        # different type
        other = set([_a, _b, _c])
        self.assertFalse(bitmap_set.equals(other))
        self.assertFalse(bitmap_set == other)
        self.assertTrue(bitmap_set != other)

    def test_isdisjoint(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        # same sets
        other = NdBitmapSet(_shape, elems=[_a, _b, _c])
        self.assertFalse(bitmap_set.isdisjoint(other))
        # different sets
        other = NdBitmapSet(_shape, elems=[_a, _d, _b])
        self.assertTrue(bitmap_set.isdisjoint(other))

    def test_issubset(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        # proper subset
        other = NdBitmapSet(_shape, elems=[_a, _b, _c, _d])
        self.assertTrue(bitmap_set.issubset(other))
        self.assertTrue(bitmap_set <= other)
        self.assertTrue(bitmap_set.ispropersubset(other))
        self.assertTrue(bitmap_set < other)
        # equal sets
        other = NdBitmapSet(_shape, elems=[_a, _b, _c])
        self.assertTrue(bitmap_set.issubset(other))
        self.assertTrue(bitmap_set <= other)
        self.assertFalse(bitmap_set.ispropersubset(other))
        self.assertFalse(bitmap_set < other)
        # proper superset
        other = NdBitmapSet(_shape, elems=[_a, _b])
        self.assertFalse(bitmap_set.issubset(other))
        self.assertFalse(bitmap_set <= other)
        self.assertFalse(bitmap_set.ispropersubset(other))
        self.assertFalse(bitmap_set < other)

    def test_issuperset(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        # proper subset
        other = NdBitmapSet(_shape, elems=[_a, _b, _c, _d])
        self.assertFalse(bitmap_set.issuperset(other))
        self.assertFalse(bitmap_set >= other)
        self.assertFalse(bitmap_set.ispropersuperset(other))
        self.assertFalse(bitmap_set > other)
        # equal sets
        other = NdBitmapSet(_shape, elems=[_a, _b, _c])
        self.assertTrue(bitmap_set.issuperset(other))
        self.assertTrue(bitmap_set >= other)
        self.assertFalse(bitmap_set.ispropersuperset(other))
        self.assertFalse(bitmap_set > other)
        # proper superset
        other = NdBitmapSet(_shape, elems=[_a, _b])
        self.assertTrue(bitmap_set.issuperset(other))
        self.assertTrue(bitmap_set >= other)
        self.assertTrue(bitmap_set.ispropersuperset(other))
        self.assertTrue(bitmap_set > other)

    def test_union(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        other = NdBitmapSet(_shape, elems=[_b, _c, _d])
        expected = NdBitmapSet(_shape, elems=[_a, _b, _c, _d])
        self.assertNdBitmapSetEqual(bitmap_set.union(other), expected)
        self.assertNdBitmapSetEqual(bitmap_set | other, expected)
        self.assertNdBitmapSetEqual(other | bitmap_set, expected)

    def test_union_multiple_others(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a])
        others = [
            NdBitmapSet(_shape, elems=[_b]),
            NdBitmapSet(_shape, elems=[_c]),
            NdBitmapSet(_shape, elems=[_d]),
        ]
        expected = NdBitmapSet(_shape, elems=[_a, _b, _c, _d])
        self.assertNdBitmapSetEqual(bitmap_set.union(*others), expected)

    def test_update(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        other = NdBitmapSet(_shape, elems=[_b, _c, _d])
        expected = NdBitmapSet(_shape, elems=[_a, _b, _c, _d])
        actual = bitmap_set.copy()
        actual.update(other)
        self.assertTrue(actual == expected)
        actual = bitmap_set.copy()
        actual |= other
        self.assertNdBitmapSetEqual(actual, expected)

    def test_update_multiple_others(self):
        bitmap_set = NdBitmapSet(_shape, elems=[
            _a,
        ])
        others = [
            NdBitmapSet(_shape, elems=[_b]),
            NdBitmapSet(_shape, elems=[_c]),
            NdBitmapSet(_shape, elems=[_d]),
        ]
        bitmap_set.update(*others)
        expected = NdBitmapSet(_shape, elems=[_a, _b, _c, _d])
        self.assertNdBitmapSetEqual(bitmap_set, expected)

    def test_intersection(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        other = NdBitmapSet(_shape, elems=[_b, _c, _d])
        expected = NdBitmapSet(_shape, elems=[_b, _c])
        self.assertNdBitmapSetEqual(bitmap_set.intersection(other), expected)
        self.assertNdBitmapSetEqual(bitmap_set & other, expected)
        self.assertNdBitmapSetEqual(other & bitmap_set, expected)

    def test_intersection_multiple_others(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        others = [
            NdBitmapSet(_shape, elems=[_a, _b]),
            NdBitmapSet(_shape, elems=[_a, _c]),
            NdBitmapSet(_shape, elems=[_a, _d]),
        ]
        expected = NdBitmapSet(_shape, elems=[_a])
        self.assertNdBitmapSetEqual(bitmap_set.intersection(*others), expected)

    def test_intersection_update(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        other = NdBitmapSet(_shape, elems=[_b, _c, _d])
        expected = NdBitmapSet(_shape, elems=[_b, _c])
        actual = bitmap_set.copy()
        actual.intersection_update(other)
        self.assertNdBitmapSetEqual(actual, expected)
        actual = bitmap_set.copy()
        actual &= other
        self.assertNdBitmapSetEqual(actual, expected)

    def test_intersection_update_multiple_others(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        others = [
            NdBitmapSet(_shape, elems=[_a, _b]),
            NdBitmapSet(_shape, elems=[_a, _c]),
            NdBitmapSet(_shape, elems=[_a, _d]),
        ]
        bitmap_set.intersection_update(*others)
        expected = NdBitmapSet(_shape, elems=[_a])
        self.assertNdBitmapSetEqual(bitmap_set, expected)

    def test_difference(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        other = NdBitmapSet(_shape, elems=[_b, _c, _d])
        expected = NdBitmapSet(_shape, elems=[_a])
        self.assertNdBitmapSetEqual(bitmap_set.difference(other), expected)
        self.assertNdBitmapSetEqual(bitmap_set - other, expected)
        expected = NdBitmapSet(_shape, elems=[_d])
        self.assertNdBitmapSetEqual(other - bitmap_set, expected)

    def test_difference_multiple_others(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c, _d])
        others = [
            NdBitmapSet(_shape, elems=[_a]),
            NdBitmapSet(_shape, elems=[_c]),
            NdBitmapSet(_shape, elems=[_d]),
        ]
        expected = NdBitmapSet(_shape, elems=[_b])
        self.assertNdBitmapSetEqual(bitmap_set.difference(*others), expected)

    def test_difference_update(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        other = NdBitmapSet(_shape, elems=[_b, _c, _d])
        expected = NdBitmapSet(_shape, elems=[_a])
        actual = bitmap_set.copy()
        actual.difference_update(other)
        self.assertNdBitmapSetEqual(actual, expected)
        actual = bitmap_set.copy()
        actual -= other
        self.assertNdBitmapSetEqual(actual, expected)

    def test_difference_update_multiple_others(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c, _d])
        others = [
            NdBitmapSet(_shape, elems=[_a]),
            NdBitmapSet(_shape, elems=[_c]),
            NdBitmapSet(_shape, elems=[_d]),
        ]
        bitmap_set.difference_update(*others)
        expected = NdBitmapSet(_shape, elems=[_b])
        self.assertNdBitmapSetEqual(bitmap_set, expected)

    def test_symmetric_difference(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        other = NdBitmapSet(_shape, elems=[_b, _c, _d])
        expected = NdBitmapSet(_shape, elems=[_a, _d])
        self.assertNdBitmapSetEqual(bitmap_set.symmetric_difference(other),
                                    expected)
        self.assertNdBitmapSetEqual(bitmap_set ^ other, expected)
        self.assertNdBitmapSetEqual(other ^ bitmap_set, expected)

    def test_symmetric_difference_update(self):
        bitmap_set = NdBitmapSet(_shape, elems=[_a, _b, _c])
        other = NdBitmapSet(_shape, elems=[_b, _c, _d])
        expected = NdBitmapSet(_shape, elems=[_a, _d])
        actual = bitmap_set.copy()
        actual.symmetric_difference_update(other)
        self.assertNdBitmapSetEqual(actual, expected)
        actual = bitmap_set.copy()
        actual ^= other
        self.assertNdBitmapSetEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
