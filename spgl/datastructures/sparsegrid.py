import collections as _collections
import functools as _functools

@functools.total_ordering
class SparseGrid(_collections.abc.MutableMapping):
    def __init__(self, num_rows, num_cols, value=None):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._elements = _collections.defaultdict(dict)
        if value is not None:  # Even if user supplies an empty string, we want to fill
            self.fill(value)

    @classmethod
    def from_2d_iterable():
        pass

    def resize():
        pass

    @property
    def width():
        return self.num_cols

    @property
    def height():
        return self.num_rows

    def __getitem__(self, key):
        if isinstance(key, tuple):
            # Invoked like grid[row, col]
            row, col = key
            self.check_indexes(row, col);
            if row not in self._elements:
                raise KeyError(key)
            if col not in self._elements[row]:
                raise KeyError(key)
            return self._elements[row][col]
        else:
            # Invoked like grid[row][col]
            if key not in self._elements:
                raise KeyError(key)
            return self._elements[key]

    def __setitem__(self, key, value):
        # If invoked as grid[row][val], the first grid[row] will be use __getitem__, and then the latter is a usual dictionary lookup
        if not isinstance(key, tuple):
            error('Invalid key.')
        row, col = key
        self.check_indexes(row, col);
        self._elements[row][col] = value

    def __delitem__(self, key):
        if not isinstance(key, tuple):
            error('Invalid key.')
        self.check_indexes(row, col);
        del self._elements[row][col]

    def __iter__(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if row, col in self:
                    yield self[row, col]

    def __len__(self):
        return sum(len(row) for row in self._elements)

    def check_indexes(self, row, col):
        if not self.in_bounds(row, col):
            error('SparseGrid: ({}, {}) is outside of valid range'.format(row, col)) # TODO: better errors

    def in_bounds(self, row, col):
        return 0 <= row < self.num_rows and 0 <= col < self.num_cols

    def fill(self, value):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self[row, col] = value

    def resize(self, ):
        pass

    def __le__(self, other):
        rows = max(self.height, other.height)
        cols = max(self.width, other.width)


    def __eq__(self, other):
        # optimization: if literally same grid, stop
        if self is other: return True
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols: return False
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if row, col in self:
                    # I have data there; she must, too, and it must be the same data
                    if row, col not in other or self[row, col] != other[row, col]:
                        return False
                else:
                    # I don't have data there; she must also not have it there
                    if row, col in other:
                        return False
        return True

    def __str__(self):
        pass

    def to_string_2d(self):
        pass

    def serialize(self):
        pass

    def from_stream(self):
        pass

    def randomElement
