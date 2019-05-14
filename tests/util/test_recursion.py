"""Tests for the :mod:`campy.util.recursion` module."""
from campy.util.recursion import get_indent

import functools
import io


def apply_io_patch(monkeypatch):
    out = io.StringIO()
    monkeypatch.setattr('sys.stdout', out)
    return out


def tail(n):
    if n > 0:
        print(get_indent() + str(n))
        tail(n - 1)


def fib(n):
    print(get_indent() + str(n))
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def cached_fib(n, cache={}):
    print(get_indent() + str(n))
    if n <= 1:
        return 1

    if n in cache:
        return cache[n]
    out = cached_fib(n-1) + cached_fib(n-2)
    cache[n] = out
    return cache[n]


@functools.lru_cache(maxsize=None)
def decorated_fib(n):
    print(get_indent() + str(n))
    return 1 if n <= 1 else decorated_fib(n-1) + decorated_fib(n-2)


def test_tail(monkeypatch):
    out = apply_io_patch(monkeypatch)
    tail(5)
    expected = (
        "5\n"
        "    4\n"
        "        3\n"
        "            2\n"
        "                1\n"
    )
    assert out.getvalue() == expected


def test_fib(monkeypatch):
    out = apply_io_patch(monkeypatch)
    fib(5)
    expected = (
        "5\n"
        "    4\n"
        "        3\n"
        "            2\n"
        "                1\n"
        "                0\n"
        "            1\n"
        "        2\n"
        "            1\n"
        "            0\n"
        "    3\n"
        "        2\n"
        "            1\n"
        "            0\n"
        "        1\n"
    )
    assert out.getvalue() == expected


def test_cached_fib(monkeypatch):
    out = apply_io_patch(monkeypatch)
    cached_fib(5)
    expected = (
        "5\n"
        "    4\n"
        "        3\n"
        "            2\n"
        "                1\n"
        "                0\n"
        "            1\n"
        "        2\n"
        "    3\n"
    )
    assert out.getvalue() == expected


def test_decorated_fib(monkeypatch):
    out = apply_io_patch(monkeypatch)
    decorated_fib(5)
    expected = (
        "5\n"
        "    4\n"
        "        3\n"
        "            2\n"
        "                1\n"
        "                0\n"
    )
    assert out.getvalue() == expected
