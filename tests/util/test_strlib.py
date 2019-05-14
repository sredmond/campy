"""Tests for the :mod:`campy.util.strlib` module."""
from campy.util.strlib import quote_string


def test_write_quoted_string():
    quoted = "\a\b\f\n\r\t\v\"\\abcdefghijklmnopqrstuvwxyz1234567890"
    assert quote_string(quoted) == '"\\a\\b\\f\\n\\r\\t\\v\\"\\\\abcdefghijklmnopqrstuvwxyz1234567890"'
