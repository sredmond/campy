"""Tests for the :mod:`campy.graphics.gcolor` module."""
from campy.graphics.gcolor import Pixel, GColor

def test_empty_pixel_is_black():
    empty = Pixel()
    assert empty.red == 0x00
    assert empty.green == 0x00
    assert empty.blue == 0x00
    assert empty.alpha == 0xFF

def test_make_color_by_positional_arguments():
    cardinal = Pixel(168, 0, 59)
    assert cardinal.red == 168
    assert cardinal.green == 0
    assert cardinal.blue == 59

def test_make_color_with_alpha():
    cardinal = Pixel(168, 0, 59, 0x7F)
    assert cardinal.alpha == 0x7F

def test_make_color_with_only_some_channels():
    pixel = Pixel(168, 41)
    assert pixel.red == 168
    assert pixel.green == 41
    assert pixel.blue == 0
    assert pixel.alpha == 0xFF

def test_make_color_with_only_some_channels_by_keyword():
    cardinal = Pixel(blue=59, red=168)
    assert cardinal.red == 168
    assert cardinal.green == 0
    assert cardinal.blue == 59

def test_set_red_channel():
    cardinal = Pixel(168, 0, 59)
    cardinal.red = 41
    assert cardinal.red == 41

def test_set_green_channel_repeatedly():
    cardinal = Pixel(168, 0, 59)
    for i in range(256):
        assert cardinal.green == i
        cardinal.green += 1

def test_unpack_rgb():
    cardinal = Pixel(168, 0, 59)
    red, green, blue = cardinal.rgb()
    assert red == 168
    assert green == 0
    assert blue == 59

def test_unpack_argb():
    cardinal = Pixel(168, 0, 59, 0x41)
    alpha, red, green, blue = cardinal.argb()
    assert alpha == 0x41
    assert red == 168
    assert green == 0
    assert blue == 59
