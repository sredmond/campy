"""
"""
import spgl.datastructures.grid as _grid
import spgl.gui.ginteractors as _ginteractors
import spgl.graphics.gcolor as _gcolor
import spgl.graphics.gtypes as _gtypes
import spgl.private.platform as _platform
import spgl.io.base64helper as _base64helper


GBUFFEREDIMAGE_DEFAULT_DIFF_PIXEL_COLOR = 0xdd00dd

# def _char_to_hex(ch):
#      return ord('0') <= ch <= ord('9') ? (ch - ord('0')) : (ch - ord('a') + 10)

class GBufferedImage(_ginteractors.GInteractor):
    WIDTH_HEIGHT_MAX = 65535

    @classmethod
    def load_from_file(cls, filename):
        inst = cls()
        inst.load(filename)
        return inst

    @property
    def bounds(self):
        return _gtypes.GRectangle(self.x, self.y, self.width, self.height)

    def clear(self):
        self.fill(self.bg_color)

    def count_diff_pixels(self, other, bounds=None):
        # TODO(sredmond): This API differs from the CPP lib.
        # TODO(sredmond): Include bounds
        min_width = min(self.width, other.width)
        min_height = min(self.height, other.height)
        overlap = min_width * min_height
        diff_pixel_count = (self.width * self.height - overlap) + (other.width * other.height - overlap)
        for y in range(min_height):
            for x in range(min_width):
                if self.pixels.get(y, x) != other.pixels.get(y, x):
                    diff_pixel_count += 1
        return diff_pixel_count

    def diff(self, other, diff_color=GBUFFEREDIMAGE_DEFAULT_DIFF_PIXEL_COLOR):
        pass

    def fill(self, color):
        # color = _gcolor.normalize(color)
        self.pixels.fill(color)
        _platform.Platform().gbufferedimage_fill(self, color) # TODO(get rgb value)
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
        # TODO(sredmond): Ensure file exists.
        result = _platform.Platform().gbufferedimage_load(self, filename)
        decoded = _base64helper.decode(result)
        self._pixel_string_to_grid(decoded)

    def resize(self, width, height, retain=True):
        pass

    def save(self, filename):
        pass

    def set_rgb(x, y, TODO):
        pass

    def to_grid(self):
        pass

    def _pixel_string_to_grid(self, decoded):
        # Read width (2B) and height (2B)
        # TODO(sredmond): Seriously check this bit fiddling
        w = (decoded[0] << 8) | decoded[1];
        h = (decoded[2] << 8) | decoded[3];
        if w != self.pixels.width() or h != self.pixels.height():
            self.pixels.resize(h, w, retain=False)

        # Check that we received approximately the right length of bytes.
        expected = (w * h * 3) + 4
        actual = len(decoded)
        if actual != decoded:
            print('Expected {} but saw {} bytes'.format(expected, actual))
            # TODO(sredmond): Abort abort
            import sys
            sys.exit(1)

        pixels = []
        for red, green, blue in zip(decoded[4::3], decoded[5::3], decoded[6::3]):
            pixels.append(Pixel(red=red, green=green, blue=blue))

        i = 0
        for row in range(h):
            for col in range(w):
                self.pixels.set(row, col, pixels[i])
                i += 1

        self.width = pixels.width
        self.height = pixels.height

    # "Private" constructor, called by class method constructors.
    def __init__(self, x=0, y=0, width=1, height=1, bg_color=0x000000):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.pixels = _grid.Grid()

    def __str__(self):
        return 'GBufferedImage()'

if __name__ == '__main__':
    from spgl.graphics.gwindow import GWindow
    gw = GWindow()
    # gbi = GBufferedImage(width=50, height=80, bg_color=0xFFFFFF)
    # gbi.resize(100, 800)
    # gbi.fill(0xFFFFFF)
    gbi = GBufferedImage.load_from_file('/Users/sredmond/Pictures/wallpapers/8to5/car.jpg')
    gw.add(gbi)
    input('>')
