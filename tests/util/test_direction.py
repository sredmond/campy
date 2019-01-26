"""Tests for the :mod:`campy.util.direction` module."""
from campy.util.direction import Direction


def test_north_exists():
    assert Direction.NORTH in Direction


def test_west_is_left_of_north():
    direction = Direction.NORTH
    assert direction.left() == Direction.WEST


def test_east_is_right_of_north():
    direction = Direction.NORTH
    assert direction.right() == Direction.EAST


def test_south_is_opposite_of_north():
    direction = Direction.NORTH
    assert direction.opposite() == Direction.SOUTH


def test_left_is_inverse_of_right():
    for direction in Direction:
        assert direction == direction.left().right()
        assert direction == direction.right().left()


def test_opposite_is_inverse_of_itself():
    for direction in Direction:
        assert direction == direction.opposite().opposite()


def test_left_has_order_4():
    for direction in Direction:
        assert direction == direction.left().left().left().left()


def test_right_has_order_4():
    for direction in Direction:
        assert direction == direction.right().right().right().right()
