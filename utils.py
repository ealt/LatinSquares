from collections import namedtuple


Triple = namedtuple('Triple', ['r', 'c', 's'])


# ----- Orthogonal Array -------------------------------------------------------

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

# ----- Hashing ----------------------------------------------------------------

_hash_power = lambda r, c, n: (n ** 2 - 1) - (r * n + c)
_hash_triple = lambda triple, n: (triple.s) * n ** _hash_power(triple.r, triple.c, n)

def hash_latin_square(latin_square):
    return hash_orthognoal_array(to_orthogonal_array(latin_square))

def hash_orthognoal_array(orthogonal_array):
    n = _get_n(orthogonal_array)
    return sum(_hash_triple(triple, n) for triple in orthogonal_array)

def from_hash_val(hash_val, n):
    latin_square = _get_empty_latin_square(n)
    for r in reversed(range(n)):
        for c in reversed(range(n)):
            latin_square[r][c] = hash_val % n
            hash_val //= n
    return latin_square
