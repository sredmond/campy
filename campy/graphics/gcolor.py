"""Classes for manipulating colors and pixels.

A :class:`GColor` is a heavy object representing an abstract color. It
should be thought of as an opaque data type that can be initialized from any of
several possible representations, and serialized to any of those representations.

A :class:`Pixel` represents a single pixel of an image, and is stored much more
efficiently. A Pixel can represent an (R, G, B) triplet or an (R, G, B, A)
quadruplet.

The main difference between a :class:`Pixel` and a :class:`GColor` is that a
:class:`Pixel` is basically an efficiently stored integer representing the alpha,
red, green, and blue channels of the pixel, whereas a :class:`GColor` has no
alpha channel and has many more utility methods attached.

Additionally, a :class:`Pixel` is mutable, whereas a :class:`GColor` is immutable.
"""
# TODO(sredmond): Rethink Pixel mutability, since changes won't propagate to
# Pixel containers.
from campy.system.error import CampyException

import math


class Pixel:
    """A :class:`Pixel` represents a single, possibly-transparent pixel from an image.

    Students will likely never have to directly instantiate Pixels, and will instead
    likely just modify provided Pixels.

    Pixels can be modified directly by getting or setting their properties.

    To change the values of channels of a pixel::

        cardinal = Pixel(168, 0, 59)
        print(cardinal.red)  # => 168

        cardinal.red = 223
        cardinal.green = 202
        cardinal.blue = 151

        red, green, blue = cardinal.rgb()

    To modify the alpha channel of a pixel, use the same syntax::

        opaque = Pixel(168, 0, 59)
        opaque.alpha //= 2
        alpha, red, green, blue = opaque.argb()

    The alpha channel of a pixel defaults to 255 if not otherwise set.

    When setting values for these channels, it is required to supply an integer between
    0 and 255, inclusive.
    """
    # TODO(sredmond): Document which methods produce pixels.
    # TODO(sredmond): Revisit subclassing from int.

    # Tell Python to disallow dynamic attribute creation except for self._value
    __slots__ = ['_value']

    def __init__(self, red=0x00, green=0x00, blue=0x00, alpha=0xFF):
        """Create a new Pixel by channels.

        The red, green, blue, and alpha channels can be independently set.

        To create a default (black) pixel::

            default = Pixel()

        To create a pixel with given red, green, and blue values::

            cardinal = Pixel(168, 0, 59)

        To create a red pixel::

            red = Pixel(red=0xFF)

        To create a cyan (half-blue, half-green) pixel::

            cyan = Pixel(green=0x7F, blue=0x7F)

        To create a semi-transparent green pixel::

            pixel = Pixel(green=0xFF, alpha=0x7F)

        :param red: The value of the red channel between 0 and 255.
        :param green: The value of the green channel between 0 and 255.
        :param blue: The value of the blue channel between 0 and 255.
        :param alpha: The value of the alpha channel between 0 and 255.
        """

        # NOTE(sredmond): Since int is immutable, we can't set ourself (or can we?!)
        # TODO(sredmond): Check that the supplied arguments are within valid bounds.
        self._value = (alpha << 24) | (red << 16) | (green << 8) | blue

    @property
    def alpha(self):
        """Get or set this :class:`Pixel`'s alpha channel.

        Usage::

            pixel = Pixel(168, 0, 59)
            pixel.alpha = 127
            print(pixel.alpha)
        """
        # TODO(sredmond): The C++ libraries claim that you "have to & a second time
        # because of sign-extension on >> shift." That's because if the value is
        # stored in something like an int_32, some values of alpha might mean that
        # the integer is negative, so right-shifting would carry over that negativity.
        # This shift doesn't apply in Python, since ints are unbounded.
        return (self._value >> 24) & 0xFF

    @property
    def red(self):
        """Get or set this :class:`Pixel`'s red channel.

        Usage::

            pixel = Pixel(168, 0, 59)
            pixel.red = 41
            print(pixel.red)
        """
        return (self._value >> 16) & 0xFF

    @property
    def green(self):
        """Get or set this :class:`Pixel`'s green channel.

        Usage::

            pixel = Pixel(168, 0, 59)
            pixel.green = 41
            print(pixel.green)
        """
        return (self._value >> 8) & 0xFF

    @property
    def blue(self):
        """Get or set this :class:`Pixel`'s blue channel.

        Usage::

            pixel = Pixel(168, 0, 59)
            pixel.blue = 41
            print(pixel.blue)
        """
        return self._value & 0xFF

    @alpha.setter
    def alpha(self, new_alpha):
        self._value &= ~(0xFF << 24)
        self._value |= new_alpha << 24

    @red.setter
    def red(self, new_red):
        self._value &= ~(0xFF << 16)
        self._value |= (new_red << 16)

    @green.setter
    def green(self, new_green):
        self._value &= ~(0xFF << 8)
        self._value |= new_green << 8

    @blue.setter
    def blue(self, new_blue):
        self._value &= ~0xFF
        self._value |= new_blue

    def rgb(self):
        """Return a 3-tuple of this Pixel's channels, not including alpha transparency.

        The elements of the tuple correspond to red, green, and blue.

        To extract all color channels at once::

            pixel = Pixel(168, 0, 59)
            red, green, blue = pixel.rgb()
        """
        return self.red, self.green, self.blue

    def argb(self):
        """Return a 4-tuple of this Pixel's channels, including alpha transparency.

        The elements of the tuple correspond to alpha, red, green, and blue.

        To extract all channels at once::

            pixel = Pixel(168, 0, 59)
            alpha, red, green, blue = pixel.argb()
        """
        return self.alpha, self.red, self.green, self.blue

    def __str__(self):
        return "Pixel(red={self.red}, green={self.green}, blue={self.blue})".format(self=self)


class _ColorResolverMeta(type):
    """Metaclass to override attribute access for :class:`GColor`."""
    def __getattr__(cls, attr):
        """Implement ``self.attr`` if normal attribute lookup fails.

        As a metaclass, this will modify attribute lookup on its derived class.
        """
        # TODO(sredmond): Optionally also remove non-ASCII characters.
        # TODO(Sredmond): "Did you mean... GColor.BLUE" with config flag
        attr = attr.strip().lower().replace(' ', '').replace('_', '').replace('-', '')
        if attr in COLORS:
            # TODO(sredmond): This constructs a new GColor each time.
            return cls.normalize(COLORS[attr])
        raise AttributeError("type object '{}' has no attribute '{}'".format(cls.__name__, attr))


class GColor(metaclass=_ColorResolverMeta):
    """A :class:`GColor` represents a color.

    Colors can be represented in many different forms.

    (1) As a three-integer tuple, such as as (168, 0, 59), with each entry in the range 0..255
    (2) As a three-character hex string prefaced with '#', such as "#83E"
    (3) As a six-character hex string prefaced with '#', such as "#A8003B"
    (4) As a three-character hex string prefaced with '0x', such as "0x83E"
    (5) As a six-character hex string prefaced with '0x', such as "0xA8003B"
    (6) As a case-insensitive name, such as "red" or "LiGhT sKy BlUe"
    (7) As a GColor constant, such as GColor.RED or GColor.LIGHT_SKY_BLUE.
    (8) As a 24-bit integer, representing the red, green, and blue channels.
    (9) As a Pixel object, such as Pixel(168, 0, 59).

    The canonical (internal) form for a GColor is as three integers between 0 and 255.

    A :class:`GColor` should be thought of as immutable.
    """

    def __init__(self, red, green, blue):
        self._red = red
        self._green = green
        self._blue = blue

    @classmethod
    def normalize(cls, color):
        """Normalize a color description provided by an end user."""
        if isinstance(color, GColor):
            return color

        if isinstance(color, int):
            # Mode (8): 24-bit integer.
            red = (color >> 16) & 0xFF
            green = (color >> 8) & 0xFF
            blue = color & 0xFF
            return cls(red, green, blue)

        elif isinstance(color, (tuple, list)):
            # Mode (1): 3-element tuple.
            if len(color) != 3:
                raise CampyException  # TODO(sredmond): Test this color!

            red, green, blue = color
            return cls(red, green, blue)

        elif isinstance(color, str):
            color = color.strip()
            if color.startswith('#'):
                value = int(color[1:], 16)
                red = (value >> 16) & 0xFF
                green = (value >> 8) & 0xFF
                blue = value & 0xFF
                return cls(red, green, blue)
            elif color.startswith('0x'):
                value = int(color[2:], 16)
                red = (value >> 16) & 0xFF
                green = (value >> 8) & 0xFF
                blue = value & 0xFF
                return cls(red, green, blue)

            color = color.lower().replace(' ', '').replace('_', '').replace('-', '')
            if color in COLORS:
                value = COLORS[color]
                red = (value >> 16) & 0xFF
                green = (value >> 8) & 0xFF
                blue = value & 0xFF
                return cls(red, green, blue)
            else:
                raise CampyException  # OH NO
        elif isinstance(color, Pixel):  # Discard the alpha information from a pixel.
            return cls(color.red, color.green, color.blue)
        else:
            raise CampyException  # OH NO

        return Color.BLACK

    @property
    def r(self):
        return self._red

    @property
    def g(self):
        return self._green

    @property
    def b(self):
        return self._blue

    @property
    def rgb(self):
        return self.r, self.g, self.b

    @property
    def hex(self):
        # TODO(sredmond): This is SO dumb. Fix this code!
        r = hex(self._red).replace('0x', '').zfill(2)
        g = hex(self._green).replace('0x', '').zfill(2)
        b = hex(self._blue).replace('0x', '').zfill(2)
        # Probably something like: #{:02x}{:02x}{:02x}
        return '#{}{}{}'.format(r,g,b).upper()

    @property
    def name(self):
        """Return a human-readable name for this color."""
        return "Nearly <color>"

    @classmethod
    def darken(cls, color):
        """Construct a new color at 2/3 of the current color's red, green, and blue values, rounded down."""
        if not isinstance(color, cls):
            color = cls.normalize(color)
        return cls(int(2 * color.r / 3), int(2 * color.g / 3), int(2 * color.b / 3))

    @classmethod
    def brighten(cls, color):
        if not isinstance(color, cls):
            color = cls.normalize(color)
        new_red = math.ceil(color.r + (255 - color.r) / 3)
        new_green = math.ceil(color.g + (255 - color.g) / 3)
        new_blue = math.ceil(color.b + (255 - color.b) / 3)
        return cls(new_red, new_green, new_blue)

    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b


COLORS = {
    'aliceblue': 0xF0F8FF,
    'antiquewhite': 0xFAEBD7,
    'aqua': 0x00FFFF,
    'aquamarine': 0x7FFFD4,
    'azure': 0xF0FFFF,
    'beige': 0xF5F5DC,
    'bisque': 0xFFE4C4,
    'black': 0x000000,
    'blanchedalmond': 0xFFEBCD,
    'blue': 0x0000FF,
    'blueviolet': 0x8A2BE2,
    'brown': 0xA52A2A,
    'burlywood': 0xDEB887,
    'cadetblue': 0x5F9EA0,
    'chartreuse': 0x7FFF00,
    'chocolate': 0xD2691E,
    'coral': 0xFF7F50,
    'cornflowerblue': 0x6495ED,
    'cornsilk': 0xFFF8DC,
    'crimson': 0xDC143C,
    'cyan': 0x00FFFF,
    'darkblue': 0x00008B,
    'darkcyan': 0x008B8B,
    'darkgoldenrod': 0xB8860B,
    'darkgray': 0xA9A9A9,
    'darkgreen': 0x006400,
    'darkgrey': 0xA9A9A9,
    'darkkhaki': 0xBDB76B,
    'darkmagenta': 0x8B008B,
    'darkolivegreen': 0x556B2F,
    'darkorange': 0xFF8C00,
    'darkorchid': 0x9932CC,
    'darkred': 0x8B0000,
    'darksage': 0x598556,
    'darksalmon': 0xE9967A,
    'darkseagreen': 0x8FBC8F,
    'darkslateblue': 0x483D8B,
    'darkslategray': 0x2F4F4F,
    'darkslategrey': 0x2F4F4F,
    'darkturquoise': 0x00CED1,
    'darkviolet': 0x9400D3,
    'deeppink': 0xFF1493,
    'deepskyblue': 0x00BFFF,
    'dimgray': 0x696969,
    'dimgrey': 0x696969,
    'dodgerblue': 0x1E90FF,
    'firebrick': 0xB22222,
    'floralwhite': 0xFFFAF0,
    'forestgreen': 0x228B22,
    'fuchsia': 0xFF00FF,
    'gainsboro': 0xDCDCDC,
    'ghostwhite': 0xF8F8FF,
    'gold': 0xFFD700,
    'goldenrod': 0xDAA520,
    'gray': 0x808080,
    'green': 0x008000,
    'greenyellow': 0xADFF2F,
    'grey': 0x808080,
    'honeydew': 0xF0FFF0,
    'hotpink': 0xFF69B4,
    'indianred': 0xCD5C5C,
    'indigo': 0x4B0082,
    'ivory': 0xFFFFF0,
    'khaki': 0xF0E68C,
    'lavender': 0xE6E6FA,
    'lavenderblush': 0xFFF0F5,
    'lawngreen': 0x7CFC00,
    'lemonchiffon': 0xFFFACD,
    'lightblue': 0xADD8E6,
    'lightcoral': 0xF08080,
    'lightcyan': 0xE0FFFF,
    'lightgoldenrodyellow': 0xFAFAD2,
    'lightgray': 0xD3D3D3,
    'lightgreen': 0x90EE90,
    'lightgrey': 0xD3D3D3,
    'lightpink': 0xFFB6C1,
    'lightsage': 0xBCECAC,
    'lightsalmon': 0xFFA07A,
    'lightseagreen': 0x20B2AA,
    'lightskyblue': 0x87CEFA,
    'lightslategray': 0x778899,
    'lightslategrey': 0x778899,
    'lightsteelblue': 0xB0C4DE,
    'lightyellow': 0xFFFFE0,
    'lime': 0x00FF00,
    'limegreen': 0x32CD32,
    'linen': 0xFAF0E6,
    'magenta': 0xFF00FF,
    'maroon': 0x800000,
    'mediumaquamarine': 0x66CDAA,
    'mediumblue': 0x0000CD,
    'mediumorchid': 0xBA55D3,
    'mediumpurple': 0x9370DB,
    'mediumseagreen': 0x3CB371,
    'mediumslateblue': 0x7B68EE,
    'mediumspringgreen': 0x00FA9A,
    'mediumturquoise': 0x48D1CC,
    'mediumvioletred': 0xC71585,
    'midnightblue': 0x191970,
    'mintcream': 0xF5FFFA,
    'mistyrose': 0xFFE4E1,
    'moccasin': 0xFFE4B5,
    'navajowhite': 0xFFDEAD,
    'navy': 0x000080,
    'oldlace': 0xFDF5E6,
    'olive': 0x808000,
    'olivedrab': 0x6B8E23,
    'orange': 0xFFA500,
    'orangered': 0xFF4500,
    'orchid': 0xDA70D6,
    'palegoldenrod': 0xEEE8AA,
    'palegreen': 0x98FB98,
    'paleturquoise': 0xAFEEEE,
    'palevioletred': 0xDB7093,
    'papayawhip': 0xFFEFD5,
    'peachpuff': 0xFFDAB9,
    'peru': 0xCD853F,
    'pink': 0xFFC0CB,
    'plum': 0xDDA0DD,
    'powderblue': 0xB0E0E6,
    'purple': 0x800080,
    'red': 0xFF0000,
    'rosybrown': 0xBC8F8F,
    'royalblue': 0x4169E1,
    'saddlebrown': 0x8B4513,
    'sage': 0x87AE73,
    'salmon': 0xFA8072,
    'sandybrown': 0xFAA460,
    'seagreen': 0x2E8B57,
    'seashell': 0xFFF5EE,
    'sienna': 0xA0522D,
    'silver': 0xC0C0C0,
    'skyblue': 0x87CEEB,
    'slateblue': 0x6A5ACD,
    'slategray': 0x708090,
    'slategrey': 0x708090,
    'snow': 0xFFFAFA,
    'springgreen': 0x00FF7F,
    'steelblue': 0x4682B4,
    'tan': 0xD2B48C,
    'teal': 0x008080,
    'thistle': 0xD8BFD8,
    'tomato': 0xFF6347,
    'turquoise': 0x40E0D0,
    'violet': 0xEE82EE,
    'wheat': 0xF5DEB3,
    'white': 0xFFFFFF,
    'whitesmoke': 0xF5F5F5,
    'yellow': 0xFFFF00,
    'yellowgreen': 0x9ACD32
}

# Overrides from the Stanford ACM libraries, whose color
# definitions may be slightly different.
COLORS.update({
    "black": 0x000000,
    "darkgray": 0x595959,
    "darkgrey": 0x595959,
    "gray": 0x999999,
    "grey": 0x999999,
    "lightgray": 0xBFBFBF,
    "lightgrey": 0xBFBFBF,
    "orange": 0xFFC800,
    "pink": 0xFFAFAF,
})
