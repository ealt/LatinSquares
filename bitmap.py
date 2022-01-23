from typing import Optional, Union


class Bitmap:

    def __init__(self,
                 size: Optional[int] = None,
                 value: int = 0,
                 **kwargs) -> None:  # type: ignore
        self._validate_value(value)
        self._value = value
        self._init_size(size)

    def __len__(self) -> int:
        return self._size

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._validate_value(value)
        self._value = value

    def get_bit(self, i: int) -> int:
        self._validate_i(i)
        return self._get_bit(i)

    def _get_bit(self, i: int) -> int:
        return ((self.value >> i) & 1)

    def set_bit(self, i: int) -> None:
        self._validate_i(i)
        self._set_bit(i)

    def _set_bit(self, i: int) -> None:
        self.value |= (1 << i)

    def clear_bit(self, i: int) -> None:
        self._validate_i(i)
        self._clear_bit(i)

    def _clear_bit(self, i: int) -> None:
        ones = (1 << self._size) - 1
        self.value &= (ones ^ (1 << i))

    def flip_bit(self, i: int) -> None:
        self._validate_i(i)
        self._flip_bit(i)

    def _flip_bit(self, i: int) -> None:
        self.value ^= (1 << i)

    def update_bit(self, i: int, v: Union[bool, int]) -> None:
        self._update_bit(i, v)

    def _update_bit(self, i: int, v: Union[bool, int]) -> None:
        if v == 1:
            self.set_bit(i)
        elif v == 0:
            self.clear_bit(i)
        else:
            raise ValueError

    def _init_size(self, size: Optional[int]) -> None:
        if size:
            self._validate_size(size)
            self._size = size
        else:
            self._size = len(bin(self.value)) - 2

    def _validate_value(self, value: int) -> None:
        if isinstance(value, int):
            if value >= 0:
                if hasattr(self, '_size'):
                    if value < (1 << self._size):
                        pass
                    else:
                        raise ValueError
                else:
                    pass
            else:
                raise ValueError
        else:
            raise TypeError

    def _validate_size(self, size: int) -> None:
        if isinstance(size, int):
            if size >= len(bin(self.value)) - 2:
                pass
            else:
                raise ValueError
        else:
            raise TypeError

    def _validate_i(self, i: int) -> None:
        if isinstance(i, int):
            if 0 <= i < self._size:
                pass
            else:
                raise ValueError
        else:
            raise TypeError
