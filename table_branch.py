from collections import defaultdict


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
