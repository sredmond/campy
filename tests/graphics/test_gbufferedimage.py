"""Tests for the :mod:`campy.graphics.gbufferedimage` module."""
from campy.graphics.gbufferedimage import GBufferedImage


def test_create_empty_image():
    image = GBufferedImage(width=50, height=80, bg_color=0xFFFFFF)
    assert True


def test_resize_image():
    image = GBufferedImage(width=50, height=80, bg_color=0xFFFFFF)
    image.resize(100, 800)
    assert True


def test_fill_image():
    image = GBufferedImage(width=50, height=80, bg_color=0xFFFFFF)
    image.fill(0xFF00FF)
    assert True


def test_load_image_from_file():
    image = GBufferedImage.load_from_file('/Users/sredmond/Pictures/wallpapers/8to5/car.jpg')
    assert True
