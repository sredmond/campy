"""Tests for the :mod:`campy.io.tokenscanner` module."""
from campy.io.tokenscanner import TokenScanner
import io

def test_tokenscanner():
    source = io.StringIO('hello 3.14 "world" is this weird >> then I think so')
    scanner = TokenScanner(source)
    scanner.add_operator('>>')
    scanner._scan_numbers = True
    scanner._scan_words = True

    # TODO(sredmond): Actually implement TokenScanner so that these tests pass.
    assert scanner.has_more_tokens()
    assert scanner.next_token() == 'hello'
    assert scanner.has_more_tokens()
    assert scanner.next_token() == '3.14'
    assert scanner.has_more_tokens()
    assert scanner.next_token() == '"world"'
    assert scanner.has_more_tokens()
    assert scanner.next_token() == 'is'
    assert scanner.has_more_tokens()
    assert scanner.next_token() == 'this'
    assert scanner.has_more_tokens()
    assert scanner.next_token() == 'weird'
    assert scanner.has_more_tokens()
    assert scanner.next_token() == 'then'
    assert scanner.has_more_tokens()
    assert scanner.next_token() == 'I'
    assert scanner.has_more_tokens()
    assert scanner.next_token() == 'think'
    assert scanner.has_more_tokens()
    assert scanner.next_token() == 'so'
    assert not scanner.has_more_tokens()
