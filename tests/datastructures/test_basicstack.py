"""Tests for the :mod:`campy.datastructures.basicstack` module."""
from campy.datastructures.basicstack import BasicStack


def test_create_empty_stack():
    bs = BasicStack()
    assert True


def test_create_queue_with_data_from_list():
    bs = BasicStack([40, "one"])
    assert len(bs) == 2


def test_create_queue_with_data_from_iterable():
    bs = BasicStack(range(41, 198, 3))
    assert len(bs) == 53


def test_basic_operations():
    bs = BasicStack()
    bs.push('of one')
    bs.push(6)
    bs.push(8)
    assert bs.pop() == 8
    assert bs.peek() == 6
    assert str(bs) == "BasicStack([6, 'of one'])"

    bs2 = BasicStack([6, 'of one'])
    assert bs == bs2

    # TODO(sredmond): What the heck is this stack comparison?
    bs.add(12)
    assert bs > bs2
