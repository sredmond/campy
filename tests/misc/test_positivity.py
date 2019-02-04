"""Tests for the :mod:`campy.misc.positivity` module."""
from campy.misc.positivity import QUOTES


def test_quotes_exist():
    assert len(QUOTES) > 0

def test_quotes_have_content():
    assert len(QUOTES[0].content) > 0

def test_quotes_have_an_author():
    assert len(QUOTES[0].author) > 0
