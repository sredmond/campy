"""Provide a hierarchy of graphical shapes based on the ACM Graphics model.

This module exports the superclass :class:`GObject`, as well as derived classes:

- :class:`GRect`
- :class:`GRoundRect`
- :class:`G3DRect`
- :class:`GOval`
- :class:`GArc`
- :class:`GLine`
- :class:`GImage`
- :class:`GLabel`
- :class:`GPolygon`

There is also a :class:`GCompound` class to facilitate nested object structures.

For more information on how to use each of these objects, see the comments on
each class.
"""
# TODO(sredmond): Handle lifecycles and deletion of these objects.
import campy.graphics.gcolor as _gcolor
import campy.graphics.gfont as _gfont
import campy.graphics.gmath as _gmath
import campy.graphics.gtypes as _gtypes
import campy.private.platform as _platform

from collections.abc import MutableSequence
import pathlib
import math


class GObject:
    """The common superclass of all graphical objects that can be displayed on a graphical window.

    For examples illustrating the use of the GObject class, see the descriptions
    of the individual subclasses.
    """
    def __init__(self):
        """Initialize a GObject with reasonable default values."""
        self._x = 0.0
        self._y = 0.0

        self._color = _gcolor.GColor.BLACK
        self._line_width = 1.0  # TODO(sredmond): Lots of GObjects currently ignore self._line_width
        self._visible = True

        self._transformed = False
        self._parent = None

    @property
    def x(self):
        """Get or set the x-coordinate of this :class:`GObject`."""
        return self._x

    @x.setter
    def x(self, x):
        self.location = x, self.y

    @property
    def y(self):
        """Get or set the y-coordinate of this :class:`GObject`."""
        return self._y

    @y.setter
    def y(self, y):
        self.location = self.x, y

    @property
    def location(self):
        """Get or set the location of this object as a :class:`GPoint`.

        You can supply either a GPoint or a 2-element tuple to this property.
        Accessing this property will return a GPoint which can be unpacked as a
        tuple.
        """
        return _gtypes.GPoint(self.x, self.y)

    @location.setter
    def location(self, point):
        x, y = point
        self._x = x
        self._y = y
        _platform.Platform().gobject_set_location(self, x, y)

    def move(self, dx, dy):
        """Move this object on the screen using the supplied displacements.

        :param dx: The displacement in the x-direction.
        :param dy: The displacement in the y-direction.
        """
        self.location = (self.x + dx, self.y + dy)

    @property
    def bounds(self):
        """Get the bounding box for this object.

        The bounding box of an object is the smallest rectangle that covers
        everything drawn by the figure. The coordinates of this rectangle will
        usually, but not always, match the object's location. For example, the
        location of a :class:`GLabel` gives the coordinates of the point on the
        baseline where the string begins. However, the bounds of the GLabel
        represent a rectangle that entirely covers the window area occupied by
        the GLabel.

        Subclasses must override this property (and optionally declare a setter)
        to indicate their bounding box.

        :returns: The bounding box of this GObject.
        :rtype: :class:`GRectangle`
        """
        # TODO(sredmond): Make this an abstract method?
        return _gtypes.GRectangle(-1, -1, 0, 0)

    @property
    def width(self):
        """Get the width of this :class:`GObject`.

        The width of an object is the same as the width of its bounding box.

        :returns: The width (in pixels) of this GObject.
        """
        return self.bounds.width

    @property
    def height(self):
        """Get the height of this :class:`GObject`.

        The height of an object is the same as the height of its bounding box.

        :returns: The height (in pixels) of this GObject.
        """
        return self.bounds.height

    @property
    def size(self):
        """Get the size of this :class:`GObject` as a :class:`GDimension`.

        :returns: The size of this GObject in pixels.
        :rtype: :class:`GDimension`
        """
        return _gtypes.GDimension(self.bounds.width, self.bounds.height)

    @property
    def color(self):
        """Get or set the color used to draw this object.

        The supplied color can be any object acceptable to :class:`GColor`, so
        check that class's documentation for complete details on arguments.

        Usually, the supplied color will be one of the predefined colors:

            - BLACK
            - BLUE
            - CYAN
            - DARK_GRAY
            - GRAY
            - GREEN
            - LIGHT_GRAY
            - MAGENTA
            - ORANGE
            - PINK
            - RED
            - WHITE
            - YELLOW

        TODO(sredmond): Add more detail to the possible colors with examples.

        Accessing this property will return a :class:`GColor` which can be
        used anywhere that expects a color.
        """
        # TODO(sredmond): It looks like setting the color for a gobject won't change the outside.
        return self._color

    @color.setter
    def color(self, color):
        self._color = _gcolor.GColor.normalize(color)
        _platform.Platform().gobject_set_color(self, self.color)

    @property
    def line_width(self):
        """Get or set the line width used to draw this :class:`GObject`."""
        # TODO(sredmond): Add more documentation here.
        # TODO(sredmond): Does line width need to be an integer?
        return self._line_width

    @line_width.setter
    def line_width(self, width):
        self._line_width = width
        _platform.Platform().gobject_set_line_width(self, width)

    @property
    def visible(self):
        """Get or set whether this :class:`GObject` is visible.

        A :class:`GObject` that is visible will still exist on a GWindow once added.

        Usage::

            window = GWindow()
            oval = GOval(0, 0, 41, 41)
            window.add(oval)
            print(oval.visible)  # => True
            oval.visible = False  # Hides the oval on the window.
            print(oval.visible)  # => False
        """
        return self._visible

    @visible.setter
    def visible(self, flag):
        self._visible = flag
        _platform.Platform().gwindow_set_visible(flag, gobj=self)

    def scale(self, *scales):
        """Scale this object by the given scale factor(s).

        Most clients use the one-argument form, which scales an object in both
        dimensions. To double the size of a GOval::

            oval = GOval(0, 0, 41, 41)
            oval.scale(2)
            print(oval.width, oval.height)  # => 82, 82

        There is also a two-argument form which applies separate scale factors
        to the x- and y-dimensions::

            oval = GOval(0, 0, 41, 41)
            oval.scale(3, 5)
            print(oval.width, oval.height)  # => 123, 205

        It is an error to call this function with no arguments, or with three or
        more arguments.

        :param scales: The scale factors by which to scale this object.
        """
        # TODO(sredmond): Does this scale about the center or about the origin?
        if not scales or len(scales) > 2:
            return  # TODO(sredmond): Actually fail if the number of scale factors isn't 1 or 2.

        if len(scales) == 1:
            sx, sy = scales[0], scales[0]
        else:
            sx, sy = scales

        # Mark this object as transformed so we know to defer to the platform's methods.
        self._transformed = True
        _platform.Platform().gobject_scale(self, sx, sy)

    def rotate(self, theta):
        """Rotate this object some degrees counterclockwise about its origin.

        :param: The angle (in degrees) about which to rotate this object about its origin.
        """
        # Mark this object as transformed so we know to defer to the platform's methods.
        self._transformed = True
        _platform.Platform().gobject_rotate(self, theta)

    def send_forward(self):
        """Moves this object one step toward the front in the z dimension.

        If it was already at the front of the stack, nothing happens.
        """
        if self.parent:
            self.parent.send_forward(self)

    def send_to_front(self):
        """Move this object to the front of the display in the z dimension.

        By moving it to the front, this object will appear to be on top of the
        other graphical objects on the display and may hide any objects that
        are further back.
        """
        if self.parent:
            self.parent.send_forward(self)

    def send_backward(self):
        """Moves this object one step toward the back in the z dimension.

        If it was already at the back of the stack, nothing happens.
        """
        if self.parent:
            self.parent.send_backward(self)

    def send_to_back(self):
        """Move this object to the back of the display in the z dimension.

        By moving it to the back, this object will appear to be behind the other
        graphical objects on the display and may be obscured by other objects
        that are further forward.
        """
        if self.parent:
            self.parent.send_to_back(self)

    def __contains__(self, point):
        """Implement ``point in self``.

        Check whether a given :class:`GPoint` or 2-element tuple is contained
        within the bounding box of this :class:`GObject`.

        Subclasses can override this method to provide shape-specific containment
        checks. For example, the :class:`GOval` class provides a custom method to
        check for containment.
        """
        # TODO(sredmond): It sort of feels like all of the subclasses (except GImage and GLabel)
        # just define their own contains anyway. Is it still good design to keep this implementation here?
        # Attempt to unpack the supplied point as a tuple.
        x, y = point

        # TODO(sredmond): Should we really just offload the work if it happens to be transformed?
        if self._transformed:
            return _platform.Platform().gobject_contains(self, x, y)

        return (x, y) in self.bounds

    @property
    def parent(self):
        """Return the GCompound that contains this object, if it exists.

        Each :class:`GWindow` has a single :class:`GCompound` that is aligned
        with the window. Adding objects to the window adds them to the window's
        top :class:`GCompound`. So, a :class:`GObject` does not have a parent
        until it is added to a :class:`GCompound`, either directly or by way of
        adding the :class:`GObject` to a :class:`GWindow`::

            window = GWindow()
            oval = GOval(0, 0, 41, 41)
            print(oval.parent is None)  # => True
            window.add(oval)
            print(oval.parent is None)  # => False

        :returns: This object's parent :class:`GCompound`, if it exists.
        :rtype: :class:`GCompound`
        """
        return self._parent

# SECTION: Graphical Mixins
class GFillableObject(GObject):
    """Representation of a :class:`GObject` that can be filled.

    Subclasses of :class:`GFillableObject` have a boolean property ``filled``
    and a :class:`GColor`-valued property ``fill_color``.
    """
    def __init__(self, filled=False, fill_color=None):
        super().__init__()
        self._filled = False
        self._fill_color = self.color  # Default to the outline color.

    @property
    def filled(self):
        """Get or set whether this object is filled.

        A value of True corresponds to filled and a value of False corresponds to outlined.
        """
        return self._filled

    @filled.setter
    def filled(self, is_filled):
        self._filled = is_filled
        _platform.Platform().gobject_set_filled(self, is_filled)

    @property
    def fill_color(self):
        """Return the color used to fill this object.

        If none has been set, return the empty string."""
        return self._fill_color

    @fill_color.setter
    def fill_color(self, color):
        color = _gcolor.GColor.normalize(color)
        self._fill_color = color
        _platform.Platform().gobject_set_fill_color(self, self.fill_color)

# END SECTION: Graphical Mixins

class GRect(GFillableObject):
    """Graphical representation of a rectangular box.

    To add a filled red rectangle with width 200 and height 100 to a :class:`GWindow`::

        window = GWindow()
        rect = GRect(200, 100)
        rect.filled = True
        rect.color = "RED"
        window.add(rect, 0, 0)
    """
    def __init__(self, width, height, *, x=0, y=0):
        """Create a rectangle of a width and height with an optional location.

        The two required arguments represent the width and the height of the
        :class:`GRect`, in pixels. Keyword arguments can be supplied to set the
        initial location of the :class:`GRect`.

        A :class:`GRect` defaults to being unfilled and outlined in black. The
        default location for a new :class:`GRect` is at (0, 0).

        To create a :class:`GRect` with width 200 and height 100::

            rect = GRect(200, 100)

        To create a 300x400 :class:`GRect` at position (50, 80)

            rect = GRect(200, 100, x=50, y=80)

        :param width: The width of the rectangle in pixels.
        :param height: The height of the rectangle in pixels.
        :param x: The x-coordinate of the top-left corner of this rectangle.
        :param y: The y-coordinate of the top-left corner of this rectangle.
        """
        super().__init__()
        self._width = width
        self._height = height
        self.location = x, y

    # @property
    # def size(self):
    #     return self.width, self.height

    # TODO(sredmond): Figure out how to set width as a property from an inherited getter.

    # @property
    # def setSize(self, size=None, width=None, height=None):
    #     '''
    #     Changes the size of this rectangle to the specified width and height.

    #     @type size: GDimention
    #     @type width: float
    #     @type height: float
    #     @param size: GDimension, will override height and width
    #     @rtype: void
    #     '''
    #     if(size != None):
    #         width = size.getWidth()
    #         height = size.getHeight()

    #     if(width == None or height == None): return

    #     if(self._transformed):
    #         raise Exception("setSize: Object has been transformed")

    #     self.width = width
    #     self.height = height
    #     _platform.Platform().gobject_set_size(self, width, height)

    # def setBounds(self, bounds=None, x=None, y=None, width=None, height=None):
    #     '''
    #     Changes the bounds of this rectangle to the specified values.

    #     @type bounds: GRectangle
    #     @type x: float
    #     @type y: float
    #     @type width: float
    #     @type height: float
    #     @param bounds: bounding rectangle, will override other parameters
    #     @rtype: void
    #     '''
    #     if(bounds != None):
    #         x = bounds.getX()
    #         y = bounds.getY()
    #         width = bounds.getWidth()
    #         height = bounds.getHeight()

    #     if(x == None or y == None or width == None or height == None): return

    #     self.setLocation(x=x, y=y)
    #     self.setSize(width=width, height=height)

    @property
    def bounds(self):
        """Get the bounding box for this :class:`GRect`.

        The bounding box of a :class:`GRect` is simply the rectangle's bounds
        itself.

        :returns: A bounding box that covers this :class:`GRect`.
        :rtype: :class:`GRectangle`
        """
        # TODO(sredmond): What do we we do about transformed rectangles?
        if(self._transformed): return _platform.Platform().gobject_get_bounds(self)
        return _gtypes.GRectangle(self.x, self.y, self._width, self._height)

    def __str__(self):
        return "GRect({self.width}, {self.height}, x={self.x}, y={self.y})".format(self=self)


class GRoundRect(GRect):
    """Graphical representation of a rectangular box with rounded corners.

    The rounded corners are quarter-circle arcs of a fixed diameter.
    """
    # TODO(sredmond): Add documentation from the GRect object here

    # The number of pixels in the diameter of the arc forming the corner.
    CORNER_ROUNDING = 10

    def __init__(self, width, height, *, x=None, y=None, corner=CORNER_ROUNDING):
        """Create a new rounded rectangle with the supplied width and height.

        The caller can also specify x and y coordinates for the top-left corner
        of this :class:`GRoundRect`'s bounding box.

        The corner parameter gives the diameter of the arc forming the corner,
        with a reasonable default. The higher this number is, the more rounded
        the resulting rectangle will be.

        :param width: The width of the rounded rectangle in pixels.
        :param height: The height of the rounded rectangle in pixels.
        :param x: The x-coordinate of the top-left corner of this rounded rectangle.
        :param y: The y-coordinate of the top-left corner of this rounded rectangle.
        :param corner: The diameter in pixels of the rounded arcs.
        """
        super().__init__(width, height, x=x, y=y)

        self.corner = corner
        _platform.Platform().groundrect_constructor(self, width, height, corner)

    def __str__(self):
        # TODO(sredmond): It's a little awkward that the constructor argument order is different.
        return "GRoundRect(x={self.x}, y={self.y}, width={self.width}, height={self.height}, corner={self.corner})".format(self=self)


class G3DRect(GRect):
    """Graphical representation of a rectangular box that can be raised or lowered.

    The 3D effect of this rectangle is purely aesthetic and does not affect the
    rectangle's z-positioning on the parent :class:`GCompound`.
    """
    # TODO(sredmond): Add more documentation from the GRect object here
    def __init__(self, width, height, *, x=None, y=None, raised=False):
        """Create a new 3D rectangle with the supplied width and height.

        The caller can also specify x and y coordinates for the top-left corner
        of this :class:`G3DRect`'s bounding box.

        If this rectangle is raised (defaulting to False), then the rectangle is
        drawn with highlights that suggest that it is raised about the background.

        :param width: The width of the 3D rectangle in pixels.
        :param height: The height of the 3D rectangle in pixels.
        :param x: The x-coordinate of the top-left corner of this 3D rectangle.
        :param y: The y-coordinate of the top-left corner of this 3D rectangle.
        :param raised: Whether to draw the 3D rectangle as raised (or lowered)
        """
        super().__init__(width, height, x=x, y=y)
        self._raised = raised
        _platform.Platform().g3drect_constructor(self, width, height, raised)

    @property
    def raised(self):
        """Get or set whether this object appears raised.

        True represents a rectangle with highlights to appear raised above the background.
        False represents a rectangle with highlights to appear lowered above the background.
        """
        return self._raised

    @raised.setter
    def raised(self, is_raised):
        self._raised = is_raised
        _platform.Platform().g3drect_set_raised(self, is_raised)

    def __str__(self):
        # TODO(sredmond): It's a little awkward that the constructor argument order is different.
        return "G3DRect(x={self.x}, y={self.y}, width={self.width}, height={self.height}, raised={self.raised})".format(self=self)


class GOval(GFillableObject):
    """Graphical representation of an oval inscribed in a rectangular box.

    To display a filled green oval::

        window = GWindow()
        oval = gobjects.GOval(window.width, window.height)
        oval.filled = True
        oval.color = "GREEN"
        window.add(oval)
    """

    def __init__(self, width, height, *, x=0, y=0):
        """Initialize a new oval inscribed in a rectangular box.

        By default, the corner of the rectangular box is at (0, 0). By
        specifying x- and y- coordinates as keyword arguments, the caller can
        locate the oval at a given position.


        :param width: The width of the bounding rectangle in pixels.
        :param height: The height of the bounding rectangle in pixels.
        :param x: The x-coordinate of the top-left corner of the bounding rectangle.
        :param y: The y-coordinate of the top-left corner of the bounding rectangle.
        """
        super().__init__()
        self._width = width
        self._height = height
        # _platform.Platform().goval_constructor(self, width, height)
        # TODO(sredmond): At the moment, this needs to be after the constructor line. This is a sign of a bad organization and should be changed.
        self.location = x, y

    # def setSize(self, width=None, height=None, size=None):
    #     '''
    #     Changes the size of the bounding rectangle to the specified width
    #     and height.

    #     @type width: float
    #     @type height: float
    #     @type size: GDimension
    #     @param size: will override height and width parameters
    #     @rtype: void
    #     '''
    #     if(self._transformed): raise Exception("setSize: Object has been transformed")
    #     if(size != None):
    #         width = size.width
    #         height = size.height

    #     self.width = width
    #     self.height = height
    #     _platform.Platform().gobject_set_size(self, width, height)

    # def setBounds(self, x=None, y=None, width=None, height=None, bounds=None):
    #     '''
    #     Changes the bounds of the oval to the specified values.

    #     @type x: float
    #     @type y: float
    #     @type width: float
    #     @type height: float
    #     @type bounds: GRectangle
    #     @param bounds: will override all other parameters
    #     @rtype: void
    #     '''
    #     if(bounds != None):
    #         x, y, width, height = bounds

    #     self.setLocation(x=x, y=y)
    #     self.setSize(width, height)

    @property
    def bounds(self):
        """Get the bounding box for this :class:`GOval`.

        The bounding box of a :class:`GOval` is simply the bounding rectangle.

        :returns: A bounding box that covers this :class:`GOval`.
        :rtype: :class:`GRectangle`
        """
        # TODO(sredmond): What do we we do about transformed rectangles?
        if(self._transformed): return _platform.Platform().gobject_get_bounds(self)
        return _gtypes.GRectangle(self.x, self.y, self._width, self._height)


    def __contains__(self, point):
        """Implement ``point in self``.

        Check whether a given :class:`GPoint` or 2-element tuple is contained
        within this oval. A point is contained within the oval if it lies
        completely inside the oval or is on the boundary.

        :param point: The :class:`GPoint` or 2-element tuple to check.
        :returns: Whether the point is within this oval.
        """
        # Attempt to unpack the supplied point as a tuple.
        x, y = point

        # TODO(sredmond): How should I handle transformed GObjects?
        if self._transformed:
            return _platform.Platform().gobject_contains(self, x, y)

        rx = self.width / 2
        ry = self.height / 2
        if rx == 0 or ry == 0:  # No points in a line.
            return False

        # `point` is at (dx, dy) relative to ellipse center.
        dx = x - (self.x + rx)
        dy = y - (self.y + ry)
        return (dx * dx) / (rx * rx) + (dy * dy) / (ry * ry) <= 1.0

    def __str__(self):
        return "GOval({self.width}, {self.height}, x={self.x}, y={self.y})".format(self=self)


class GArc(GFillableObject):
    """Graphical representation of an elliptical arc.

    An elliptical arc is uniquely determined by the following three parameters:

    - The coordinates of the ellipse's bounding rectangle (width, height) and (x, y)
    - The angle at which the arc starts (start)
    - The number of degrees that the arc covers (sweep)

    All angles in the :class:`GArc` class are measured in degrees counterclockwise
    from the positive x-axis. Negative angles refer to degrees clockwise.

    To create an semicircle arc starting 45 degrees counterclockwise of the
    positive x-axis with diameter 50::

        window = GWindow()
        arc = GArc(50, 50, 45, 180, x=0, y=0)
        window.add(arc)

    If a :class:`GArc` is unfilled, the figure consists only of the arc itself.

    If a :class:`GArc` is filled, the figure consists of the
    pie-shaped wedge formed by connecting the endpoints of the arc to
    the center.

    For example, the following program draws a 270-degree arc starting at 45
    degrees filled in yellow, similar to the PacMan video game::

        window = GWindow()
        center = GPoint(window.width / 2, window.height / 2)
        radius = 25
        pacman = GArc(2 * radius, 2 * radius, 45, 270
            x=center.x - radius, y=center.y - radius)
        pacman.filled = True
        pacman.fill_color = "YELLOW"
        window.add(pacman)
    """
    def __init__(self, width, height, start, sweep, x=0, y=0):
        """Initialize a new :class:`GArc` consisting of an elliptical arc.


        By default, the corner of the rectangular box is at (0, 0). By
        specifying x- and y- coordinates as keyword arguments, the caller can
        locate the arc's bounding rectangle at a given position.

        :param width: The width of the bounding rectangle in pixels.
        :param height: The height of the bounding rectangle in pixels.
        :param start: The angle at which the arc starts (in degrees) from the positive x-axis.
        :param sweep: The angle that the arc sweeps out (in degrees).
        :param x: The x-coordinate of the top-left corner of the bounding rectangle.
        :param y: The y-coordinate of the top-left corner of the bounding rectangle.
        """
        super().__init__()
        self.location = x, y

        # What are these?
        self.frameWidth = width
        self.frameHeight = height

        self._start = start
        self._sweep = sweep
        # _platform.Platform().garc_constructor(self, width, height, start, sweep)

    @property
    def start(self):
        """Get or set the starting angle (in degrees) of this :class:`GArc`.

        The starting angle is measured in degrees counterclockwise from the
        positive x-axis.
        """
        return self._start

    @start.setter
    def start(self, start_angle):
        self._start = start_angle
        _platform.Platform().garc_set_start_angle(self, start)

    @property
    def sweep(self):
        """Get or set the sweep angle (in degrees) of this :class:`GArc`.

        The sweep angle is measured in degrees and represents the number of
        degrees carved out by this :class:`GArc`. For example, a semi-elliptical
        arc has a sweep of 180 degrees.
        """
        # TODO(sredmond): Enforce that sweep is between 0 and 360. or perhaps -360 and 360
        return self._sweep

    @sweep.setter
    def sweep(self, sweep_angle):
        self._sweep = sweep_angle
        _platform.Platform().garc_set_sweep_angle(self, sweep_angle)

    @property
    def start_point(self):
        """Get the :class:`GPoint` at which the arc starts."""
        rx, ry = self.width / 2, self.height / 2
        cx, cy = self.x + rx, self.y + ry
        return _gtypes.GPoint(cx + rx * _gmath.cos_degrees(self.start), cy - ry * math.sin_degrees(self.start))

    @property
    def end_point(self):
        """Get the :class:`GPoint` at which the arc ends."""
        rx, ry = self.width / 2, self.height / 2
        cx, cy = self.x + rx, self.y + ry
        return _gtypes.GPoint(cx + rx * _gmath.cos_degrees(self.start + self.sweep), cy - ry * math.sin_degrees(self.start + self.sweep))

    # TODO(sredmond): Expose a setter for the start point or end point?

    # def setFrameRectangle(self, x=None, y=None, width=None, height=None, rect=None):
    #     '''
    #     Changes the boundaries of the rectangle used to frame the arc.

    #     @type x: float
    #     @type y: float
    #     @type width: float
    #     @type height: float
    #     @type rect: GRectangle
    #     @param rect: bounding frame, will override other parameters
    #     @rtype: void
    #     '''
    #     if(rect != None):
    #         x = rect.getX()
    #         y = rect.getY()
    #         width = rect.getWidth()
    #         height = rect.getHeight()

    #     self.location = x, y
    #     self.frameWidth = width
    #     self.frameHeight = height
    #     _platform.Platform().garc_set_frame_rectangle(self, x, y, width, height)

    # def getFrameRectangle(self):
    #     '''
    #     Returns the boundaries of the rectangle used to frame the arc.

    #     @rtype: GRectangle
    #     '''
    #     return _gtypes.GRectangle(0,0,0,0) #!!

    @property
    def bounds(self):
        """Get the bounding rectangle for this arc.

        @rtype: GRectangle
        """
        # TODO(sredmond): Should this be small if the arc is small?
        # TODO(sredmond): Write this method.
        if(self._transformed): return _platform.Platform().gobject_get_bounds(self)

        rx = self.frameWidth / 2
        ry = self.frameHeight / 2
        cx = self.x + rx
        cy = self.y + ry

        startRadians = self.start * _gmath.PI / 180
        sweepRadians = self.sweep * _gmath.PI / 180

        p1x = cx + math.cos(startRadians) * rx
        p1y = cy - math.sin(startRadians) * ry
        p2x = cx + math.cos(startRadians + sweepRadians) * rx
        p2y = cy - math.sin(startRadians + sweepRadians) * ry

        xMin = min(p1x, p2x)
        xMax = max(p1x, p2x)
        yMin = min(p1y, p2y)
        yMax = max(p1y, p2y)

        if self.containsAngle(0): xMax = cx + rx
        if self.containsAngle(90): yMin = cy - ry
        if self.containsAngle(180): xMin = cx - rx
        if self.containsAngle(270): yMax = cy + ry

        if self.filled:
            xMin = min(xMin, cx)
            yMin = min(yMin, cy)
            xMax = max(xMax, cx)
            yMax = max(yMax, cy)
        return _gtypes.GRectangle(xMin, yMin, xMax - xMin, yMax - yMin)

    def __contains__(self, point, tolerance=2.5):
        """Implement ``point in self``.

        A :class:`GArc` contains a point if and only if the point is contained
        inside of the pie wedge defined by the bounds of the arc.

        # For advanced users, this method is overloaded with an optional tolerance
        # parameter. Since *almost* no one will ever want to directly call
        # ``self.__contains__(point)``, the tolerance defaults to a reasonable value.
        # However, to check for containment with a custom tolerance, call::

        #     line = GLine(0, 0, 5, 5)
        #     print(line.__contains__((2, 2), tolerance=0.5))  # => False

        # :param point: The :class:`GPoint` or 2-element tuple to check.
        # :param tolerance: The maximum distance (in pixels) to still count as containment.
        # :returns: Whether the point is within a tolerance of any point on this line.
        """

        '''
        Returns whether or not this object contains the point x, y

        @type x: float
        @type y: float
        @rtype: boolean
        '''
        # TODO(sredmond): Write this method correctly.
        if(self._transformed): return _platform.Platform().gobject_contains(self, x, y)

        rx = frameWidth / 2
        ry = frameHeight / 2
        if rx == 0 or ry == 0: return False
        dx = x - (self.x + rx)
        dy = y - (self.y + ry)
        r = (dx * dx) / (rx * rx) + (dy * dy) / (ry * ry)
        if(self.fillFlag):
            if (r > 1.0): return False
        else:
            t = tolerance / ((rx + ry) / 2) #!!
            if (abs(1.0 - r) > t): return False
        return self.containsAngle(math.atan2(-dy, dx) * 180 / _gmath.PI)

    def containsAngle(self, theta):
        '''
        Internal method
        '''
        start = min(self.start, self.start + self.sweep)
        sweep = abs(self.sweep)
        if(sweep >= 360): return True
        if(theta < 0): theta = 360 - math.fmod(-theta, 360)
        else: theta = math.fmod(theta, 360)
        if(start < 0): start = 360 - math.fmod(-start, 360)
        else: start = math.fmod(start, 360)
        if(start + sweep > 360):
            return (theta >= start or theta <= start + sweep - 360)
        else:
            return (theta >= start and theta <= start + sweep)

    def __str__(self):
        return "GArc({self.frame_width}, {self.frame_height}, {self.start}, {self.sweep}, x={self.x}, y={self.y}".format(self=self)


class GLine(GObject):
    """Graphical representation of a line segment defined by two endpoints.

    To create a line from ``(14, 41)`` to ``(601, 106)``::

        line = GLine(14, 41, 601, 106)

    To draw two diagonal lines crossing a :class:`GWindow`::

        window = GWindow()
        window.add(GLine(0, 0, window.width, window.height))
        window.add(GLine(0, window.height, window.width, 0))

    Note that creating a :class:`GLine` will not automatically add it to any
    displays. Rather, you must explicitly call the `.add` method on an
    appropriate :class:`GWindow`.
    """
    def __init__(self, x0, y0, x1, y1):
        """Create a line segment from its endpoints.

        The first two parameters ``(x0, y0)`` define the start of the line, and
        the next two parameters ``(x1, y1)`` define the end of the line.

        To create a line from ``(0, 0)`` to ``(41, 106)``::

            line = GLine(0, 0, 41, 106)

        :param x0: The x-coordinate of the starting point.
        :param y0: The y-coordinate of the starting point.
        :param x1: The x-coordinate of the ending point.
        :param y1: The y-coordinate of the ending point.
        """
        # TODO(sredmond): Consider allowing the user to supply two GPoints (with splats?)
        super().__init__()
        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1

        # TODO(sredmond): Don't bother sending along the values when we also send the built object.
        # _platform.Platform().gline_constructor(self)

    @property
    def start(self):
        """Get or set this :class:`GLine`'s starting point.

        Changing the start point modifies the line segment even if it has
        already been added to a :class:`GWindow`.

        Usage::

            window = GWindow()
            line = GLine(0, 0, 41, 41)
            window.add(line)
            print(line.start)  # => GPoint(0, 0)
            line.start = 4, 1
            print(line.start)  # => GPoint(4, 1)

        You can supply either a GPoint or a 2-element tuple to this property.
        Accessing this property will return a GPoint which can be unpacked as a
        tuple::

            window = GWindow()
            line = GLine(0, 0, 41, 41)
            window.add(line)
            line.start = GPoint(16, 25)  # Supply a GPoint to the setter.
            startx, starty = line.start  # Unpack the start point immediately.

        Setting the start point does not modify the end point. Thus, this is
        different from setting this :class:`GLine`'s location, which translates
        the entire line segment.
        """
        return _gtypes.GPoint(self._x0, self._y0)

    @start.setter
    def start(self, start_point):
        # Attempt to unpack the supplied start point as a tuple. This supports
        # both GPoints and 2-element tuples.
        start_x, start_y = start_point
        self._x0 = start_x
        self._y0 = start_y
        _platform.Platform().gline_set_start_point(self, self._x0, self._y0)

    @property
    def end(self):
        """Get or set this :class:`GLine`'s ending point.

        Changing the end point modifies the line segment even if it has
        already been added to a :class:`GWindow`.

        Usage::

            window = GWindow()
            line = GLine(0, 0, 41, 41)
            window.add(line)
            print(line.end)  # => GPoint(41, 41)
            line.end = 4, 1
            print(line.end)  # => GPoint(4, 1)

        You can supply either a GPoint or a 2-element tuple to this property.
        Accessing this property will return a GPoint which can be unpacked as a
        tuple::

            window = GWindow()
            line = GLine(0, 0, 41, 41)
            window.add(line)
            line.end = GPoint(106, 106)  # Supply a GPoint to the setter.
            endx, endy = line.start  # Unpack the end point immediately.

        Setting the end point does not modify the start point. Thus, this is
        different from setting this :class:`GLine`'s location, which translates
        the entire line segment.
        """
        return _gtypes.GPoint(self._x1, self._y1)

    @end.setter
    def end(self, end_point):
        # Attempt to unpack the supplied start point as a tuple. This supports
        # both GPoints and 2-element tuples.
        end_x, end_y = end_point
        self._x1 = end_x
        self._y1 = end_y
        _platform.Platform().gline_set_end_point(self, self._x1, self._y1)

    # TODO(sredmond): Add methods to get/set dx/dy?
    # TODO(sredmond): Add methods to get/set just x0/y0/x1/y1?

    # TODO(sredmond): Implement bounds.
    # @property
    # def bounds

    def __contains__(self, point, tolerance=1.5):
        """Implement ``point in self``.

        Check whether a given :class:`GPoint` or 2-element tuple is contained
        within this line.

        Since a line segment technically has zero area, this method actual checks
        whether the supplied point is within some small, default tolerance (inclusive)
        of any point on the line segment, measured by perpendicular distance.
        For example, the point ``(2, 2)`` is within the default tolerance of
        the line from ``(0, 0)`` to ``(5, 5)``::

            line = GLine(0, 0, 5, 5)
            print((2, 2) in line)  # => True
            print((0, 5) in line)  # => False

        For advanced users, this method is overloaded with an optional tolerance
        parameter. Since *almost* no one will ever want to directly call
        ``self.__contains__(point)``, the tolerance defaults to a reasonable value.
        However, to check for containment with a custom tolerance, call::

            line = GLine(0, 0, 5, 5)
            print(line.__contains__((2, 2), tolerance=0.5))  # => False

        :param point: The :class:`GPoint` or 2-element tuple to check.
        :param tolerance: The maximum distance (in pixels) to still count as containment.
        :returns: Whether the point is within a tolerance of any point on this line.
        """
        # TODO(sredmond): This method will need to change if the GLine is transformed.

        # The distance between a point (x, y) and a line (infinite, not a segment)
        # between two points (x0, y0) and (x1, y1) is given by:
        #
        #    |(y1 - y0) * x - (x1 - x0) * y + x1 * y0 - y1 * x0|
        #    ---------------------------------------------------
        #           distance between (x0, y0) and (x1, y1)
        # Attempt to unpack the supplied point as a tuple.
        x, y = point

        # If our line segment is really a point, just check the circle.
        if self._x0 == self._x1 and self._y0 == self._y1:
            return math.hypot(self._x0 - x, self._y0 - y) <= tolerance

        # If the distance to either of the endpoints is small enough, we're good.
        if math.hypot(self._x0 - x, self._y0 - y) <= tolerance or math.hypot(self._x1 - x, self._y1 - y) <= tolerance:
            return True

        # Compute coefficients a, b, c for the expression of this line as ax + by + c = 0
        a = self._y1 - self._y0
        b = self._x0 - self._x1
        c = self._x1 * self._y0 - self._y1 * self._x0
        dist = math.hypot(a, b)

        proj_x = (b * (b * x - a * y) - a * c) / (dist * dist)
        proj_y = (a * (-b * x + a * y) - b * c) / (dist * dist)

        # Otherwise, we're only close enough if (1) the point we project to (on
        # the full line) is between the two endpoints AND (2) we are close enough
        # to that point.
        return (min(self._x0, self._x1) <= proj_x <= max(self._x0, self._x1)
            and min(self._y0, self._y1) <= proj_y <= max(self._y0, self._y1)
            and abs(a * x + b * y + c) / dist <= tolerance)

    def __str__(self):
        return "GLine({self.x0}, {self.y0}, {self.x1}, {self.y1}".format(self=self)


# TODO(sredmond):Un-hotfix me
# from campy.graphics.gimage import GImage  # Make the "new" GImage accessible from this namespace.

# class GImage(GObject):
#     """Graphical representation of an image from a file.

#     To display a centered :class:`GImage` of the Stanford tree::

#         window = GWindow()
#         tree = GImage("StanfordTree.gif")
#         x = (window.width - tree.width) / 2
#         y = (window.height - tree.height) / 2
#         window.add(tree, x, y)

#     The above code assumes that you have a file named ``StanfordTree.gif`` in
#     the current directory.

#     The search for matching image files begins in the current directory and,
#     failing that, searches an ``images/`` subdirectory relative to the calling script.
#     """
#     # TODO(sredmond): Have a environmental variable for a custom subdirectory.
#     # TODO(sredmond): When would you use a GImage over a GBufferedImage?

#     def __init__(self, filename, x=0, y=0):
#         """Initialize a new image from the given file.

#         The image file should either exist in the current directory or in a
#         subdirectory named ``images/``.

#         By default, the upper left corner of the image appears at the origin.
#         By supplying x- and y- coordinates, the caller can set the location
#         to the point (x, y).

#         :param filename: the name of the image file to load.
#         :param x: (optional) the x-coordinate to which to move this :class:`GImage`.
#         :param y: (optional) the y-coordinate to which to move this :class:`GImage`.
#         """
#         super().__init__()
#         self._path = _platform.Platform().image_find(filename)
#         self._image = _platform.Platform().gimage_constructor(self)
#         self.location = x, y
#         self._size = _platform.Platform().gimage_constructor(self, filename)

#     @property
#     def filename(self):
#         """Get this :class:`GImage`'s filename."""
#         return self._path.name

#     @property
#     def bounds(self):
#         """Get the bounding box for this :class:`GImage`."""
#         if self._transformed: return _platform.Platform().gobject_get_bounds(self)
#         return _gtypes.GRectangle(self.x, self.y, self._size.width, self._size.height)

#     def __str__(self):
#         return 'GImage({!r})'.format(self.filename)


class GLabel(GObject):
    """Graphical representation of a text string.

    For example, to add a :class:`GLabel` with the message "Hello, world!" to
    the center of a :class:`GWindow`::

        window = GWindow()
        label = GLabel("Hello, world!")
        label.font = "SansSerif-18"
        x = (window.width - label.width) / 2
        y = (window.height + label.ascent) / 2
        window.add(label, x, y)

    In order to control the appearance and positioning of a :class:`GLabel`,
    it's important to understand the following terms:

        - The baseline is the horizontal line on which the characters rest.
        - The origin is the point on the baseline at which the label begins.
        - The height is the distance (in pixels) that would separate two
          successive lines such that characters would not overlap.
        - The ascent is the maximum distance that any character in this font
          extends above the baseline.
        - The descent is the maximum distance that any character in this font
          extends below the baseline.
    """
    # TODO(sredmond): Are ascent and descent distances for the given text, or for the font itself?
    # TODO(sredmond): What exactly do we mean in the description of height above?

    def __init__(self, label, x=0, y=0):
        """Initialize a :class:`GLabel` displaying a given label.

        Supplying x and y arguments sets the location of the :class:`GLabel` to
        (x, y). Recall that the location of a :class:`GLabel` is its bottom-left
        coordinate.

        :param label: The message to display in this :class:`GLabel`.
        :param x: The x-coordinate of the bottom-left corner of this rectangle.
        :param y: The y-coordinate of the bottom-left corner of this rectangle.
        """
        super().__init__()
        self._text = label
        self.font = _gfont.GFont.default()
        self.location = x, y

        # TODO(sredmond): Check that overriding bounds makes width and height work appropriately.
        # size = _platform.Platform().glabel_get_size(self)
        # self.width = size.width
        # self.height = size.height


    @property
    def font(self):
        """Get or set this :class:`GLabel`'s font."""
        return self._font

    @font.setter
    def font(self, font):
        if not isinstance(font, _gfont.GFont):
            font = _gfont.GFont.parse(font)

        self._font = font
        _platform.Platform().glabel_set_font(self, font)

        # size = _platform.Platform().glabel_get_size(self)
        # self.width = size.width
        # self.height = size.height

    @property
    def text(self):
        """Get or set this :class:`GLabel`'s label.

        Setting the label changes the internal state of the :class:`GLabel`,
        so a existing drawn labels will redisplay."""
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        _platform.Platform().glabel_set_label(self, text)

        # size = _platform.Platform().glabel_get_size(self)
        # self.width = size.width
        # self.height = size.height

    @property
    def ascent(self):
        """Return the maximum distance strings in this font ascend above the baseline."""
        return self.font.ascent

    @property
    def descent(self):
        """Return the maximum distance strings in this font descend below the baseline."""
        return self.font.descent

    @property
    def bounds(self):
        """Get the bounding box for this :class:`GLabel`.

        The bounding box of a :class:`GLabel` is the smallest rectangle that
        completely covers the displayed message.

        :returns: A bounding box that covers this :class:`GLabel`'s message.
        :rtype: :class:`GRectangle`
        """
        # TODO(sredmond): How do we handle bounds when there could be descent?

        if self._transformed: return _platform.Platform().gobject_get_bounds(self)
        width = self.font.measure(self.text)
        height = self.font.linespace
        # TODO(sredmond): This assumes that linespace is ascent + descent, and we top-justify
        # the bounding box so the actual box's y-coordinates go from y - ascent to y - ascent + height.
        return _gtypes.GRectangle(self.x, self.y - self.ascent, width, height)

    def __str__(self):
        return 'GLabel("{}")'.format(self.label)


class GPolygon(GFillableObject):
    """Graphical representation of a polygon.

    Polygons are bounded by line segments. A :class:`GPolygon` is initialized
    to an empty polygon with no vertices. To complete the figure, you need to
    add vertices to the polygon using the methods :meth:`add_vertex`,
    :meth:`add_edge`, or :meth:`add_polar_edge`.

    To add a filled red octagon to the center of the window::

        window = GWindow()
        edge_length = 75
        stop_sign = GPolygon()
        start = GPoint(-edge_length / 2, edge_length / 2 + edge_length / math.sqrt(2.0))
        stop_sign.add_vertex(start)
        for edge in range(8):
            stop_sign.add_polar_edge(edge_length, 45*edge)
        stop_sign.filled = True
        stop_sign.color = "RED"
        window.add(stop_sign, window.width / 2, window.height / 2)
    """

    def __init__(self):
        """Initialize an empty polygon at the origin."""
        super().__init__()
        self.last_x = 0
        self.last_y = 0
        self.vertices = []
        # _platform.Platform().gpolygon_constructor(self)

    def add_vertex(self, point):
        """Add a vertex at a given :class:`GPoint` relative to the polygon origin."""
        # TODO(sredmond): Flush out this documentation with the usual messages.
        x, y = point
        self.last_x = x
        self.last_y = y
        self.vertices.append(_gtypes.GPoint(x, y))
        _platform.Platform().gpolygon_add_vertex(self, x, y)

    def add_edge(self, dx, dy):
        """
        Adds an edge to the polygon whose components are given by the displacements
        dx and dy from the last vertex.
        """
        # TODO(sredmond): Fix documentation
        self.add_vertex((self.last_x + dx, self.last_y + dy))

    def add_polar_edge(self, r, theta):
        """
        Adds an edge to the polygon specified in polar coordinates.  The length
        of the edge is given by r, and the edge extends in
        direction theta, measured in degrees counterclockwise
        from the +x axis.

        @type r: float
        @type theta: float
        @param theta: degrees
        @rtype: void
        """
        # TODO(sredmond): Fix documentation
        self.add_edge(
            r * _gmath.cos_degrees(theta),
            -r * _gmath.sin_degrees(theta)
        )

    @property
    def bounds(self):
        """Get the bounding box for this :class:`GPolygon`.

        :returns: The bounding box of this :class:`GPolygon`.
        :rtype: :class:`GRectangle`
        """
        if self._transformed: return _platform.Platform().gobject_get_bounds(self)

        xs = [vertex.x for vertex in self.vertices]
        ys = [vertex.y for vertex in self.vertices]
        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)
        return _gtypes.GRectangle(min_x, min_y, max_x - min_x, max_y - min_y)


    def __contains__(self, point):
        """Implement ``point in self``.
        """
        # TODO(sredmond): Add the usual documentation here.
        x, y = point
        if self._transformed: return _platform.Platform().gobject_contains(self, x, y)

        # TOOD(sredmond): Verify this containment algorithm.
        crossings = 0

        n = len(self.vertices)
        if(n < 2): return False
        if(vertices[0] == vertices[n-1]): n = n - 1
        x0 = vertices[0].getX()
        y0 = vertices[0].getY()
        for i in range(1, n+1):
            x1 = vertices[i % n].getX()
            y1 = vertices[i % n].getY()
            if((y0 > y) != (y1 > y) and x - x0 < (x1-x0)*(y-y0)/(y1-y0)):
                crossings = crossings + 1
            x0 = x1
            y0 = y1
        return (crossings % 2 == 1)

    def __iter__(self):
        return iter(self.vertices)

    def __str__(self):
        return "GPolygon(num_vertices={})".format(len(self.vertices))


class GCompound(GObject, MutableSequence):
    """A graphics object that is a collection of other graphics objects.

    Once assembled, the contained :class:`GObject`s can be manipulated as a unit.

    The :class:`GCompound` has its own position, and items within in are drawn
    relative to that position.

    Internally, the :class:`GCompound` just holds a stack of its :class:`GObject`s.
    """
    # TODO(sredmond): I was a little delirious when I wrote this - take another look over it.
    # TODO(sredmond): It's a little weird to make this into a collection.
    def __init__(self):
        """Create an empty :class:`GCompound`."""
        super().__init__()
        self.contents = []
        _platform.Platform().gcompound_constructor(self)

    # These abstract methods end up adding a bunch of derived methods, some of which are nice.
    # One of these is __contains__, which we override for the point containment. That might break
    # something unexpectedly, so TODO(sredmond): Read more about these abstract superclasses and
    # make a call.
    def __getitem__(self, index):
        """Return the :class:`GObject` at the given index.

        The number is from back to front in the z-dimension. That is, index 0
        refers to the backmost element and index -1 refers to the frontmost element.
        """
        return self.contents[index]

    def __setitem__(self, index, value):
        self.contents[index] = value

    def __delitem__(self, index):
        gobj = self.contents.pop(index)
        _platform.Platform().gobject_remove(gobj)
        gobj._parent = None

    def __len__(self):  # Definitely keep this one!
        """Return the number of graphical objects stored in this :class:`GCompound`."""
        return len(self.contents)

    def insert(self, index, value):
        self.contents.insert(index, value)
        # TODO(sredmond): Also construct the object if it needs to be drawn.

    def add(self, gobj, x=None, y=None):
        """Add a new :class:`GObject` to this :class:`GCompound`.

        If two additional arguments x and y are both supplied, move the object
        to ``(x, y)`` first. It is an error to specify just one of x and y.

        :param gobj: The object to add to this compound.
        :param x: (optional) The x-coordinate of the location to which to move this object.
        :param y: (optional) The y-coordinate of the location to which to move this object.
        """
        # TODO(sredmond): Raise an error if only x or only y is set.
        if x is not None and y is not None:
            gobj.location = (x, y)

        # TODO(sredmond): Temporary override while resolving multiple image types.
        from campy.graphics.gimage import GImage

        # Dispatch the constructor to the appropriate backend constructor.
        if isinstance(gobj, GLine):
            _platform.Platform().gline_constructor(gobj)

        if isinstance(gobj, GImage):
            _platform.Platform().gimage_constructor(gobj)

        if isinstance(gobj, GRect):
            _platform.Platform().grect_constructor(gobj)

        if isinstance(gobj, GOval):
            _platform.Platform().goval_constructor(gobj)

        if isinstance(gobj, GArc):
            _platform.Platform().garc_constructor(gobj)

        if isinstance(gobj, GLabel):
            _platform.Platform().glabel_constructor(gobj)

        if isinstance(gobj, GPolygon):
            # TODO(sredmond): Warn against creating a polygon w/o enough vertices.
            _platform.Platform().gpolygon_constructor(gobj)

        _platform.Platform().gcompound_add(self, gobj)
        self.contents.append(gobj)
        gobj._parent = self

    def remove(self, gobj):
        """Remove a :class:`GObject` from this :class:`GCompound`.

        Return whether or not the :class:`GCompound` contained the :class:`GObject`.

        :param gobj: The object to remove.
        :returns: Whether this compound contained the object.
        """
        # TODO(sredmond): People familiar with Python lists might expect this to raise a ValueError if the gobj isn't there.

        # TODO(sredmond): Don't blindly delete from the backend if it's not added.
        _platform.Platform().gobject_remove(gobj)

        try:
            self.contents.remove(gobj)
        except ValueError:
            return False
        else:
            return True

    def clear(self):
        """Remove all graphical objects from the GCompound."""
        while self.contents:
            self.pop()

    @property
    def bounds(self):
        """Get the bounding box for this :class:`GCompound`.

        The bounding box of a :class:`GCompound` is the smallest rectangle that
        covers all of its components bounding boxes.

        :returns: A bounding box that covers all of this compounds components.
        :rtype: :class:`GRectangle`
        """
        if self._transformed:
            return _platform.Platform().gobject_get_bounds(self)

        min_x = min((obj.x for obj in self.contents), default=-1)
        min_y = min((obj.y for obj in self.contents), default=-1)
        max_x = max((obj.x + obj.width for obj in self.contents), default=-1)
        max_y = max((obj.y + obj.height for obj in self.contents), default=-1)

        return _gtypes.GRectangle(min_x, min_y, max_x - min_x, max_y - min_y)

    def __contains__(self, point):
        """Implement ``point in self``.

        Check whether a given :class:`GPoint` or 2-element tuple is contained
        within the bounding box of this :class:`GCompound`. A point is contained
        within a GCompound if it is contained within any of the components.
        """
        # Attempt to unpack the supplied point as a tuple.
        x, y = point

        if self._transformed:
            return _platform.Platform().gobject_contains(self, x, y)

        return any((x, y) in obj for obj in self.contents)

    def send_forward(self, gobj):
        try:
            index = self.contents.find(gobj)
        except ValueError:
            return
        else:
            if index != len(self) - 1:
                self.contents.pop(index)
                self.contents.insert(index + 1, gobj)
                _platform.Platform().gobject_send_forward(gobj)

    def send_to_front(self, gobj):
        try:
            index = self.contents.find(gobj)
        except ValueError:
            return
        else:
            if index != len(self) - 1:
                self.contents.pop(index)
                self.contents.append(index + 1, gobj)
                _platform.Platform().gobject_send_to_front(gobj)

    def send_backward(self, gobj):
        try:
            index = self.contents.find(gobj)
        except ValueError:
            return
        else:
            if index > 0:
                self.contents.pop(index)
                self.contents.insert(index - 1, gobj)
                _platform.Platform().gobject_send_backward(gobj)

    def send_to_back(self, gobj):
        try:
            index = self.contents.find(gobj)
        except ValueError:
            return
        else:
            if index > 0:
                self.contents.pop(index)
                self.contents.insert(0, gobj)
                _platform.Platform().gobject_send_to_back(gobj)


    # TODO(sredmond): Search for a way to not explicitly load this class setter.
    @GObject.location.setter # Overload the superclass location setter
    def location(self, point):
        x, y = point
        dx = x - self.x
        dy = y - self.y
        # TODO(sredmond): Python magic!
        GObject.location.fset(self, point)  # Move the compound to the requested location.
        # Move each component by the same amount.
        # TODO(sredmond): Does the Java backend already move contained elements?
        for element in self.contents:
            element.move(dx, dy)

    def __iter__(self):
        return iter(self.contents)
