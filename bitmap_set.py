from abc import abstractclassmethod, abstractmethod
from collections import abc
from typing import Any, Iterable, Iterator, Optional, TypeVar, Union

from bitmap import Bitmap

Bounds = TypeVar('Bounds', int, tuple[int])
Elem = TypeVar('Elem', int, tuple[int])
Elems = TypeVar('Elems', int, Iterable[int], Iterable[tuple[int]])


class BitmapSet(abc.MutableSet):

    # ------- init methods -----------------------------------------------------

    def __init__(self, bounds: Bounds, elems: Optional[Elems] = None) -> None:
        self._validate_bounds(bounds)
        self._bounds = bounds
        self._size = self._get_size(bounds)
        self._init_bitmap(elems)

    @abstractclassmethod
    def _validate_bounds(cls, bounds: Bounds) -> None:
        pass

    @abstractmethod
    def _get_size(self, bounds: Bounds) -> int:
        pass

    def _init_bitmap(self, elems: Optional[Elems]) -> None:
        self._bitmap = Bitmap(size=self.size)
        if elems:
            self._init_elems(elems)

    def _init_elems(self, elems: Elems) -> None:
        if isinstance(elems, int):
            self._bitmap.value = elems
        elif hasattr(elems, '__iter__'):
            for elem in elems:
                self.add(elem)
        else:
            raise TypeError

    def copy(self):
        return self.__class__(self._bounds, elems=self._bitmap.value)

    # ------- container methods ------------------------------------------------

    @property
    def size(self) -> int:
        return self._size

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

    def __reduce__(self) -> tuple[type, tuple[Bounds, int]]:
        return (self.__class__, (self._bounds, self._bitmap.value))

    # ------- single elem methods ----------------------------------------------

    @abstractmethod
    def _validate_elem(self, elem: Elem) -> None:
        pass

    @abstractmethod
    def _hash(self, elem: Elem) -> int:
        pass

    @abstractmethod
    def _unhash(self, i: int) -> Elem:
        pass

    def __getitem__(self, elem: Elem) -> bool:
        return elem in self

    def __contains__(self, value: Elem) -> bool:
        self._validate_elem(value)
        i = self._hash(value)
        return bool(self._bitmap.get_bit(i))

    def __setitem__(self, elem: Elem, v: Union[bool, int]) -> None:
        self._validate_elem(elem)
        i = self._hash(elem)
        self._bitmap.update_bit(i, v)

    def add(self, value: Elem) -> None:
        self._validate_elem(value)
        i = self._hash(value)
        self._bitmap.set_bit(i)

    def __delitem__(self, elem: Elem) -> None:
        self.remove(elem)

    def remove(self, value: Elem) -> None:
        if value not in self:
            raise KeyError
        else:
            self.discard(value)

    def discard(self, value: Elem) -> None:
        self._validate_elem(value)
        i = self._hash(value)
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
        elif other.size != self.size:
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
        return self.__class__(self._bounds, elems=value)

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
        return self.__class__(self._bounds, elems=value)

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
        return self.__class__(self._bounds, elems=value)

    def __rsub__(self, other):
        self._validate_other(other)
        value = other._bitmap.value - (self._bitmap.value & other._bitmap.value)
        return self.__class__(self._bounds, elems=value)

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
        return self.__class__(self._bounds, elems=value)

    def symmetric_difference_update(self, other):
        self._validate_other(other)
        self._bitmap.value ^= other._bitmap.value

    def __ixor__(self, other):
        self.symmetric_difference_update(other)
        return self
