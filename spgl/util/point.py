#!/usr/bin/env python3 -tt
"""
File: point.h
-------------
Exports a type representing 2- and 3-dimensional points.
These points inherit from tuples, so you can do anything
you could otherwise do with tuples (notably, tuple unpacking)

Usage:

    origin = Point()
    pt = Point(4, 1)
    x = origin.x  # => x = 0
    y = pt.y      # => y = 1

    origin3 = Point3()
    pt = Point3(3, 4, 5)
    x, y, z = pt

"""
from collections import namedtuple as _nt

Point = _nt('Point', ['x', 'y'])
Point3 = _nt('Point', ['x', 'y', 'z'])
