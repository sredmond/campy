"""Tests for the :mod:`campy.graphics.gfilechooser` module."""
from campy.graphics.gfilechooser import GFileChooser

# TODO(sredmond): Find a way to unit test these modules.

def test_open_dialog():
    assert False
    print(GFileChooser.show_open_dialog())
    print(GFileChooser.show_open_dialog('/Users/sredmond/Desktop/'))
    # print(GFileChooser.show_open_dialog('/'))
    # print(GFileChooser.show_open_dialog('~/Desktop'))
    print(GFileChooser.show_open_dialog('/not/a/dir'))
    print(GFileChooser.show_open_dialog('/no/trailing/slash/'))
    print(GFileChooser.show_open_dialog('../../'))


def test_save_dialog():
    assert False
    print(GFileChooser.show_save_dialog())
    print(GFileChooser.show_save_dialog('/'))
    print(GFileChooser.show_save_dialog('~/Desktop'))
    print(GFileChooser.show_save_dialog('/not/a/dir'))
    print(GFileChooser.show_save_dialog('/no/trailing/slash/'))
    print(GFileChooser.show_save_dialog('../../'))
