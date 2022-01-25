from functools import reduce
from operator import mul
from typing import Optional

from bitmap_set import Elem, Elems
from nd_bitmap_set import NdBitmapSet


class PossibilitySet(NdBitmapSet):

    def __init__(self, bounds, elems: Optional[Elems] = None) -> None:
        elems = elems if elems else (1 << self._get_size(bounds)) - 1
        super().__init__(bounds, elems)
        self._init_masks()

    def elminate(self, elem: Elem) -> None:
        ones = (1 << self.size) - 1
        factor = 1
        for v, mask, n in zip(reversed(elem), reversed(self._masks),
                              reversed(self.shape)):
            self._bitmap.value &= ones ^ (mask << (v * factor))
            factor *= n

    def _init_masks(self) -> None:
        self._masks = [0 for _ in self.shape]
        one_factor = reduce(mul, self.shape, 1)
        zero_factor = 1
        repeat_factor = 1
        for i, n in enumerate(self.shape):
            one_factor //= self.shape[i]
            zero_factor = one_factor * (self.shape[i] - 1)
            mask = '0b' + ('0' * zero_factor + '1' * one_factor) * repeat_factor
            self._masks[i] = int(mask, 2)
            repeat_factor *= n
