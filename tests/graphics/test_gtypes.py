"""Tests for the :mod:`campy.graphics.gtypes` module."""
from campy.graphics.gtypes import GPoint, GDimension, GRectangle

def test_create_gpoint_with_default_values():
    point = GPoint()
    assert True

def test_create_gpoint_with_index():
    pass


def test_access_gpoint_components_by_name():
    point = GPoint(4, 1)
    x, y = point.x, point.y
    assert x == 4
    assert y == 1


def test_access_gpoint_components_by_index():
    point = GPoint(4, 1)
    x, y = point[0], point[1]
    assert x == 4
    assert y == 1


def test_unpack_gpoint():
    point = GPoint(4, 1)
    x, y = point
    assert x == 4
    assert y == 1


def test_string():
    point = GPoint()
    assert str(point) == "GPoint(x=0.0, y=0.0)"


def test_point_equality():
    point = GPoint()
    empty = GPoint()
    assert point == empty
    assert not point != empty
