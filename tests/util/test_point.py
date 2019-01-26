"""Tests for the :mod:`campy.util.point` module."""
from campy.util.point import Point, Point3


def test_origin():
    point = Point()
    assert point.x == 0
    assert point.y == 0


def test_set_point_by_positional_arguments():
    point = Point(4, 1)
    assert point.x == 4
    assert point.y == 1


def test_set_point_by_named_arguments():
    point = Point(y=1, x=4)
    assert point.x == 4
    assert point.y == 1


def test_pointwise_equality():
    a = Point(4, 1)
    b = Point(y=1, x=4)
    assert a == b


def test_partial_point_construction_x():
    point = Point(4)
    assert point.x == 4
    assert point.y == 0


def test_partial_point_construction_y():
    point = Point(y=1)
    assert point.x == 0
    assert point.y == 1

def test_origin3():
    point = Point3()
    assert point.x == 0
    assert point.y == 0
    assert point.z == 0


def test_set_point3_by_positional_arguments():
    point = Point3(2, 8, 9)
    assert point.x == 2
    assert point.y == 8
    assert point.z == 9


def test_set_point3_by_named_arguments():
    point = Point3(y=8, z=9, x=2)
    assert point.x == 2
    assert point.y == 8
    assert point.z == 9


def test_point3wise_equality():
    a = Point3(2, 8, 9)
    b = Point3(y=8, z=9, x=2)
    assert a == b


def test_partial_point3_construction_x():
    point = Point3(4)
    assert point.x == 4
    assert point.y == 0
    assert point.z == 0


def test_partial_point3_construction_y():
    point = Point3(y=8)
    assert point.x == 0
    assert point.y == 8
    assert point.z == 0


def test_partial_point3_construction_z():
    point = Point3(z=9)
    assert point.x == 0
    assert point.y == 0
    assert point.z == 9


def test_partial_point3_construction_xy():
    point = Point3(2, 8)
    assert point.x == 2
    assert point.y == 8
    assert point.z == 0


def test_partial_point3_construction_yz():
    point = Point3(y=8, z=9)
    assert point.x == 0
    assert point.y == 8
    assert point.z == 9


def test_partial_point3_construction_xz():
    point = Point3(2, y=8)
    assert point.x == 2
    assert point.y == 8
    assert point.z == 0
