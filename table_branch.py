from collections import defaultdict
from copy import deepcopy


class TableBranch:
    def __init__(self, n, vals_type=set):
        self._n = n
        get_new_cell = lambda i: vals_type([j for j in range(n) if j != i])
        get_new_row = lambda: [get_new_cell(i) for i in range(n)]
        self._values = [[i for i in range(n)]]
        self._values.extend([get_new_row() for _ in range(n-1)])
        self._liberties = defaultdict(set)
        self._liberties[n-1] = set([(row, col) for col in range(n) for row in range(1, n)])

    @property
    def values(self):
        return self._values

    def get_children(self):
        self._remove_empty_liberties()
        size = min(self._liberties.keys())
        row, col = self._liberties[size].pop()
        assert len(self._values[row][col]) == size
        children = []
        for val in self._values[row][col]:
            child = deepcopy(self)
            child._set_value(row, col, val)
            child._update_values()
            if child._is_viable():
                children.append(child)
        return children

    def _remove_empty_liberties(self):
        for k, v in self._liberties.items():
            if len(v) == 0:
                del self._liberties[k]

    def _update_values(self):
        while self._liberties[1]:
            row, col = self._liberties[1].pop()
            assert len(self._values[row][col]) == 1
            val = self._values[row][col].pop()
            self._set_value(row, col, val)
    
    def _set_value(self, row, col, val):
        size = len(self._values[row][col])
        self._liberties[size].discard((row, col))
        self._values[row][col] = val
        for i in range(self._n):
            self._remove_value(row, i, val)
            self._remove_value(i, col, val)

    def _remove_value(self, row, col, val):
        if hasattr(self._values[row][col], 'remove'):
            if val in self._values[row][col]:
                size = len(self._values[row][col])
                self._liberties[size].remove((row, col))
                self._values[row][col].remove(val)
                size = len(self._values[row][col])
                self._liberties[size].add((row, col))

    def _is_viable(self):
        return len(self._liberties[0]) == 0
