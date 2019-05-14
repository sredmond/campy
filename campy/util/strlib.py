#!/usr/bin/env python3 -tt
"""
File: strlib.py
---------------
Exports a few useful string functions that are not
included by default with Python strings.
"""
import string as _string
import urllib.parse as _parse

_STRING_DELIMITERS = ",:)}]\n"

def equals_ignore_case(s1, s2):
    return s1.lower() == s2.lower()

def string_needs_quoting(string):
    """
    Checks whether the string needs quoting in order to be handled correctly.
    """

    for ch in string:
        if ch.isspace():
            break
        if ch in _STRING_DELIMITERS:
            return True
    return False

def quote_string(string, force_quotes=True):
    """
    Returns a copy of the string surrounded by double quotes, converting
    special characters to escape sequences, as necessary. If the optional
    parameter force is explicitly set to false, quotes are included
    in the output only if necessary.

    TODO make this more pythonic
    TODO: bug: doesn't print non-printing chars to JBE correctly
    """
    force_quotes |= string_needs_quoting(string)
    out = ''
    if force_quotes:
        out += '"'

    trans = str.maketrans({
        '"': '\\"',
        '\a': '\\a',
        '\b': '\\b',
        '\f': '\\f',
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
        '\v': '\\v',
        '\\': '\\\\'
    })
    return '"{}"'.format(string.translate(trans))

def html_decode(encoded_html):
    return encoded_html.replace('&lt;', '<') \
                       .replace('&gt;', '>') \
                       .replace('&quot;', '"') \
                       .replace('&amp;', '&')

def html_encode(plain_html):
    return plain_html.replace('&', '&amp;') \
                     .replace('<', '&lt;') \
                     .replace('>', '&gt;') \
                     .replace('"', '&quot;')

def url_encode(string):
    # TODO make sure this is consistent with CPP lib
    return _parse.quote_plus(string, safe='~*')

def url_decode(string):
    # TODO make sure this is consistent with CPP lib
    return _parse.unquote_plus(string)


def string_is_bool(string):
    return string in (str(False), str(True))


def string_is_integer(string, radix=10):
    try:
        out = int(string, radix)
    except ValueError:
        return False
    return True

def string_is_real(string):
    try:
        out = float(string)
    except ValueError:
        return False
    return True

string_is_double = string_is_real
string_is_long = string_is_real

"""
The following methods are included only for compatibility with the Stanford CPP Libraries
They are redundant with builtin Python functionality, and should almost never be used.
"""
def bool_to_string(b):
    return 'True' if b else 'False'

def starts_with(string, prefix):
    return string.startswith(prefix)

def ends_with(string, suffix):
    return string.endswith(suffix)

