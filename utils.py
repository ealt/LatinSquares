from collections import namedtuple


Triple = namedtuple('Triple', ['r', 'c', 's'])


def to_orthogonal_array(latin_square):
    return [Triple(r=r, c=c, s=s) for r, row in enumerate(latin_square) for c, s in enumerate(row)]

def from_orthogonal_array(orthogonal_array):
    n = _get_n(orthogonal_array)
    latin_square = _get_empty_latin_square(n)
    for triple in orthogonal_array:
        latin_square[triple.r][triple.c] = triple.s
    return latin_square

def _get_n(orthogonal_array):
    return max(orthogonal_array, key=lambda triple: triple.r).r + 1

def _get_empty_latin_square(n):
    return [[None for _ in range(n)] for _ in range(n)]
