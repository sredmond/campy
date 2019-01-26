"""An enumerated type :class:`Direction` whose elements are the four cardinal directions:
``NORTH``, ``SOUTH``, ``EAST``, and ``WEST``.

A :class:`Direction` knows what :class:`Direction` is to the left, the right, or opposite itself
using the methods :func:`left`, :func:`right`, and :func:`opposite`.

Usage::

    direction = Direction.NORTH
    direction.left()      # => Direction.WEST
    direction.right()     # => Direction.EAST
    direction.opposite()  # => Direction.SOUTH
"""
import enum

@enum.unique
class Direction(enum.Enum):
    """Represent the four compass directions."""
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def left(self):
        """Return the direction to the left."""
        return self.__class__((self.value + 3) % 4)

    def right(self):
        """Return the direction to the right."""
        return self.__class__((self.value + 1) % 4)

    def opposite(self):
        """Return the opposite direction."""
        return self.__class__((self.value + 2) % 4)

    def __repr__(self):
        # Only show Direction.NAME, instead of the default '<Direction.NAME: value>`.
        return "{}.{}".format(self.__class__.__name__, self.name)

__all__ = ['Direction']
