"""Functions for encoding and decoding binary data in the base64 format.

For information on the base64 format, see:

    http://en.wikipedia.org/wiki/Base64

It is a lightweight wrapper around the builtin base64 library that ships with
Python.
"""

import base64 as _base64

def encode(b):
    """Encode bytes-like object b using the standard Base64 alphabet and return the encoded bytes.

    b is the byte string to encode. The encoded byte string is returned.
    """
    return _base64.standard_b64encode(b)

def decode(b):
    """Decode bytes-like object or ASCII string s using the standard Base64 alphabet and return the decoded bytes.

    b is the byte string to decode. The decoded byte string is returned.
    """
    return _base64.standard_b64decode(b)

__all__ = ['encode', 'decode']
