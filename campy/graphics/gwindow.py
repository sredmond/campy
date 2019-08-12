"""Provide a :class:`GWindow` that supports drawing graphical objects on screen."""
from collections import namedtuple as _nt
import enum as _enum
import math

import campy.graphics.gtypes as _gtypes
import campy.graphics.gobjects as _gobjects
import campy.graphics.gtypes as _gtypes
import campy.private.platform as _platform
import campy.graphics.gcolor as _gcolor


@_enum.unique
class Alignment(_enum.Enum):
    """Horizontal alignment within a region."""
    LEFT = 0
    CENTER = 1
    RIGHT = 2


@_enum.unique
class Region(_enum.Enum):
    """Regions of a :class:`GWindow`."""
    CENTER = 0
    EAST = 1
    NORTH = 2
    SOUTH = 3
    WEST = 4


@_enum.unique
class CloseOperation(_enum.Enum):
    """Actions to take upon closure of a GWindow.

    Currently unused.
    """
    DO_NOTHING = 0
    HIDE = 1
    DISPOSE = 2
    EXIT = 3


# TODO(sredmond): There used to be a lot of fluff around copying a GWindow.
# It seems like that was all misguided - Python should handle the creation
# of these objects. However, keep an eye out for unexpected copying errors.
class GWindow:
    """A Graphics Window that supports simple graphics.

    Each GWindow consists of two layers. The background layer
    provides a surface for drawing static pictures that involve no animation.
    Graphical objects drawn in the background layer are persistent and do
    not require the client to update the contents of the window.  The
    foreground layer contains graphical objects that are redrawn as necessary.

    The GWindow class includes several methods that draw
    lines, rectangles, and ovals on the background layer without making
    use of the facilities of the gobjects.h interface.  For
    example, the following program draws a diamond, rectangle, and oval
    at the center of the window::

        gw = gwindow.GWindow
        print("This program draws a diamond, rectangle, and oval.")
        width = gw.getWidth()
        height = gw.getHeight()
        gw.drawLine(0, height / 2, width / 2, 0);
        gw.drawLine(width / 2, 0, width, height / 2);
        gw.drawLine(width, height / 2, width / 2, height);
        gw.drawLine(width / 2, height, 0, height / 2);
        gw.setColor("BLUE");
        gw.fillRect(width / 4, height / 4, width / 2, height / 2);
        gw.setColor("GRAY");
        gw.fillOval(width / 4, height / 4, width / 2, height / 2);
    """
    # The default width (in pixels) for a new GWindow.
    DEFAULT_WIDTH = 500

    # The default height (in pixels) for a new GWindow.
    DEFAULT_HEIGHT = 500

    # TODO(sredmond): Add a default color once the GColor library is fixed!
    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, visible=True, title="", color=None, top=None):
        """Create a new GWindow. Optionally, supply a specific width and height.

        Initial visibility, window title, marker color, and top compound can also
        be specified, but will default to reasonable values.

        To create a new GWindow of a default size::

            window = GWindow()

        To create a new GWindow with a specific size::

            window = GWindow(width=1280, height=800)

        To create a new GWindow with the default size but a specific title and marker color::

            window = GWindow(title="My Window", color=GColor.RED)

        :param width: The initial width of the GWindow.
        :param height: The initial height of the GWindow.
        :param visible: The default visibility of the GWindow.
        :param title: The displayed title on the GWindow.
        :param color: The marker color used to draw GObjects.
        :param top: The topmost GCompound in the GWindow.
        """
        self._width = width
        self._height = height
        self._visible = visible
        self._title = title
        # TODO(sredmond): Propagate the title to the backend constructor.

        if not color:
            color = _gcolor.GColor.BLACK
        self._color = color

        if not top:
            top = _gobjects.GCompound()
        self._top = top

        # TODO(sredmond): Isn't it a little silly to pass this object along with its attributes?
        _platform.Platform().gwindow_constructor(self, self._width, self._height, self._top)

    def close(self):
        """Close this GWindow."""
        # TODO(sredmond): Use the CloseOperation setting to determine how aggresive to close things down.
        _platform.Platform().gwindow_close(self)
        _platform.Platform().gwindow_delete(self)

    @property
    def width(self):
        """Get this GWindow's width (in pixels)."""
        # TODO(sredmond): If the actual GWindow's width changes (i.e. from a resize operation),
        # this value will be incorrect.
        return self._width

    @property
    def height(self):
        """Get this GWindow's height (in pixels)."""
        # TODO(sredmond): If the actual GWindow's height changes (i.e. from a resize operation),
        # this value will be incorrect.
        return self._height

    @property
    def visible(self):
        """Get or set this GWindow's visibility.

        TODO(sredmond): Document what, exactly, a GWindow's visibility means.

        Usage::

            window = GWindow()
            if not window.visible:
                window.visible = True
        """
        return self._visible

    @visible.setter
    def visible(self, flag):
        self._visible = flag
        _platform.Platform().gwindow_set_visible(flag, gw=self)

    @property
    def title(self):
        """Get or set this GWindow's title.

        Changing the title modifies the text in the top bar of the GWindow.

        Usage::

            window = GWindow()
            window.title = "My Title"
            print(window.title)
        """
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        _platform.Platform().gwindow_set_window_title(self, title)

    @property
    def color(self):
        """Get or set the marker color used for drawing.

        When accessing the color, retrieve a GColor object.

        TODO(sredmond): Document what sorts of colors can be supplied.
        """
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        # TODO(sredmond): Canonicalize this input color into a GColor.

    def draw_line(self, x0, y0, x1, y1):
        """Draw a line between the given coordinates.

        The line's color is this GWindow's current marker color.

        To draw a line from (0, 0) to (4, 1)::

            window = GWindow()
            window.draw_line(0, 0, 4, 1)

        To draw a line between two :class:`GPoint`s::

            window = GWindow()
            window.draw_line(*p0, *p1)

        :param x0: The x-coordinate of the starting point.
        :param y0: The y-coordinate of the starting point.
        :param x1: The x-coordinate of the ending point.
        :param y1: The y-coordinate of the ending point.
        """
        # TODO(sredmond): Multiple splat unpackings weren't supported until a recent version of Python.
        line = _gobjects.GLine(x0, y0, x1, y1)
        line.color = self.color
        self.draw(line)

    def draw_polar_line(self, x, y, r, theta):
        """Draw a line from an initial point with a given length and polar direction.

        The angle is measured in degrees counterclockwise from the positive x-axis.

        This function also returns the ending point of the constructed line.

        To draw a line of length 3 from the point (100, 100) at an angle of 60 degrees::

            window = GWindow()
            window.draw_polar_line(100, 100, 3, 60)

        :param x: The x-coordinate of the starting point.
        :param y: The y-coordinate of the starting point.
        :param r: The length of the line to draw.
        :param theta: The angle (measured from the positive x-axis) of the new line.
        :returns: The endpoint of the line.
        """
        # TODO(sredmond): Consider alternate ways to specify coordinates with a GPoint.
        x_end = x + r * math.cos(math.radians(theta))
        y_end = y - r * math.sin(math.radians(theta))  # Subtraction, since y decreases upwards.
        self.draw_line(x, y, x_end, y_end)
        return _gtypes.GPoint(x_end, y_end)

    def draw_oval(self, x, y, width, height):
        """Draw the outline of an oval.

        The oval's upper-left corner has coordinates given by (x, y), and size
        given by (width, height). The corner of an oval is the corner of the oval's
        bounding box.

        The color of the oval's outline will be this GWindow's current marker color.

        To draw an oval with an upper-left corner at (0, 0), a width of 300 pixels,
        and a height of 200 pixels::

            window = GWindow()
            window.draw_oval(0, 0, 300, 200)

        To draw a circle centered at (410, 410) with radius 160::

            window = GWindow()
            window.draw_oval(410 - 160, 410 - 160, 160 * 2, 160 * 2)

        :param x: The x-coordinate of the upper-left corner of the oval's bounding box.
        :param y: The y-coordinate of the upper-left corner of the oval's bounding box.
        :param width: The width of the oval in pixels.
        :param height: The height of the oval in pixels.
        """
        # TODO(sredmond): Find a way to supply a GRectangle's bounds instead.
        # TODO(sredmond): It's a little awkward to reverse the order of the arguments here.
        oval = _gobjects.GOval(width, height, x=x, y=y)
        # oval.color = self.color  # TODO(sredmond): Uncomment me! Just commented out for a brief moment of testing.
        self.draw(oval)

    def fill_oval(self, x, y, width, height):
        """Draw a filled oval.

        The oval's upper-left corner has coordinates given by (x, y), and size
        given by (width, height). The corner of an oval is the corner of the oval's
        bounding box.

        The color of the oval will be this GWindow's current marker color.

        To draw a filled oval with an upper-left corner at (0, 0), a width of 300
        pixels, and a height of 200 pixels::

            window = GWindow()
            window.fill_oval(0, 0, 300, 200)

        To draw a filled circle centered at (410, 410) with radius 160::

            window = GWindow()
            window.fill_oval(410 - 160, 410 - 160, 160 * 2, 160 * 2)

        :param x: The x-coordinate of the upper-left corner of the oval's bounding box.
        :param y: The y-coordinate of the upper-left corner of the oval's bounding box.
        :param width: The width of the oval in pixels.
        :param height: The height of the oval in pixels.
        """
        # TODO(sredmond): Find a way to supply a GRectangle's bounds instead.
        # TODO(sredmond): It's a little awkward to reverse the order of the arguments here.
        oval = _gobjects.GOval(width, height, x=x, y=y)
        oval.color = self.color
        # TODO(sredmond): Possibly, fall back to a black outline when the oval is filled.
        # oval.fill_color = self.color # TODO(sredmond): Uncomment me! Just commented out for a brief moment of testing.
        # oval.filled = True  # TODO(sredmond): Uncomment me! Just commented out for a brief moment of testing.
        self.draw(oval)

    def draw_rect(self, x, y, width, height):
        """Draw the outline of a rectangle.

        The rectangle's upper-left corner has coordinates given by (x, y) and size
        given by (width, height).

        The color of the rectangle's outline will be this GWindow's current color.

        To draw a rectangle with an upper-left corner at (0, 0), a width of 300 pixels,
        and a height of 200 pixels::

            window = GWindow()
            window.draw_rectangle(0, 0, 300, 200)

        :param x: The x-coordinate of the upper-left corner of the rectangle's bounding box.
        :param y: The y-coordinate of the upper-left corner of the rectangle's bounding box.
        :param width: The width of the rectangle in pixels.
        :param height: The height of the rectangle in pixels.
        """
        # TODO(sredmond): Find a way to supply a GRectangle's bounds instead.
        # TODO(sredmond): It's a little awkward to reverse the order of the arguments here.
        rect = _gobjects.GRect(width, height, x=x, y=y)
        rect.color = self.color
        self.draw(rect)

    def fill_rect(self, x, y, width, height):
        """Draw a filled rectangle.

        The rectangle's upper-left corner has coordinates given by (x, y) and size
        given by (width, height).

        The color of the rectangle's outline will be this GWindow's current color.

        To draw a rectangle with an upper-left corner at (0, 0), a width of 300 pixels,
        and a height of 200 pixels::

            window = GWindow()
            window.draw_rectangle(0, 0, 300, 200)

        :param x: The x-coordinate of the upper-left corner of the rectangle's bounding box.
        :param y: The y-coordinate of the upper-left corner of the rectangle's bounding box.
        :param width: The width of the rectangle in pixels.
        :param height: The height of the rectangle in pixels.
        """
        # TODO(sredmond): It's a little awkward to reverse the order of the arguments here.
        rect = _gobjects.GRect(width, height, x=x, y=y)
        rect.color = self.color
        rect.fill_color = self.color
        rect.filled = True
        self.draw(rect)

    def draw(self, gobj, x=None, y=None):
        """Draw a GObject on this GWindow's background layer.

        The background layer is for static drawings that cannot be modified once drawn.

        If both x and y are supplied, the object is moved to that location before drawing.

        :param gobj: The GObject to draw to this GWindow's background layer.
        :param x: The x-coordinate at which to draw the GObject.
        :param y: The y-coordinate at which to draw the GObject.
        """
        if x is not None and y is not None:
            gobj.location = x, y
        _platform.Platform().gwindow_draw(self, gobj)

    def clear(self):
        """Clear all content from this GWindow.

        Both the background and foreground layers are cleared with this function.
        """
        _platform.Platform().gwindow_clear(self)  # Remove from background layer.
        self._top.clear()  # Remove from foreground layer.

    def add(self, gobj, x=None, y=None):
        """Add a :class:`GObject` to the foreground layer of this :class:`GWindow`.

        If both x and y are supplied, the object is moved to that location before adding.

        To add a GOval to the window::

            window = GWindow()
            oval = GOval(0, 0, 100, 100)
            window.add(oval)

        :param gobj: The GObject to draw to this GWindow's foreground layer.
        :param x: The x-coordinate at which to draw the GObject.
        :param y: The y-coordinate at which to draw the GObject.
        """
        # TODO(sredmond): Handle the case where location is a float.
        if x is not None and y is not None:
            gobj.location = x, y
        self._top.add(gobj)

    def __iadd__(self, gobj):
        """Implement ``self += gobj``.

        Add a GObject to the foreground layer of this :class:`GWindow`.
        """
        self.add(gobj)

    def remove(self, gobj):
        """Remove a :class:`GObject` from this :class:`GWindow`.

        If the GObject was in the foreground layer of the window, return True.
        Otherwise, return False, but otherwise do not any failure.

        :param gobj: The GObject to remove from this GWindow.
        :returns: Whether the GObject was previously contained in this GWindow.
        """
        return self._top.remove(gobj)

    def __isub__(self, obj):
        """Implement ``self -= gobj``.

        Remove a GObject from the foreground layer of this :class:`GWindow`.
        """
        # Ignore the return value.
        self.remove(gobj)

    def add_to_region(self, gobj, region):
        """Add an interactor to the control strip in a given region.

        The interactor could also be a GLabel.

        The region argument must be some region from the :class:`Region` enum.

        To add a button to the SOUTH region::

            window = GWindow()
            button = GButton("Click me!")
            window.add_to_region(button, Region.SOUTH)

        :param gobj: The interactor to add to a region.
        :param region: The region to which the interactor will be added.
        :type region: Region
        """
        # TODO(sredmond): Either here, or at the platform level, convert into the region as a string.
        _platform.Platform().gwindow_add_to_region(self, gobj, region)

    def remove_from_region(self, gobj, region):
        """Remove an interactor from the control strip in a given region.

        The region argument must be some region from the :class:`Region` enum.

        :param gobj: The interactor to remove from a region.
        :param region: The region from which the interactor will be removed.
        :type region: Region
        """
        # TODO(sredmond): Either here, or at the platform level, convert into the region as a string.
        _platform.Platform().gwindow_remove_from_region(self, gobj, region)

    def set_region_alignment(self, region, align):
        """Set an alignment for a given region.

        Both the region and alignment arguments must be from the :class:`Region`
        and :class:`Alignment` enums respectively.

        To CENTER the content in the SOUTH region::

            window = GWindow()
            window.set_region_alignment(Region.SOUTH, Alignment.CENTER)

        :param region: The region in which to set alignment.
        :type region: Region
        :param align: The alignment to set in the region.
        :type align: Alignment
        """
        # TODO(sredmond): Either here, or at the platform level, convert into the region and alignment as a string.
        _platform.Platform().gwindow_set_region_alignment(self, region, align)

    def get_object_at(self, x, y):
        """Return the topmost GObject containing the point (x, y) or None.

        If no GObject contains the point (x, y), then return None.

        This only searches through the foreground layer.

        To search for a GObject at the point (41, 106)::

            window = GWindow()
            gobj = window.get_object_at(41, 106)
            if gobj is not None:
                print('We found an object!')
            else:
                print('No object found.')

        :param x: The x-coordinate of the point to examine.
        :param y: The y-coordinate of the point to examine.
        :returns: The topmost GObject containing the given point, or None if no such object was found.
        """
        # TODO(sredmond): This is currently implemented as an inefficient linear scan.
        # Consider optimizing the data structure of a GCompound to speed up these queries.
        # TODO(sredmond): If we ever reverse the iteration order of a GCompound
        # itself to go top->bottom, remove this reversed() wrapper.
        for gobj in reversed(self._top):
            if (x, y) in gobj:
                return gobj
        return None

    def _request_focus(self):
        """Ask the OS to assign keyboard focus to this GWindow.

        This brings it to the top and ensures that key events are delivered correctly.
        Clicking in the window automatically requests the focus.

        It is not guaranteed that the OS will give focus to this GWindow.
        """
        _platform.Platform().gwindow_request_focus(self)

    def _repaint(self):
        """Schedule a repaint on this window."""
        _platform.Platform().gwindow_repaint(self)


# NOTE(sredmond): This function exists in this module only so that students don't
# have to import anything special to get a pause function. It should eventually
# be deduplicated into the timer module, and loaded on package import.
def pause(milliseconds):
    """Pause for the given number of milliseconds.

    This is useful for animation where the graphical updates would otherwise be
    too fast to observe.

    To pause for half a second::

        pause(500)

    :param milliseconds: The number of milliseconds to pause.
    """
    _platform.Platform().gtimer_pause(milliseconds)


def screen_width():
    """Return the width of the entire display screen.

    :returns: The width of the display screen.
    """
    return _platform.Platform().gwindow_get_screen_width()


def screen_height():
    """Return the height of the entire display screen.

    :returns: The height of the display screen in pixels.
    """
    return _platform.Platform().gwindow_get_screen_height()


def exit_graphics():
    """Close all graphical windows and forcibly exit the application."""
    # TODO(sredmond): When would we ever want to do this?
    _platform.Platform().gwindow_exit_graphics()
