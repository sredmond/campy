"""Tests for the :mod:`campy.io.bitstream` module."""
from campy.io.bitstream import ibitstream, obitstream, ifbitstream, ofbitstream, istringbitstream, ostringbitstream

import os


def bytes_to_bits(message):
    """Convert a bytes message to a sequence of bits.

    Usage::

        print(tuple(bytes_to_bits(b'CS')))
        # => (0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1)
        # 01000011 is C
        # 01010011 is S
    """
    return map(int, ''.join(format(ch, 'b').zfill(8) for ch in message))


def test_read_bits_from_file():
    # The first 8 bits of this file as a string.
    with ifbitstream(__file__) as stream:
        # '00100010' is the binary representation of 34, which is '"' is ASCII.
        assert tuple(stream.readbit() for _ in range(8)) == (0, 0, 1, 0, 0, 0, 1, 0)


def test_write_bits_to_file():
    # Write a 0 and a 1 to /dev/null.
    with ofbitstream(os.devnull) as stream:
        stream.writebit(0)
        stream.writebit(1)
    assert True  # TODO(sredmond): Check that the data has been written.


def test_read_from_buffered_string_stream():
    # Read a message from an istringbitstream.
    message = b'hello'
    with istringbitstream(message) as stream:
        size = stream.size()
        expected = tuple(bytes_to_bits(message))
        assert tuple(stream.readbit() for _ in range(size)) == expected


def test_write_to_buffered_string_stream():
    # Write a message to an ostringbitstream.
    message = b'hello'
    with ostringbitstream() as stream:
        for bit in bytes_to_bits(message):
            stream.writebit(bit)
        assert stream.getvalue() == message
