from collections import defaultdict
from copy import deepcopy


class LatinSquareSearchNode:
    def __init__(self, n, cell_container=set):
        self._n = n
        get_new_cell = lambda r, c: cell_container([s for s in range(n) if s != r and s != c])
        get_new_row = lambda r: [r] + [get_new_cell(r, c) for c in range(1, n)]
        self._symbols = [[i for i in range(n)]]
        self._symbols.extend([get_new_row(r) for r in range(1, n)])
        self._liberties = defaultdict(set)
        self._liberties[n-2] = set([(r, c) for c in range(1, n) for r in range(1, n)])
        for i in range(1, n):
            self._liberties[n-2].remove((i, i))
            self._liberties[n-1].add((i, i))

    @property
    def symbols(self):
        return self._symbols

    def is_terminal(self):
        self._remove_empty_liberties()
        return not self._liberties

    def get_children(self):
        self._remove_empty_liberties()
        size = min(self._liberties.keys())
        r, c = self._liberties[size].pop()
        assert len(self._symbols[r][c]) == size
        children = []
        for s in self._symbols[r][c]:
            child = deepcopy(self)
            child._set_symbol(r, c, s)
            child._update_symbols()
            if child._is_viable():
                children.append(child)
        return children

    def _remove_empty_liberties(self):
        for size in range(self._n):
            if len(self._liberties[size]) == 0:
                del self._liberties[size]

    def _update_symbols(self):
        while self._liberties[1]:
            r, c = self._liberties[1].pop()
            assert len(self._symbols[r][c]) == 1
            s = self._symbols[r][c].pop()
            self._set_symbol(r, c, s)
    
    def _set_symbol(self, r, c, s):
        size = len(self._symbols[r][c])
        self._liberties[size].discard((r, c))
        self._symbols[r][c] = s
        for i in range(self._n):
            self._remove_symbol(r, i, s)
            self._remove_symbol(i, c, s)

    def _remove_symbol(self, r, c, s):
        if hasattr(self._symbols[r][c], 'remove'):
            if s in self._symbols[r][c]:
                size = len(self._symbols[r][c])
                self._liberties[size].remove((r, c))
                self._symbols[r][c].remove(s)
                size = len(self._symbols[r][c])
                self._liberties[size].add((r, c))

    def _is_viable(self):
        return len(self._liberties[0]) == 0
