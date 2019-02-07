"""Tests for the :mod:`campy.graphics.gwindow` module."""
from campy.graphics.gwindow import Alignment, Region, CloseOperation, GWindow, pause, screen_width, screen_height, exit_graphics


def test_alignment_center_exists():
    assert Alignment.CENTER in Alignment

def test_region_south_exists():
    assert Region.SOUTH in Region

def test_close_operation_do_nothing_exists():
    assert CloseOperation.DO_NOTHING in CloseOperation

# TODO(sredmond): Add WAY more tests.
