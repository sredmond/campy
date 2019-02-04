"""Tests for the :mod:`campy.misc.easter` module."""
from campy.misc.easter import LOGO, SNAKE, QUOTES


def test_quotes_exist():
    assert len(QUOTES) > 0
