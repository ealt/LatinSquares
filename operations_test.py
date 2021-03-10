import unittest

from operations import *
from utils import Triple


class OperationsTest(unittest.TestCase):

    def test_rcs_permutation(self):
        orthogonal_array = [
            Triple(r=0,	c=0, s=0),
            Triple(r=0,	c=1, s=1),
            Triple(r=0,	c=2, s=2),
            Triple(r=1,	c=0, s=1),
            Triple(r=1,	c=1, s=2),
            Triple(r=1,	c=2, s=0),
            Triple(r=2,	c=0, s=2),
            Triple(r=2,	c=1, s=0),
            Triple(r=2,	c=2, s=1),
        ]
        actual = permute_orthogonal_array_triple(orthogonal_array, rcs)
        expected = orthogonal_array
        self.assertCountEqual(actual, expected)

    def test_rsc_permutation(self):
        orthogonal_array = [
            Triple(r=0,	c=0, s=0),
            Triple(r=0,	c=1, s=1),
            Triple(r=0,	c=2, s=2),
            Triple(r=1,	c=0, s=1),
            Triple(r=1,	c=1, s=2),
            Triple(r=1,	c=2, s=0),
            Triple(r=2,	c=0, s=2),
            Triple(r=2,	c=1, s=0),
            Triple(r=2,	c=2, s=1),
        ]
        actual = permute_orthogonal_array_triple(orthogonal_array, rsc)
        expected = [
            Triple(r=0,	s=0, c=0),
            Triple(r=0,	s=1, c=1),
            Triple(r=0,	s=2, c=2),
            Triple(r=1,	s=0, c=1),
            Triple(r=1,	s=1, c=2),
            Triple(r=1,	s=2, c=0),
            Triple(r=2,	s=0, c=2),
            Triple(r=2,	s=1, c=0),
            Triple(r=2,	s=2, c=1),
        ]
        self.assertCountEqual(actual, expected)

    def test_crs_permutation(self):
        orthogonal_array = [
            Triple(r=0,	c=0, s=0),
            Triple(r=0,	c=1, s=1),
            Triple(r=0,	c=2, s=2),
            Triple(r=1,	c=0, s=1),
            Triple(r=1,	c=1, s=2),
            Triple(r=1,	c=2, s=0),
            Triple(r=2,	c=0, s=2),
            Triple(r=2,	c=1, s=0),
            Triple(r=2,	c=2, s=1),
        ]
        actual = permute_orthogonal_array_triple(orthogonal_array, crs)
        expected = orthogonal_array
        self.assertCountEqual(actual, expected)

    def test_csr_permutation(self):
        orthogonal_array = [
            Triple(r=0,	c=0, s=0),
            Triple(r=0,	c=1, s=1),
            Triple(r=0,	c=2, s=2),
            Triple(r=1,	c=0, s=1),
            Triple(r=1,	c=1, s=2),
            Triple(r=1,	c=2, s=0),
            Triple(r=2,	c=0, s=2),
            Triple(r=2,	c=1, s=0),
            Triple(r=2,	c=2, s=1),
        ]
        actual = permute_orthogonal_array_triple(orthogonal_array, csr)
        expected = [
            Triple(s=0,	r=0, c=0),
            Triple(s=0,	r=1, c=1),
            Triple(s=0,	r=2, c=2),
            Triple(s=1,	r=0, c=1),
            Triple(s=1,	r=1, c=2),
            Triple(s=1,	r=2, c=0),
            Triple(s=2,	r=0, c=2),
            Triple(s=2,	r=1, c=0),
            Triple(s=2,	r=2, c=1),
        ]
        self.assertCountEqual(actual, expected)

    def test_src_permutation(self):
        orthogonal_array = [
            Triple(r=0,	c=0, s=0),
            Triple(r=0,	c=1, s=1),
            Triple(r=0,	c=2, s=2),
            Triple(r=1,	c=0, s=1),
            Triple(r=1,	c=1, s=2),
            Triple(r=1,	c=2, s=0),
            Triple(r=2,	c=0, s=2),
            Triple(r=2,	c=1, s=0),
            Triple(r=2,	c=2, s=1),
        ]
        actual = permute_orthogonal_array_triple(orthogonal_array, src)
        expected = [
            Triple(c=0,	s=0, r=0),
            Triple(c=0,	s=1, r=1),
            Triple(c=0,	s=2, r=2),
            Triple(c=1,	s=0, r=1),
            Triple(c=1,	s=1, r=2),
            Triple(c=1,	s=2, r=0),
            Triple(c=2,	s=0, r=2),
            Triple(c=2,	s=1, r=0),
            Triple(c=2,	s=2, r=1),
        ]
        self.assertCountEqual(actual, expected)

    def test_scr_permutation(self):
        orthogonal_array = [
            Triple(r=0,	c=0, s=0),
            Triple(r=0,	c=1, s=1),
            Triple(r=0,	c=2, s=2),
            Triple(r=1,	c=0, s=1),
            Triple(r=1,	c=1, s=2),
            Triple(r=1,	c=2, s=0),
            Triple(r=2,	c=0, s=2),
            Triple(r=2,	c=1, s=0),
            Triple(r=2,	c=2, s=1),
        ]
        actual = permute_orthogonal_array_triple(orthogonal_array, scr)
        expected = [
            Triple(s=0,	c=0, r=0),
            Triple(s=0,	c=1, r=1),
            Triple(s=0,	c=2, r=2),
            Triple(s=1,	c=0, r=1),
            Triple(s=1,	c=1, r=2),
            Triple(s=1,	c=2, r=0),
            Triple(s=2,	c=0, r=2),
            Triple(s=2,	c=1, r=0),
            Triple(s=2,	c=2, r=1),
        ]
        self.assertCountEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()