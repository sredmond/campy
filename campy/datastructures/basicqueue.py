"""A basic, stripped down queue.

"""
import collections as _collections
import collections.abc as _collections_abc
import functools as _functools


# Implementation note: The head of the queue at index 0.
@_functools.total_ordering
# TODO(sredmond): Sized,Iterable,Container is called Collection in 3.6+
class BasicQueue(_collections_abc.Sized, _collections_abc.Iterable, _collections_abc.Container):
    def __init__(self, data=None):
        self._d = _collections.deque()
        if data:
            self._d.extend(data)

    def __contains__(self, val):
        return val in self._d

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    # Methods from C++ library
    def enqueue(self, value):
        self._d.append(value)

    def dequeue(self):
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
        return str(self._d).replace('deque', 'BasicQueue', 1)

    # TODO(sredmond): Add a repr method?

    def __eq__(self, other):
        return self._d == other._d

    def __le__(self, other):
        # TODO(sredmond): There are going to be a lot of problems with unorderable types.
        # TODO(sredmond): Isn't this already the default behavior of __le__?
        return self._d < other._d

    # Synonyms
    add = enqueue
    remove = dequeue
    front = peek
    # Removed: isempty, size, equals

__all__ = ['BasicQueue']
