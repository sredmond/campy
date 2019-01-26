#!/usr/bin/env python3 -tt
"""Exports a type representing 2- and 3-dimensional points.

These points inherit from tuples, so you can do anything
you could otherwise do with tuples (notably, tuple unpacking)

Usage::

    origin = Point()
    pt = Point(4, 1)
    x = origin.x  # => x = 0
    y = pt.y      # => y = 1

    origin3 = Point3()
    pt = Point3(3, 4, 5)
    x, y, z = pt
"""
import collections

Point = collections.namedtuple('Point', ['x', 'y'])
Point3 = collections.namedtuple('Point3', ['x', 'y', 'z'])

# TODO(sredmond): In Python 3.7+, use the `defaults` keyword argument to the namedtuple constructor.
Point.__new__.__defaults__= (0, 0)
Point3.__new__.__defaults__= (0, 0, 0)

# Override property documentation
# TODO(sredmond): For some reason, the property's __doc__ attribute is readonly.
# Point.x.__doc__ = "The x-coordinate of a 2D point."
# Point.y.__doc__ = "The y-coordinate of a 2D point."
# Point3.x.__doc__ = "The x-coordinate of a 3D point."
# Point3.y.__doc__ = "The y-coordinate of a 3D point."
# Point3.z.__doc__ = "The z-coordinate of a 3D point."

__all__ = ['Point', 'Point3']
