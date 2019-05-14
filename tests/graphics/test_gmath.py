"""Tests for the :mod:`campy.graphics.gmath` module."""
from campy.graphics.gmath import PI, E, to_radians, to_degrees, sin_degrees, cos_degrees, tan_degrees, vector_magnitude, vector_angle, count_digits

import math  # For ground truth

def test_pi_is_pi():
    assert PI == math.pi

def test_e_is_e():
    assert E == math.e
