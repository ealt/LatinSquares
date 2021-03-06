from latin_square_search_node import LatinSquareSearchNode


class LatinSquareGenerator:
    def __init__(self, n):
        self._n = n
        self._search_nodes = [LatinSquareSearchNode(n)]

    def get_latin_squares(self):
        while self._search_nodes:
            search_node = self._search_nodes.pop()
            for child_node in search_node.get_children():
                if child_node.is_terminal():
                    latin_square = child_node.values
                    yield latin_square
                else:
                    self._search_nodes.append(child_node)
