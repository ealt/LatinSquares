from functools import reduce
from operator import mul
from typing import Any, Iterable, Iterator, Optional, Union

from bitmap import Bitmap

Elem = Union[int, tuple[int]]
Elems = Union[int, Iterable[Elem]]


class BitmapSet:

    # ------- init methods -----------------------------------------------------

    def __init__(self,
                 size: Optional[int] = None,
                 shape: Optional[tuple[int]] = None,
                 elems: Optional[Elems] = None,
                 **kwargs) -> None:
        self._init_size_shape(size, shape)
        self._init_bitmap(elems)

    def _init_bitmap(self, elems: Optional[Elems]) -> None:
        self._bitmap = Bitmap(size=self.size)
        if elems:
            self._init_elems(elems)

    def _init_size_shape(self,
                         size: Optional[int] = None,
                         shape: Optional[tuple[int]] = None) -> None:
        self._size = 0
        if shape:
            self._validate_shape(shape)
            self._size = reduce(mul, shape)
            self._shape = shape
        if size:
            self._validate_size(size)
            self._size = size
            if not shape:
                self._shape = (self.size,)
        if not self.size:
            raise ValueError

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

    def _init_elems(self, elems: Elems) -> None:
        if isinstance(elems, int):
            self._bitmap.value = elems
        elif hasattr(elems, '__iter__'):
            for elem in elems:
                self.add(elem)
        else:
            raise TypeError

    def copy(self):
        return self.__class__(size=self.size,
                              shape=self.shape,
                              elems=self._bitmap.value)

    # ------- container methods ------------------------------------------------

    @property
    def size(self) -> int:
        return self._size

    @property
    def shape(self) -> tuple[int]:
        return self._shape

    def __len__(self) -> int:
        # return self._elems.bit_count()  # new in version 3.10
        return bin(self._bitmap.value).count('1')

    def __iter__(self) -> Iterator[Elem]:
        for i, bit in enumerate(reversed(bin(self._bitmap.value)[2:])):
            if bit == '1':
                yield self._unhash(i)

    def __reversed__(self) -> Iterator[Elem]:
        bin_value = bin(self._bitmap.value)[2:]
        for i, bit in zip(reversed(range(len(bin_value))), bin_value):
            if bit == '1':
                yield self._unhash(i)

    def __repr__(self) -> str:
        return '{' + ', '.join([str(elem) for elem in iter(self)]) + '}'

    def __reduce__(self) -> tuple[type, tuple[int, tuple[int], int]]:
        return (self.__class__, (self.size, self.shape, self._bitmap.value))

    # ------- single elem methods ----------------------------------------------

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
        elif isinstance(elem, int) and len(self.shape) == 1:
            if 0 <= elem < self.size:
                pass
            else:
                raise ValueError
        else:
            raise TypeError

    def _hash(self, elem: Elem) -> int:
        if isinstance(elem, int):
            return elem
        else:
            i = 0
            factor = 1
            for v, n in zip(reversed(elem), reversed(self.shape)):
                i += v * factor
                factor *= n
            return i

    def _unhash(self, i: int) -> Elem:
        if len(self.shape) == 1:
            return i
        else:
            elem = [0] * len(self.shape)
            for v_i, n in enumerate(reversed(self.shape)):
                elem[v_i] = i % n
                i //= n
            return tuple(reversed(elem))

    def __getitem__(self, elem: Elem) -> bool:
        return elem in self

    def __contains__(self, elem: Elem) -> bool:
        self._validate_elem(elem)
        i = self._hash(elem)
        return bool(self._bitmap.get_bit(i))

    def __setitem__(self, elem: Elem, v: Union[bool, int]) -> None:
        self._validate_elem(elem)
        i = self._hash(elem)
        self._bitmap.update_bit(i, v)

    def add(self, elem: Elem) -> None:
        self._validate_elem(elem)
        i = self._hash(elem)
        self._bitmap.set_bit(i)

    def __delitem__(self, elem: Elem) -> None:
        self.remove(elem)

    def remove(self, elem: Elem) -> None:
        if elem not in self:
            raise KeyError
        else:
            self.discard(elem)

    def discard(self, elem: Elem) -> None:
        self._validate_elem(elem)
        i = self._hash(elem)
        self._bitmap.clear_bit(i)

    def pop(self) -> Elem:
        elem = next(iter(self))
        i = self._hash(elem)
        self._bitmap.clear_bit(i)
        return elem

    def clear(self) -> None:
        self._bitmap.value = 0

    # ------- other methods ----------------------------------------------------

    def _validate_other(self, other: Any) -> None:
        if not isinstance(other, self.__class__):
            raise TypeError
        elif other.shape != self.shape:
            raise ValueError

    def __ne__(self, other):
        return not self.equals(other)

    def __eq__(self, other):
        return self.equals(other)

    def equals(self, other):
        try:
            self._validate_other(other)
            return self._bitmap.value == other._bitmap.value
        except TypeError:
            return False
        except ValueError:
            return False

    def isdisjoint(self, other):
        self._validate_other(other)
        return bool(self._bitmap.value ^ other._bitmap.value)

    def __le__(self, other):
        return self.issubset(other)

    def issubset(self, other):
        self._validate_other(other)
        return (self._bitmap.value -
                (self._bitmap.value & other._bitmap.value)) == 0

    def __lt__(self, other):
        return self.ispropersubset(other)

    def ispropersubset(self, other):
        return self <= other and self != other

    def __ge__(self, other):
        return self.issuperset(other)

    def issuperset(self, other):
        self._validate_other(other)
        return (other._bitmap.value -
                (self._bitmap.value & other._bitmap.value)) == 0

    def __gt__(self, other):
        return self.ispropersuperset(other)

    def ispropersuperset(self, other):
        return self >= other and self != other

    def __or__(self, other):
        return self.union(other)

    def __ror__(self, other):
        return self.union(other)

    def union(self, *others):
        value = self._bitmap.value
        for other in others:
            self._validate_other(other)
            value |= other._bitmap.value
        return self.__class__(size=self.size, shape=self.shape, elems=value)

    def update(self, *others):
        for other in others:
            self._validate_other(other)
            self._bitmap.value |= other._bitmap.value

    def __ior__(self, other):
        self.update(other)
        return self

    def __and__(self, other):
        return self.intersection(other)

    def __rand__(self, other):
        return self.intersection(other)

    def intersection(self, *others):
        value = self._bitmap.value
        for other in others:
            self._validate_other(other)
            value &= other._bitmap.value
        return self.__class__(size=self.size, shape=self.shape, elems=value)

    def intersection_update(self, *others):
        for other in others:
            self._validate_other(other)
            self._bitmap.value &= other._bitmap.value

    def __iand__(self, other):
        self.intersection_update(other)
        return self

    def __sub__(self, other):
        return self.difference(other)

    def difference(self, *others):
        value = self._bitmap.value
        for other in others:
            self._validate_other(other)
            value -= (value & other._bitmap.value)
        return self.__class__(size=self.size, shape=self.shape, elems=value)

    def __rsub__(self, other):
        self._validate_other(other)
        value = other._bitmap.value - (self._bitmap.value & other._bitmap.value)
        return self.__class__(size=self.size, shape=self.shape, elems=value)

    def difference_update(self, *others):
        for other in others:
            self._validate_other(other)
            self._bitmap.value -= (self._bitmap.value & other._bitmap.value)

    def __isub__(self, other):
        self.difference_update(other)
        return self

    def __xor__(self, other):
        return self.symmetric_difference(other)

    def __rxor__(self, other):
        return self.symmetric_difference(other)

    def symmetric_difference(self, other):
        self._validate_other(other)
        value = self._bitmap.value ^ other._bitmap.value
        return self.__class__(size=self.size, shape=self.shape, elems=value)

    def symmetric_difference_update(self, other):
        self._validate_other(other)
        self._bitmap.value ^= other._bitmap.value

    def __ixor__(self, other):
        self.symmetric_difference_update(other)
        return self
