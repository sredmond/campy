"""Graphical representation of an image.

To display a centered :class:`GImage` of the Stanford tree::

    window = GWindow()
    tree = GImage("StanfordTree.gif")
    x = (window.width - tree.width) / 2
    y = (window.height - tree.height) / 2
    window.add(tree, x, y)

The above code assumes that you have a file named ``StanfordTree.gif`` in
the current directory.

The search for matching image files begins in the current directory and,
failing that, searches an ``images/`` subdirectory relative to the calling script.
"""
# TODO(sredmond): Have a environmental variable for a custom subdirectory.
# TODO(sredmond): When would you use a GImage over a GBufferedImage?
import campy.private.platform as _platform
import campy.graphics.gobjects as _gobjects
from campy.graphics.gcolor import Pixel, GColor
import campy.graphics.gtypes as _gtypes
from campy.system.error import CampyException


# TODO(sredmond): Find some way to set pixels all at once instead of buffering at the platform levek.
# Have both these classes inherit from the appropriate abc.

class GImage(_gobjects.GObject):
    class ImageRow:
        # This is an awkward implementation for sure.
        def __init__(self, parent, row, width):
            self._parent = parent
            self._row = row
            self._width = width

        def __iter__(self):
            for c in range(self._width):
                yield self[c]

        def __getitem__(self, col):
            return _platform.Platform().gimage_get_pixel(self._parent, self._row, col)

        def __setitem__(self, col, color):
            # TODO(sredmond): Normalize this pixel.
            color = GColor.normalize(color)
            _platform.Platform().gimage_set_pixel(self._parent, self._row, col, color.rgb)


    # TODO(sredmond): When an image is just loaded and displayed and never modified, don't buffer it.
    def __init__(self, filename):
        super().__init__()
        self._filename = filename

        # Try to use the supplied path to find the complete path to the image.
        # TODO(sredmond): Accessing the backend like this will spawn a Tk master,
        # even if we don't plan on adding it anywhere. See if I can delay the
        # spawning of a Tk app until necssary (in cases where Pillow already
        # provides the image reading/loading/previewing).
        self._path = _platform.Platform().image_find(filename)
        if not self._path:
            raise CampyException('Unable to locate the image at {!r}.'.format(self._filename))


        self._data, self._width, self._height= _platform.Platform().image_load(filename)

        # TODO(sredmond): The JBE returns the size after the GImage construction.
        # Sync that API with the Tk one.


    @classmethod
    def blank(cls, width, height, background=GColor.WHITE):
        pass


    @classmethod
    def from_file(cls, filename):
        """Initialize a new image from the given file.

        The image file should either exist in the current directory or in a
        subdirectory named ``images/``.

        :param filename: the name of the image file to load.
        """
        return cls(filename)


    @classmethod
    def from_data(cls):
        pass

    @property
    def filename(self):
        """Get this :class:`GImage`'s filename."""
        return self._filename

    def __getitem__(self, row):
        # TODO(sredmond): Replace these modifiers with a Grid.
        return GImage.ImageRow(self, row, self._width)

    def __setitem__(self, row):
        return GImage.ImageRow(self, row, self._width)

    def __iter__(self):
        for r in range(self._height):
            yield GImage.ImageRow(self, r, self._width)

    def preview(self):
        _platform.Platform().gimage_preview(self)

    @property
    def bounds(self):
        """Get the bounding box for this :class:`GImage`."""
        if self._transformed: return _platform.Platform().gobject_get_bounds(self)
        return _gtypes.GRectangle(self.x, self.y, self._width, self._height)

    def __str__(self):
        return 'GImage({self.width}x{self.height}, name={!r})'.format(self.filename)
