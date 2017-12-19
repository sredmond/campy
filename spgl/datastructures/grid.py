#!/usr/bin/env python3 -tt
"""

"""
class Grid(list):
    def __init__(self, num_rows=0, num_cols=0, value=None):
        self.num_rows = num_rows
        self.num_cols = num_cols
        # Elements are stored in row-major order
        self.elems = [[value for __ in range(num_cols)] for _ in range(num_rows)]

    def empty(self):
        return self.num_rows == 0 or self.num_cols == 0

    def fill(self, value):
        self.elems = [[value for __ in range(self.num_cols)] for _ in range(self.num_rows)]

    def get(self, row, col):
        return self.elems[row][col]

    def set(self, row, col, value):
        self.elems[row][col] = value

    def in_bounds(self, row, col):
        pass

    def resize(self, num_rows, num_cols, retain=False):
        if not retain:
            self.__init__(num_rows, num_cols)
        else:
            old = self.elems
            self.elems = [[None for __ in range(self.num_cols)] for _ in range(self.num_rows)]
            for oldrow, newrow in zip(old, self.elems):
                for pos, elems in enumerate(zip(oldelems, newelems)):
                    oldelem, newelem = elems
                    if oldelem != newelem:
                        newrow[pos] = oldelem

    # Use this when you need to copy
    @classmethod
    def from_grid(cls, grid):
        new = cls(grid.num_rows, grid.num_cols)
        new.elems = grid.elems
        return new

    @property
    def height(self):
        return num_rows

    @property
    def width(self):
        return num_cols

    # Magic methods to make a grid look like a list of lists

    def __len__(self):
        return len(self.elems)

    # Note - setitem and delitem don't make sense in this case
    def __getitem__(self, key):
        return self.elems[key]

    def __iter__(self):
        return iter(self.elems)

    def __reversed__(self):
        return reversed(self.elems)

    def __contains__(self, item):
        return item in self.elems

    def __repr__(self):
        return repr(self.elems)

