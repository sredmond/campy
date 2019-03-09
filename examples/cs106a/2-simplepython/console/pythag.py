#!/usr/bin/env python
"""CS106A Assignment 2 Example: Pythagorean Theorem

Given two positive integers a and b, print the value c that satisfies
$a^2 + b^2 = c^2$. In other words, if a and b are the non-hypotenuse side
lengths of a right triangle, c is the length of the hypotenuse.

Usage::

    $ python pythag.py
    a: 3
    b: 4
    c = 5.0
"""
import math

from campy.util.simpio import get_positive_real


def compute_hypotenuse(a, b):
    """Compute the hypotenuse length of a right triangle with legs a and b."""
    return math.hypot(a, b)


if __name__ == '__main__':
    print("Enter values to compute the Pythagorean theorem.")

    # Get two positive real numbers from the user.
    a = get_positive_real('a:')
    b = get_positive_real('b:')

    # Print out the hypotenuse length.
    print('c = {}'.format(compute_hypotenuse(a, b)))
