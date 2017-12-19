# TODO(sredmond): Possibly rename this file priorityqueue.h for compatibility.
"""
Min-heap.
"""
import collections as _collections

# TODO(sredmond): Make this into a collection subclass.
# TODO(sredmond): Use namedtuples.
import heapq as _heapq

class PriorityQueue(object):
    def __init__(self, initializer=None, priorities_first=True):
        if not initializer:
            initializer = []

        if priorities_first:
            self._heap = [(priority, value) for priority, value in initializer]
        else:
            self._heap = [(priority, value) for value, priority in initializer]
        _heapq.heapify(self._heap)

    def add(self, value, priority):
        _heapq.heappush(self._heap, (priority, value))

    def back(self):
        raise NotImplementedError

    def change_priority(self, value, new_priority):
        raise NotImplementerError

    def clear(self):
        self._heap = []

    def remove(self):
        top = _heapq.heappop(self._heap)
        return top[1]

    def front(self):
        raise NotImplementedError

    def __len__(self):
        return len(self._heap)

    def __eq__(self, other):
        return self._heap == other._heap

    def peek(self):
        top = self._heap[0]
        return top

    def peek_value(self):
        top = self._heap[0]
        return top[1]

    def peek_priority(self):
        top = self._heap[0]
        return top[0]

    enqueue = add
    dequeue = remove

    def __str__(self):
        pass




