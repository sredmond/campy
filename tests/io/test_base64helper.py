"""Tests for the :mod:`campy.io.base64helper` module."""
from campy.io.base64helper import encode, decode


def test_encode_empty_string():
    message = b''
    assert encode(message) == b''


def test_decode_empty_string():
    message = b''
    assert decode(message) == b''


def test_encode():
    message = b'Hello world!'
    assert encode(message) == b'SGVsbG8gd29ybGQh'


def test_decode():
    message = b'SGVsbG8gd29ybGQh'
    assert decode(message) == b'Hello world!'
