"""Tests for the :mod:`campy.datastructures.lexicon` module."""
from campy.datastructures.lexicon import Lexicon


def test_create_lexicon(tmp_path):
    f = tmp_path / 'small.lex'
    f.write_text(
        "aardvark\n"
        "balloon\n"
    )
    print(str(f) )
    # TODO(sredmond): Move away from Unix-specific dictionary.
    lex = Lexicon(file=str(f))
    assert 'aardvark' in lex

    it = iter(lex)
    assert 'aardvark' in it
    assert next(it) == 'balloon'

