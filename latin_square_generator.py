from itertools import permutations
from latin_square_search_node import LatinSquareSearchNode


class LatinSquareGenerator:
    def __init__(self, n, subset='all', **kwargs):
        self._n = n
        self._subset = subset
        self._search_nodes = [LatinSquareSearchNode(n)]

    def get_latin_squares(self):
        while self._search_nodes:
            search_node = self._search_nodes.pop()
            for child_node in search_node.get_children():
                if child_node.is_terminal():
                    latin_square = child_node.symbols
                    if self._subset == 'reduced':
                        yield latin_square
                    elif self._subset == 'symbol_isotropy_classes':
                        yield from self._get_row_permutations(latin_square)
                    else:
                        yield from self._get_all_permutations(latin_square)
                else:
                    self._search_nodes.append(child_node)

    def _get_all_permutations(self, latin_square):
        for symbol_map in permutations(range(self._n)):
            permuted_symbols = [[symbol_map[s] for s in row] for row in latin_square]
            yield from self._get_row_permutations(permuted_symbols)

    def _get_row_permutations(self, latin_square):
        for permuted_rows in permutations(latin_square[1:]):
            yield [latin_square[0]] + list(permuted_rows)
