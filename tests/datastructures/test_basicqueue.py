"""Tests for the :mod:`campy.datastructures.basicqueue` module."""
from campy.datastructures.basicqueue import BasicQueue

def test_create_empty_queue():
    bq = BasicQueue()
    assert True

def test_create_queue_with_data_from_list():
    bq = BasicQueue([40, "one"])
    assert True

def test_create_queue_with_data_from_iterable():
    bq = BasicQueue(range(41, 198, 3))
    assert len(bq) == 53

def test_basic_operations():
    bq = BasicQueue()

    bq.enqueue(8)
    bq.enqueue(6)
    assert bq.dequeue() == 8
    assert bq.peek() == 6

    bq.enqueue('of one')
    assert str(bq) == "BasicQueue([6, 'of one'])"

    bq2 = BasicQueue([6, 'of one'])
    assert bq == bq2

    # TODO(sredmond): What the heck is this queue comparison?
    bq.enqueue(12)
    assert bq > bq2
