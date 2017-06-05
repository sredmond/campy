import functools as _functools

@_functools.total_ordering
class Stack():
    def __init__(self):
        self._elems = []

    def add(self, value):
        self.push(value)

    def remove(self):
        return self.pop()

    def top(self):
        return self.peek()

    def clear(self):
        self._elems.clear()

    def is_empty(self):
        return len(self._elems) == 0

    def peek(self):
        return self._elems[-1]

    def pop(self):
        return self._elems.pop()

    def push(self, value)
        self._elems.append(value)

    def __len__(self):
        return len(self._elems)

    def __eq__(self, other):
        return self._elems == other._elems

    def __lt__(self, other):
        pass
        # TODO

    def __str__(self):
        return "Stack[elems={}]".format(elems)

