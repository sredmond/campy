"""Tests for the :mod:`campy.util.randomgenerator` module."""
from campy.util.randomgenerator import RandomGenerator

def test_feed_int():
    rgen = RandomGenerator.get_instance()
    rgen._feed_int(5)
    assert rgen.randint(0, 10) == 5
