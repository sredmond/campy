#!/usr/bin/env python3 -tt
"""
File: bitstream.cpp
-------------------
This file defines the ibitstream and obitstream classes.
These classes are patterned after (and, in fact, inherit from) the standard
io.BufferedReader and io.BufferedWriter classes.

The ibitstream and obitstream classes are basically the
same as the ordinary io.BufferedReader and io.BufferedWriter classes, but add the
functionality to read and write one bit at a time.

The idea is that you can substitute an ibitstream in place of an
io.BufferedReader and use the same operations (read, close, tell, etc.)
along with added member functions of readBit, rewind, and size.

Similarly, the obitstream can be used in place of io.BufferedWriter, and has
same operations (write, close, seek, etc.) along with additional
member functions writeBit and size.

# You can use ibitstream in any There are two subclasses of ibitstream: ifbitstream and istringbitstream,
# which are similar to the io. and istringstream classes.  The
# obitstream class similarly has ofbitstream and ostringbitstream as
# subclasses.

Note: in keeping with the naming conventions of the Python standard library,
readBit and writeBit have been renamed as readbit and writebit

Additionally, str() in ibitstream has been removed (doesn't make much sense anyway)
and for consistency with the standard library str in obitstream has been renamed getvalue()

Usage:

To use an ifbitstream::

    with ifbitstream(filename) as stream:
        bit = stream.readbit()
        stream.rewind()
        bit = stream.readbit()

To use an ofbitstream::

    with ofbitstream(filename) as stream:
        stream.writebit(0)
        ...

To use an ostringbitstream::

    with ostringbitstream() as stream:
        stream.writebit(0)
        ...
        stream.getvalue()  # => b'hello world'

To use an istringbitstream::

    with istringstream(b'hello world') as stream:
        bit = stream.readbit()
"""

import io as _io

"""
Constant: PSEUDO_EOF
A constant representing the PSEUDO_EOF marker that you will
write at the end of your Huffman-encoded file.
"""
PSEUDO_EOF = 256;

"""
Constant: NOT_A_CHAR
A constant representing an extended character that does not
actually hold a value.    When you are constructing your Huffman
encoding tree, you should set the characters in each internal
node (non-leaf) to this value to explicitly mark that they are not
being used.
"""
NOT_A_CHAR = 257;

NUM_BITS_IN_BYTE = 8

def get_nth_bit(pos, byte):
    return (byte >> (NUM_BITS_IN_BYTE - 1 - pos)) & 1

def set_nth_bit(pos, byte):
    return byte | 1 << (NUM_BITS_IN_BYTE - 1 - pos)

class ibitstream(_io.BufferedReader):
    def __init__(self, raw, buffer_size=_io.DEFAULT_BUFFER_SIZE):
        super().__init__(raw, buffer_size)
        self._fake = False
        self.pos = NUM_BITS_IN_BYTE
        self.current_byte = 0
        self.last_tell = 0

    def readbit(self):
        if self.closed:
            raise ValueError("ibitstream.readbit: Cannot read a bit from a stream that is not open.")
        if self._fake:  # Fake mode is used for autograding, and reads bytes as if they were bits
            bit = read(1)
            if bit == 0 or bit == ord('0'):
                return 0
            else:
                return 1
        else:
            # We consumed a whole byte, or the stream changed under us
            if self.pos == NUM_BITS_IN_BYTE or self.last_tell != self.tell():
                self.current_byte = self.read(1)
                if not self.current_byte:  # EOS
                    return PSEUDO_EOF
                self.current_byte = ord(self.current_byte)
                self.pos = 0
                self.last_tell = self.tell()
            result = get_nth_bit(self.pos, self.current_byte)
            self.pos += 1
            return result

    def rewind(self):
        if not self.seekable():
            raise _io.UnsupportedOperation()
        return self.seek(0) == 0

    def size(self):
        cur = self.tell()
        self.seek(0, _io.SEEK_END)
        end = self.tell()
        self.seek(cur, _io.SEEK_SET)
        return end * NUM_BITS_IN_BYTE


class obitstream(_io.BufferedWriter):
    def __init__(self, raw, buffer_size=_io.DEFAULT_BUFFER_SIZE, always_flush=True):
        super().__init__(raw, buffer_size)
        self._fake = False
        self.pos = NUM_BITS_IN_BYTE
        self.current_byte = 0
        self.last_tell = 0
        self.always_flush = always_flush

    def writebit(self, bit):
        if bit not in (0, 1):
            raise ValueError("obitstream.writebit: must pass an integer argument of 0 or 1. You passed the integer {}".format(bit))
        if self.closed:
            raise ValueError("obitstream.writebit: Cannot write a bit to a stream that is not open.")
        if self._fake:
            self.write(b'0' if bit == 0 else b'1')
            if self.always_flush:
                self.flush()
        else:
            # We wrote a whole byte, or the stream changed under us
            if self.pos == NUM_BITS_IN_BYTE or self.last_tell != self.tell():
                self.current_byte = 0
                self.pos = 0
            if bit:
                self.current_byte = set_nth_bit(self.pos, self.current_byte)
            if self.pos == 0 or bit:  # Write the first bit, or a change from 0 to 1
                if self.pos:
                    self.seek(-1, _io.SEEK_CUR)
                self.write(bytes([self.current_byte]))
                if self.always_flush:
                    self.flush()

            self.pos += 1
            self.last_tell = self.tell()

    def size(self):
        cur = self.tell()
        self.seek(0, _io.SEEK_END)
        end = self.tell()
        self.seek(cur, _io.SEEK_SET)
        return end * NUM_BITS_IN_BYTE

class ifbitstream(ibitstream):
    def __init__(self, filename):
        self.stream = _io.open(filename, 'rb')
        super().__init__(self.stream)


class ofbitstream(obitstream):
    def __init__(self, filename):
        self.stream = _io.open(filename, 'wb')
        super().__init__(self.stream)


class istringbitstream(ibitstream):
    def __init__(self, string):
        self.stream = _io.BytesIO(string)
        super().__init__(self.stream)

    def setvalue(self, string):
        view = self.stream.getbuffer()
        view[:] = string


class ostringbitstream(obitstream):
    def __init__(self):
        self.stream = _io.BytesIO()
        super().__init__(self.stream)

    def getvalue(self):
        return self.stream.getvalue()

__all__ = ['ibitstream', 'obitstream', 'ifbitstream', 'ofbitstream', 'istringbitstream', 'ostringbitstream']
