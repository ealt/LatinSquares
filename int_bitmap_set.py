from bitmap_set import BitmapSet, Bounds, Elem


class IntBitmapSet(BitmapSet):

    @classmethod
    def _validate_bounds(cls, bounds: Bounds) -> None:
        if isinstance(bounds, int):
            if bounds > 0:
                pass
            else:
                raise ValueError
        else:
            raise TypeError

    def _get_size(self, bounds: Bounds) -> int:
        return bounds

    def _validate_elem(self, elem: Elem) -> None:
        if isinstance(elem, int):
            if 0 <= elem < self.size:
                pass
            else:
                raise ValueError
        else:
            raise TypeError

    def _hash(self, elem: Elem) -> int:
        return elem

    def _unhash(self, i: int) -> Elem:
        return i
