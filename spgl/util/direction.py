#!/usr/env/bin python3 -tt
"""
File: direction.py
------------------
Exports an enumerated type `Direction` whose elements are the four cardinal
directions: NORTH, SOUTH, EAST, and WEST.

A direction knows what direction is to the left, the right, or opposite itself
using the methods `left()`, `right()`, and `opposite()`

Usage:

    direction = Direction.NORTH
    direction.left()      # => Direction.WEST
    direction.right()     # => Direction.EAST
    direction.opposite()  # => Direction.SOUTH
"""
from enum import Enum, unique

@unique
class Direction(Enum):
    """This enumerated type represents compass directions."""
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def left(self):
        """Returns the direction that is to the left of self."""
        return self.__class__((self.value + 3) % 4)

    def right(self):
        """Returns the direction that is to the right of self."""
        return self.__class__((self.value + 1) % 4)

    def opposite(self):
        """Returns the direction that is opposite to self."""
        return self.__class__((self.value + 2) % 4)

    def __repr__(self):
        return "{}.{}".format(self.__class__.__name__, self.name)

if __name__ == '__main__':
    direction = Direction.NORTH
    print(direction)
    print(direction.left())      # => Direction.WEST
    print(direction.right())     # => Direction.EAST
    print(direction.opposite())  # => Direction.SOUTH
