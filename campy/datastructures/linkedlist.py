"""

"""
import collections as _collections

class LinkedList(_collections.abc.MutableSequence):
    def __init__(self):
        self.head = None

    # __getitem__, __setitem__, __delitem__, __len__, insert

    def add(self):
        pass

class LinkedListNode(object):
    def __init__(self, value, next_node):
        self.value = value
        self.next = next_node

    def __str__(self):
        return "LLNode(value={self.value})".format(self=self)
