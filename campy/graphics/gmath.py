"""Utility functions for working with 2D geometry degrees, vectors, and constants.

Most Python libraries (such as the ``math`` module) expect angles to be specified
in radians. While this is a good convention, new students may have trouble using
radians, so this module provides degree-accepting variants of the standard trig
functions, as well as a utility to convert between radians and degrees.

Students often also represent 2D vectors by their components, so we also provide
conversions to vector magnitude and vector angle.

The mathematical constants ``PI`` and ``E`` are also exported so that students
don't have to import the separate math module for those constants.

With all of these functions, the numerical precision is only as accurate as that
provided by the underlying ``math`` module.
"""
import math

from campy.system.error import error


"""The mathematical constant `pi`, equal to the ratio of a circle's circumference
to its diameter."""
PI = math.pi


"""The mathematical constant `e`, equal to the base of the natural logarithm."""
E = math.e


def to_degrees(radians):
    """Convert an angle from radians to degrees.

    Usage::

        print(to_degrees(PI))  # => 180.0
        print(to_degrees(PI / 2))  # => 90.0

    There is no restriction of the domain of this function, but that also means
    that the codomain is unrestricted. As a concrete example::

        print(to_degrees(-PI))  # => -180.0
        print(to_degrees(4 * PI))  # => 720.0

    :param radians: An angle (in radians)
    :returns: The same angle (in degrees)
    """
    return math.degrees(radians)


def to_radians(degrees):
    """Convert an angle from degrees to radians.

    Usage::

        print(to_radians(180.0))  # => 3.141592653589793
        print(to_radians(90.0))  # => 1.5707963267948966

    There is no restriction of the domain of this function, but that also means
    that the codomain is unrestricted. As a concrete example::

        print(to_radians(-180.0))  # => -3.141592653589793
        print(to_radians(720))  # => 12.566370614359172

    :param degrees: An angle (in degrees)
    :returns: The same angle (in radians)
    """
    return math.radians(degrees)

def sin_degrees(angle):
    """Return the trigonometric sine of an angle (in degrees).

    Usage::

        print(sin_degrees(30))  # => 0.49999999999999994
        print(sin_degrees(0))  # => 0.0
        print(sin_degrees(45.0))  # => 0.7071067811865475

    :param angle: An angle (in degrees)
    :returns: The sine of the given angle
    """
    return math.sin(to_radians(angle))

def cos_degrees(angle):
    """Return the trigonometric cosine of an angle (in degrees).

    Usage::

        print(cos_degrees(60))  # => 0.5000000000000001
        print(cos_degrees(90))  # => 6.123233995736766e-17
        print(cos_degrees(45.0))  # => 0.7071067811865476

    :param angle: An angle (in degrees)
    :returns: The cosine of the given angle
    """
    return math.cos(to_radians(angle))

def tan_degrees(angle):
    """Return the trigonometric tangent of an angle (in degrees).

    Usage::

        print(tan_degrees(0))  # => 0.0
        print(tan_degrees(90))  # => 1.633123935319537e+16
        print(tan_degrees(45.0))  # => 0.9999999999999999

    :param angle: An angle (in degrees)
    :returns: The tangent of the given angle
    """
    return math.tan(to_radians(angle))


def vector_magnitude(x, y):
    """Compute the magnitude of a vector given by two components.

    To compute the magnitude of vector with two components::

        print(vector_magnitude(3, 4))  # => 5.0

    To compute the magnitude of a :class:`GPoint`::

        pt = GPoint(3, 4)
        print(vector_magnitude(*pt))  # => 5.0

    :param x: x-coordinate of vector
    :param y: y-coordinate of vector
    :returns: magnitude of the vector (x, y)
    """
    return math.hypot(x, y)


def vector_angle(x, y):
    """Return the angle (in degrees) from the origin to the given point.

    The angle is measured counterclockwise from the positive x-axis, as is standard.

    This function accounts for the fact that, in our graphical coordinate system,
    the y-axis is flipped (with respect to the traditional Cartesian plane). That
    is, in the graphical coordinate system, the y-coordinate of a point increases
    as that point descends on the screen.

    Usage::

        print(vector_angle(3, 3))  # => -45.0
        print(vector_angle(3, 3 * math.sqrt(3)))  # => -60.00000000000001
        print(vector_angle(3 * math.sqrt(3), 3))  # => -29.999999999999996

    The returned angles in these examples are negative because the y-coordinate
    represents a point in the fourth quadrant.

    :param x: x-coordinate of point
    :param y: y-coordinate of point
    :returns: angle (in degrees) from (0, 0) to (x, -y)
    """
    return to_degrees(math.atan2(-y, x))


def count_digits(n, base=10):
    """Count the number of digits in a number in some base.

    Any non-integral part of the number is discarded: ``count_digits(3.1415)``
    is the same as ``count_digits(3)``.

    The provided n must be finite and the provided base must be a positive
    integer, otherwise an error is raised.

    Usage::

        count_digits(4)  # => 1
        count_digits(41)  # => 2
        count_digits(413)  # => 3

        count_digits(9.9)  # => 1
        count_digits(10.1)  # => 2

        count_digits(-15)  # => 2
        count_digits(-314.15)  # => 3

        count_digits(3, base=2)  # => 2
        count_digits(4, base=2)  # => 3
        count_digits(8, base=3)  # => 2
        count_digits(41, base=5)  # => 3

    Invalid Usage::

        count_digits(float('inf'))  # raises error
        count_digits(5, base=-3)  # raises error
        count_digits(5, base=2.2)  # raises error

    :param n: number whose digits to count
    :param base: base system to use
    :returns: the number of digits of n when written in the given base.
    """
    if not math.isfinite(n):
        error("n must be finite")
    if base <= 0 or not float.is_integer(base):
        error("base must be a positive integer")
    n = int(abs(n))
    base = int(base)

    count = 0
    while n > 0:
        count += 1
        n //= count
    return count


# TODO(sredmond): Consider adding an isclose method.


__all__ = [
    'PI', 'E',
    'to_degrees', 'to_radians',
    'sin_degrees', 'cos_degrees', 'tan_degrees',
    'vector_magnitude', 'vector_angle',
    'count_digits'
]
