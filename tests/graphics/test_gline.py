"""Tests for the :class:`campy.graphics.gobjects.GLine` class."""
from campy.graphics.gobjects import GLine

def test_create_line():
    line = GLine(0, 1, 2, 3)
    assert line.start == (0, 1)
    assert line.end == (2, 3)

def test_create_horizontal_line():
    pass

def test_create_vertical_line():
    pass

def test_create_line_on_diagonal():
    pass

def test_create_backwards_line():
    pass

def test_get_start_point():
    pass

def test_start_point_is_gpoint():
    pass

def test_start_point_is_unpackable():
    pass

def test_set_start_point_from_tuple():
    pass

def test_set_start_point_from_gpoint():
    pass

def test_get_end_point():
    pass

def test_end_point_is_gpoint():
    pass

def test_end_point_is_unpackable():
    pass

def test_set_end_point_from_tuple():
    pass

def test_set_end_point_from_gpoint():
    pass




# TODO(sredmond): Add tests that check proper interfacing with a GWindow.
