"""Friendly fonts.

A :class:`GFont` provides a convenient way to define fonts.

To get the current platform's default font::

    font = GFont.default()

To get a font from a text description in the form FAMILY-STYLE or
FAMILY-STYLE-MODIFIERS::

    font1 = GFont.parse('Helvetica-12')
    font2 = GFont.parse('Times New Roman-24-bold')
    font3 = GFont.parse('Verdana-11-bold-italic')

For finer grained control, use the constructor directly.

    font1 = GFont.parse('Helvetica', 12)
    font2 = GFont.parse('Times New Roman', 24, weight=True)
    font3 = GFont.parse('Verdana', 11, weight=True, slant=True)

To access a system font by name, such as the macOS alert header::

    font = GFont.system('systemAlertHeaderFont')

Note that a given system font may not be accessible on all platforms.

Once you have a :class:`GFont`, you can access its family, size, weight, and
slant. You can also access font metrics directly, such as the font's ascent,
the font's descent, the font's line spacing, and whether the font is
fixed-width. These are properties that apply to the font as a whole, and not
to any particular text rendered in this font.

To get the width of a particular string, use :func:`GFont.measure`::

    font = GFont.default()
    width = font.measure('Hello World!')
    print(width)  # => 77
"""
import campy.private.platform as _platform

import logging

# Module-level logger.
logger = logging.getLogger(__name__)


class GFont:
    # TODO(sredmond): Support underline and overstrike.

    # TODO(sredmond): Think harder about which of these should be required and
    # which should be optional.
    def __init__(self, family, size, weight=False, slant=False):
        self._family = family
        self._size = size
        self._weight = weight
        self._slant = slant

        metrics = _platform.Platform().gfont_get_font_metrics(self)
        self._ascent = metrics['ascent']
        self._descent = metrics['ascent']
        self._linespace = metrics['ascent']
        # TODO(sredmond): Push the actual value of 1 back down into the platform abstraction.
        self._fixed = metrics['fixed'] == '1'

    @classmethod
    def parse(cls, description):
        """Parse a description into a font.

        A description can be either FAMILY-SIZE or FAMILY-SIZE-MODIFIERS, where
        FAMILY is the name of a font family available on the current system,
        SIZE is a positive integer representing the font size (in points, not
        in pixels), and MODIFIERS is either the string "bold", "bold-italic",
        or "italic". Examples of valid font descriptions include::


            Helvetica-12
            Dialog-13
            Courier-18
            Times New Roman-24-bold
            Times-16-italic
            Verdana-11-bold-italic

        This method returns None if no font could be parsed.
        """
        # TODO(sredmond): Redesign the allowed description scheme to handle a
        # broader set of descriptions. Notably, fonts with dashes in their
        # names are currently impossible to specify. I don't know of any fonts
        # with that property, but it's still an unnecessary restriction.
        pieces = description.split('-')
        if len(pieces) < 2 or len(pieces) > 4:
            logger.warning('Unable to parse font description {!r} into an appropriate number of pieces.'.format(description))
            return
        family = pieces[0]
        size = int(pieces[1])
        weight = 'bold' in pieces[2:]
        slant = 'italic' in pieces[2:]
        return cls(family, size, weight, slant)

    @classmethod
    def system(cls, font_name):
        logger.info('Loading a font from a system name may not be portable.')
        attributes = _platform.Platform().gfont_attributes_from_system_name(font_name)
        return cls(family=attributes['family'], size=attributes['size'],
                   weight=bool(attributes['weight']), slant=bool(attributes['slant']))

    # TODO(sredmond): Also support X Font Descriptors, which is something like:
    # -*-family-weight-slant-*--*-size-*-*-*-*-charset

    @classmethod
    def default(cls):
        attributes = _platform.Platform().gfont_default_attributes()
        return cls(family=attributes['family'], size=attributes['size'],
                   weight=attributes['weight'] != 'normal', slant=attributes['slant']  != 'roman')
    @property
    def family(self):
        return self._family

    @property
    def size(self):
        return self._size

    @property
    def weight(self):
        return self._weight

    @property
    def slant(self):
        return self._slant

    @property
    def ascent(self):
        return self._ascent

    @property
    def descent(self):
        return self._descent

    @property
    def linespace(self):
        return self._linespace

    @property
    def fixed(self):
        return self._fixed

    def measure(self, text):
        return _platform.Platform().gfont_measure_text_width(self, text)

    def __str__(self):
        """Implement `str(self)`."""
        out = '{family}-{size}'.format(family=self.family, size=self.size)
        if self.weight:
            out += '-bold'
        if self.slant:
            out += '-italic'
        return out

    def __repr__(self):
        """Implement `repr(self)`."""
        return 'GFont(family={family}, size={size}, weight={weight}, slant={slant})'.format(
            family=self.family,
            size=self.size,
            weight='bold' if self.weight else 'normal',
            slant='italic' if self.slant else 'roman'
        )
