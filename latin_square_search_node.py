from collections import defaultdict
from copy import deepcopy
from typing import Callable, DefaultDict, Union


class LatinSquareSearchNode:

    def __init__(self, n: int, cell_container: type = set) -> None:
        self._n = n
        get_new_cell: Callable[[int, int],
                               set[int]] = lambda r, c: cell_container(
                                   [s for s in range(n) if s != r and s != c])
        get_new_row: Callable[[int], list[Union[
            int, set[int]]]] = lambda r: [  # type: ignore
                r
            ] + [get_new_cell(r, c) for c in range(1, n)]  # type: ignore
        self._symbols: list[list[Union[int,
                                       set[int]]]] = [[i for i in range(n)]]
        self._symbols.extend([get_new_row(r) for r in range(1, n)
                             ])  # type: ignore
        self._liberties: DefaultDict[int, set[tuple[int,
                                                    int]]] = defaultdict(set)
        self._liberties[n - 2] = set([
            (r, c) for c in range(1, n) for r in range(1, n)
        ])
        for i in range(1, n):
            self._liberties[n - 2].remove((i, i))
            self._liberties[n - 1].add((i, i))

    @property
    def symbols(self) -> list[list[Union[int, set[int]]]]:
        return self._symbols

    def is_terminal(self) -> bool:
        self._remove_empty_liberties()
        return not self._liberties

    def get_children(self):
        self._remove_empty_liberties()
        size = min(self._liberties.keys())
        r, c = self._liberties[size].pop()
        assert len(self._symbols[r][c]) == size  # type: ignore
        for s in self._symbols[r][c]:  # type: ignore
            child = deepcopy(self)
            child._set_symbol(r, c, s)  # type: ignore
            child._update_symbols()
            if child._is_viable():
                yield child

    def _remove_empty_liberties(self) -> None:
        for size in range(self._n):
            if len(self._liberties[size]) == 0:
                del self._liberties[size]

    def _update_symbols(self) -> None:
        while self._liberties[1]:
            r, c = self._liberties[1].pop()
            assert len(self._symbols[r][c]) == 1  # type: ignore
            s = self._symbols[r][c].pop()  # type: ignore
            self._set_symbol(r, c, s)  # type: ignore

    def _set_symbol(self, r: int, c: int, s: int) -> None:
        size = len(self._symbols[r][c])  # type: ignore
        self._liberties[size].discard((r, c))
        self._symbols[r][c] = s
        for i in range(self._n):
            self._remove_symbol(r, i, s)
            self._remove_symbol(i, c, s)

    def _remove_symbol(self, r: int, c: int, s: int) -> None:
        if hasattr(self._symbols[r][c], 'remove'):
            if s in self._symbols[r][c]:  # type: ignore
                size = len(self._symbols[r][c])  # type: ignore
                self._liberties[size].remove((r, c))
                self._symbols[r][c].remove(s)  # type: ignore
                size = len(self._symbols[r][c])  # type: ignore
                self._liberties[size].add((r, c))

    def _is_viable(self) -> bool:
        return len(self._liberties[0]) == 0
