from functools import reduce
from operator import mul
from typing import Optional

from bitmap_set import BitmapSet, Bounds, Elem, Elems


class NdBitmapSet(BitmapSet):

    def __init__(self, bounds: Bounds, elems: Optional[Elems] = None) -> None:
        self._shape = bounds
        super().__init__(bounds, elems)

    @classmethod
    def _validate_bounds(cls, bounds: Bounds) -> None:
        if isinstance(bounds, tuple):
            if all(isinstance(n, int) for n in bounds):
                if all(n > 0 for n in bounds):
                    pass
                else:
                    raise ValueError
            else:
                raise TypeError
        else:
            raise TypeError

    def _get_size(self, bounds: Bounds) -> int:
        return reduce(mul, bounds)

    @property
    def shape(self) -> tuple[int]:
        return self._shape

    def _validate_elem(self, elem: Elem) -> None:
        if isinstance(elem, tuple):
            if len(elem) == len(self.shape) and all(
                    isinstance(v, int) for v in elem):
                if all(0 <= v < n for v, n in zip(elem, self.shape)):
                    pass
                else:
                    raise ValueError
            else:
                raise TypeError
        else:
            raise TypeError

    def _hash(self, elem: Elem) -> int:
        i = 0
        factor = 1
        for v, n in zip(reversed(elem), reversed(self.shape)):
            i += v * factor
            factor *= n
        return i

    def _unhash(self, i: int) -> Elem:
        elem = [0 for _ in self.shape]
        for v_i, n in enumerate(reversed(self.shape)):
            elem[v_i] = i % n
            i //= n
        return tuple(reversed(elem))

    def _validate_other(self, other):
        super()._validate_other(other)
        if other.shape != self.shape:
            raise ValueError
