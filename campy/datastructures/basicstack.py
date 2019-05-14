import collections as _collections
import collections.abc as _collections_abc
import functools as _functools


# Implementation note: The head of the stack is at index 0.
@_functools.total_ordering
# TODO(sredmond): Sized,Iterable,Container is called Collection in 3.6+
class BasicStack(_collections_abc.Sized, _collections_abc.Iterable, _collections_abc.Container):
    def __init__(self, data=None):
        self._d = _collections.deque()
        if data:
            self._d.extend(data)

    def __contains__(self, val):
        return val in self._d

    def __iter__(self):
        return reversed(iter(self._d))

    def __len__(self):
        return len(self._d)

    # Methods from C++ library
    def push(self, value):
        self._d.appendleft(value)  # NOTE(sredmond): This is the only difference between BasicStack and BasicQueue

    def pop(self):
        if not self._d:
            pass
            # error("Queue::dequeue: Attempting to dequeue an empty queue")
        return self._d.popleft()

    def clear(self):
        self._d.clear()

    def peek(self):
        if not self._d:
            pass
            # error("Queue::dequeue: Attempting to dequeue an empty queue")
        return self._d[0]

    def back(self):
        if not self._d:
            pass
            # error("Queue::dequeue: Attempting to dequeue an empty queue")
        return self._d[-1]

    def __str__(self):
        return str(self._d).replace('deque', 'BasicStack', 1)

    # TODO(sredmond): Add a repr method?

    def __eq__(self, other):
        return self._d == other._d

    def __le__(self, other):
        # TODO(sredmond): There are going to be a lot of problems with unorderable types.
        # TODO(sredmond): Isn't this already the default behavior of __le__?
        return self._d < other._d

    # Synonyms
    add = push
    remove = pop
    front = peek
    # Removed: isempty, size, equals


