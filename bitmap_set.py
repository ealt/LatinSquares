from functools import reduce
from operator import mul
from typing import Iterable, Optional, Union

from bitmap import Bitmap


class BitmapSet:

    def __init__(self,
                 size: Optional[int] = None,
                 shape: Optional[tuple[int]] = None,
                 elems: Optional[Union[int, Iterable[int]]] = None,
                 **kwargs) -> None:
        self._init_size_shape(size, shape)
        self._init_bitmap(elems)

    def _init_bitmap(self, elems: Optional[Union[int, Iterable[int]]]) -> None:
        self._bitmap = Bitmap(size=self.size)
        if elems:
            self._init_elems(elems)

    def _init_size_shape(self,
                         size: Optional[int] = None,
                         shape: Optional[tuple[int]] = None) -> None:
        if not (size or shape):
            raise ValueError
        self._size = None
        self._shape = None
        if shape:
            self._validate_shape(shape)
            self._size = reduce(mul, shape)
            self._shape = shape
        if size:
            self._validate_size(size)
            self._size = size
            self._shape = self._shape if self._shape else (self.size,)

    def _validate_shape(self, shape: tuple[int]) -> None:
        if isinstance(shape, tuple):
            if all(isinstance(n, int) for n in shape):
                if all(n > 0 for n in shape):
                    pass
                else:
                    raise ValueError
            else:
                raise TypeError
        else:
            raise TypeError

    def _validate_size(self, size: int) -> None:
        if isinstance(size, int):
            if size > 0:
                if self.size:
                    if size == self.size:
                        pass
                    else:
                        raise ValueError
                else:
                    pass
            else:
                raise ValueError
        else:
            raise TypeError

    def _init_elems(self, elems: Union[int, Iterable[int]]) -> None:
        if isinstance(elems, int):
            self._bitmap.value = elems
        elif hasattr(elems, '__iter__'):
            for elem in elems:
                self.add(elem)
        else:
            raise TypeError

    @property
    def size(self) -> int:
        return self._size

    @property
    def shape(self) -> tuple[int]:
        return self._shape

    def _validate_elem(self, elem: Union[int, tuple[int]]) -> None:
        if isinstance(elem, tuple):
            if len(elem) == len(self.shape) and all(
                    isinstance(v, int) for v in elem):
                if all(0 <= v < n for v, n in zip(elem, self.shape)):
                    pass
                else:
                    raise ValueError
            else:
                raise TypeError
        elif isinstance(elem, int) and len(self.shape) == 1:
            if 0 <= elem < self.size:
                pass
            else:
                raise ValueError
        else:
            raise TypeError

    def _hash(self, elem: Union[int, tuple[int]]) -> int:
        if isinstance(elem, int):
            return elem
        else:
            i = 0
            factor = 1
            for v, n in zip(reversed(elem), reversed(self.shape)):
                i += v * factor
                factor *= n
            return i

    def add(self, elem: Union[int, tuple[int]]) -> None:
        self._validate_elem(elem)
        i = self._hash(elem)
        self._bitmap.set_bit(i)
