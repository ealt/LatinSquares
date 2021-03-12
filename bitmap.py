class Bitmap:

    def __init__(self, size=None, value=0, **kwargs):
        self._validate_value(value)
        self._value = value
        self._init_size(size)

    def __len__(self):
        return self._size

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._validate_value(value)
        self._value = value

    def get_bit(self, i):
        self._validate_i(i)
        return ((self.value >> i) & 1)

    def set_bit(self, i):
        self._validate_i(i)
        self.value |= (1 << i)

    def clear_bit(self, i):
        self._validate_i(i)
        ones = (1 << self._size) - 1
        self.value &= (ones ^ (1 << i))

    def flip_bit(self, i):
        self._validate_i(i)
        self.value ^= (1 << i)

    def update_bit(self, i, v):
        if v == 1:
            self.set_bit(i)
        elif v == 0:
            self.clear_bit(i)
        else:
            raise ValueError

    def _init_size(self, size):
        if size:
            self._validate_size(size)
            self._size = size
        else:
            self._size = len(bin(self.value)) - 2

    def _validate_value(self, value):
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

    def _validate_size(self, size):
        if isinstance(size, int):
            if size >= len(bin(self.value)) - 2:
                pass
            else:
                raise ValueError
        else:
            raise TypeError

    def _validate_i(self, i):
        if isinstance(i, int):
            if 0 <= i < self._size:
                pass
            else:
                raise ValueError
        else:
            raise TypeError
