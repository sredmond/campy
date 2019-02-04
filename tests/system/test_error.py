"""Tests for the :mod:`campy.system.error` module."""
from campy.system.error import CampyException, InterruptedIOError, error

import pytest

def test_campy_exception_inherits_from_exception():
    assert issubclass(CampyException, Exception)


def test_errors_inherit_from_campy_exception():
    assert issubclass(InterruptedIOError, CampyException)


def test_error_from_string_raises_exception():
    with pytest.raises(CampyException):
        error("This should raise a CampyException.")


def test_error_from_builtin_error_raises_exception():
    with pytest.raises(CampyException) as excinfo:
        error(ValueError("I am a ValueError."))
    # print(excinfo.value)
    assert excinfo.type == CampyException
    assert "I am a ValueError" in str(excinfo.value)


def test_raise_exception_from_builtin_error():
    with pytest.raises(CampyException) as excinfo:
        try:
            1 / 0
        except ZeroDivisionError as exc:
            raise InterruptedIOError from exc
