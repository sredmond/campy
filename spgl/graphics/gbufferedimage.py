"""
"""

GBUFFEREDIMAGE_DEFAULT_DIFF_PIXEL_COLOR = 0xdd00dd
_WIDTH_HEIGHT_MAX = 65535

def _char_to_hex(ch):
     return ord('0') <= ch <= ord('9') ? (ch - ord('0')) : (ch - ord('a') + 10)

class GBufferedImage(GInteractor):
    WIDTH_HEIGHT_MAX = 65535

    @classmethod
    def create_rgb_pixel(cls, red, green, blue):
        if 0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255:
            return (red << 16 & 0xff0000) | (green << 8 & 0x00ff00) | (blue & 0x0000ff)
        error("RGB values must be between 0-255")

    @classmethod
    def get_alpha(cls, argb):
        pass

    @classmethod
    def get_red(cls, rgb):
        pass

    @classmethod
    def get_green(cls, rgb):
        pass

    @classmethod
    def get_blue(cls, rgb):
        pass

    @classmethod
    def get_red_green_blue(cls, rgb):
        pass

    def __init__(self):
        self.

    def get_bounds(self):
        pass

    def get_type(self):
        pass

    def clear(self):
        pass

    def count_diff_pixels(self, other):
        pass

    def diff(self, other, diff_color=GBUFFEREDIMAGE_DEFAULT_DIFF_PIXEL_COLOR):
        pass

    def fill(self, TODO):
        pass

    def fill_region(self, x, y, width, height, TODO):
        pass

    def from_grid(self, grid):
        pass

    def get_height(self):
        pass

    def get_rgb(self, x, y):
        pass

    def get_rgb_string(self, x, y):
        pass

    def get_width(self):
        pass

    def in_bounds(self, x, y):
        pass

    def load(self, filename):
        pass

    def resize(self, width, height, retain=True):
        pass

    def save(self, filename):
        pass

    def set_rgb(x, y, TODO):
        pass

    def to_grid(self):
        pass



    def __str__(self):
        pass
