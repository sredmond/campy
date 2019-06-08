"""Exported types for representing points, dimensions, and rectangles.

A :class:`GPoint` represents an (x, y) pair and defaults to (0, 0).

A :class:`GDimension` represents a (width, height) pair and defaults to (0, 0).

A :class:`GRectangle` represents an (x, y, width, height) quadruplet and
defaults to (0, 0, 0, 0).

Named attributes are accessible for each of these types::

    point = GPoint(4, 1)
    print(point.x, point.y)  # => 4, 1

    size = GDimension(41, 574)
    print(size.width, size.height)  # => 41, 574

    rect = GRectangle(4, 1, 41, 574)
    print(rect.x, rect.y, rect.width, rect.height)  # => 4, 1, 41, 574

Each of these types can also be unpacked like a tuple.

    point = GPoint(4, 1)
    x, y = point

    size = GDimension(41, 574)
    width, height = size

    rect = GRectangle(4, 1, 41, 574)
    x, y, width, height = rect

Lastly, each of these types is immutable.
"""
# NOTE: There's a lot of hacking around with the internals of namedtuple in
# this module. This level of hacking is not encouraged, and might be removed
# in the future, replacing these types with custom-style namedtuples.
# Here be dragons.
# TODO(sredmond): Redocument these types so that Sphinx's autodoc sees them.
# TODO(sredmond): Reconsider defaulting all arguments to 0.0 instead of 0.
import collections
import operator


# An (x, y) pair defaulting to (0, 0).
GPoint = collections.namedtuple('GPoint', ('x', 'y'))
GPoint.__new__.__defaults__ = (0, 0)


# A (width, height) pair defaulting to (0, 0).
GDimension = collections.namedtuple('GDimension', ('width', 'height'))
GDimension.__new__.__defaults__ = (0, 0)
GDimension.empty = lambda dim: dim.width <= 0 or dim.height <= 0
GDimension.empty.__name__ = 'empty'


# An (x, y, width, height) quadruplet defaulting to (0, 0, 0, 0)
GRectangle = collections.namedtuple('GRectangle', ('x', 'y', 'width', 'height'))
GRectangle.__new__.__defaults__ = (0, 0, 0, 0)
GRectangle.empty = lambda rect: rect.width <= 0 or rect.height <= 0
GRectangle.empty.__name__ = 'empty'
# NOTE(sredmond): Since we consider the edge to be contained, "empty" GRectangles can still contain points.
GRectangle.__contains__ = lambda rect, point: 0 <= point[0] - rect.x <= rect.width and 0 <= point[1] - rect.y <= rect.height
GRectangle.__contains__.__name__ = '__contains__'


# Override docstrings. This is perhaps the messiest part of this file.
GPoint.__doc__ = 'Graphical representation of an (x, y) point defaulting to (0, 0).'
GPoint.__new__.__doc__ = """Create a :class:`GPoint`.

If parameters are not supplied, all arguments default to 0.

All arguments have units of pixels.

:param x: The x-coordinate (in pixels).
:param y: The y-coordinate (in pixels).
"""
GPoint.x = property(operator.itemgetter(0), doc='The x-coordinate (in pixels).')
GPoint.y = property(operator.itemgetter(1), doc='The y-coordinate (in pixels).')


GDimension.__doc__ = 'Graphical representation of a size (width, height) defaulting to (0, 0).'
GDimension.__new__.__doc__ = """Create a :class:`GDimension`.

If parameters are not supplied, all arguments default to 0.

All arguments have units of pixels.

:param width: The width (in pixels).
:param height: The height (in pixels).
"""
GDimension.width = property(operator.itemgetter(0), doc='The width (in pixels).')
GDimension.height = property(operator.itemgetter(1), doc='The height (in pixels).')
GDimension.empty.__doc__ = 'Return whether this rectangle is empty.'


GRectangle.__doc__ = """Graphical rectangle with upper-left corner (x, y) and size (width, height).

A :class:`GRectangle` is often used to represent the bounding box of a graphical object.
"""
GRectangle.__new__.__doc__ = """Create a :class:`GRectangle`.

The x- and y-coordinates refer to the upper-left corner of this
:class:`GRectangle`.

If parameters are not supplied, all arguments default to 0.

All arguments have units of pixels.

:param x: The x-coordinate of the upper left corner (in pixels).
:param y: The y-coordinate of the upper left corner (in pixels).
:param width: The width of this rectangle (in pixels).
:param height: The height of this rectangle (in pixels).
"""
GRectangle.x = property(operator.itemgetter(0), doc='The x-coordinate of the upper left corner (in pixels).')
GRectangle.y = property(operator.itemgetter(1), doc='The y-coordinate of the upper left corner (in pixels).')
GRectangle.width = property(operator.itemgetter(2), doc='The width of this rectangle (in pixels).')
GRectangle.height = property(operator.itemgetter(3), doc='The height of this rectangle (in pixels).')
GRectangle.empty.__doc__ = 'Return whether this rectangle is empty.'
GRectangle.__contains__.__doc__ = """Return whether this rectangle contains a point.

The edges of the rectangle are considered to be contained by the rectangle.
For example, the point (4, 1) is contained in the rectangle (4, 1, 41, 574).

The point must be unpackable into two elements, which means that you can use a
:class:`GPoint` or a two-element tuple::

    rect = GRectangle(4, 1, 41, 574)
    point = GPoint(4, 1)
    if point in rect:  # Using a GPoint.
        print('GPoint is contained.')
    if (5, 3) in rect:  # Using a tuple.
        print('tuple is contained')

:param point: An (x, y) point to check for containment.
:return: Whether this rectangle contains the given point.
"""

__all__ = ('GPoint', 'GDimension', 'GRectangle')
