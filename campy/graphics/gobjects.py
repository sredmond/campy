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
import campy.graphics.gtypes as _gtypes
import campy.graphics.gcolor as _gcolor
import campy.private.platform as _platform
import campy.graphics.gmath as _gmath

import collections
import math

__ARC_TOLERANCE__ = 2.5 # Default arc tolerance
__DEFAULT_CORNER__ = 10 # Default corner rounding
__DEFAULT_GLABEL_FONT__ = "Dialog-13" # Default label font


class GObject:
    """The common superclass of all graphical objects that can be displayed on a graphical window.

    For examples illustrating the use of the GObject class, see the descriptions
    of the individual subclasses.
    """
    def __init__(self):
        """Initialize a GObject with reasonable default values."""
        self._x = 0.0
        self._y = 0.0

        self._color = ""
        self._line_width = 1.0
        self._visible = True

        self._transformed = False
        self._parent = None

    @property
    def x(self):
        """Get the x-coordinate of this :class:`GObject`."""
        return self._x

    @property
    def y(self):
        """Get the y-coordinate of this :class:`GObject`."""
        return self._y

    # TODO(sredmond): Should I expose setters for x and y?

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
        x, y = pt
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
    """Represents a graphical object that can be filled.

    Adds a _filled attribute to the subclass instance as
    well as a _fill_color.
    """
    def __init__(self, filled=False, fill_color=''):
        super().__init__()
        self._filled = False
        self._fill_color = fill_color

    @property
    def filled(self):
        """Return whether this object is filled.

        @rtype: boolean
        """
        return self._filled

    @filled.setter
    def filled(self, is_filled):
        """Set whether the object is filled.

        True means filled and False means outlined."""
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
        # color = _gcolor.canonicalize(color)
        # hex_color = color.to_hex()
        self._fill_color = color
        _platform.Platform().gobject_set_fill_color(self, self._fill_color.as_hex)

# END SECTION: Graphical Mixins


class GRect(GObject):
    '''
    This class represents a graphical object whose appearance consists of
    a rectangular box.  For example, the following code adds a filled, red
    200x100 rectangle
    at the upper left corner of the graphics window::

        gw = _gwindow.GWindow()
        print("This program draws a red rectangle at (0, 0).")
        rect = gobjects.GRect(0, 0, 200, 100)
        rect.setFilled(true)
        rect.setColor("RED")
        gw.add(rect)
    '''

    def __init__(self, width, height, x=None, y=None):
        '''
        Initializes a rectangle with the specified width and height.  The first
        form is positioned at the origin; the second at the coordinates
        given by x and y.

        @type width: float
        @type height: float
        @type x: float
        @type y: float
        @rtype: void
        '''
        GObject.__init__(self)
        self.create(width, height)
        if(x != None and y != None):
            self.setLocation(x=x, y=y)

    def create(self, width, height):
        '''
        Internal helper method
        '''
        self.x = 0.0
        self.y = 0.0
        self.width = width
        self.height = height
        self.fillFlag = False
        self.fillColor = ""
        _platform.Platform().grect_constructor(self, width, height)

    def setSize(self, size=None, width=None, height=None):
        '''
        Changes the size of this rectangle to the specified width and height.

        @type size: GDimention
        @type width: float
        @type height: float
        @param size: GDimension, will override height and width
        @rtype: void
        '''
        if(size != None):
            width = size.getWidth()
            height = size.getHeight()

        if(width == None or height == None): return

        if(self.transformed):
            raise Exception("setSize: Object has been transformed")

        self.width = width
        self.height = height
        _platform.Platform().gobject_set_size(self, width, height)

    def setBounds(self, bounds=None, x=None, y=None, width=None, height=None):
        '''
        Changes the bounds of this rectangle to the specified values.

        @type bounds: GRectangle
        @type x: float
        @type y: float
        @type width: float
        @type height: float
        @param bounds: bounding rectangle, will override other parameters
        @rtype: void
        '''
        if(bounds != None):
            x = bounds.getX()
            y = bounds.getY()
            width = bounds.getWidth()
            height = bounds.getHeight()

        if(x == None or y == None or width == None or height == None): return

        self.setLocation(x=x, y=y)
        self.setSize(width=width, height=height)

    def getBounds(self):
        '''
        Returns the bounds of this rectangle

        @rtype: GRectangle
        '''
        if(self.transformed): return _platform.Platform().gobject_get_bounds(self)
        return _gtypes.GRectangle(self.x, self.y, self.width, self.height)

    def setFilled(self, flag):
        '''
        Sets the fill status for the rectangle, where false is
        outlined and true is filled.

        @type flag: boolean
        @rtype: void
        '''
        self.fillFlag = flag
        _platform.Platform().gobject_set_filled(self, flag)

    def isFilled(self):
        '''
        Returns true if the rectangle is filled.

        @rtype: boolean
        '''
        return self.fillFlag

    def setFillColor(self, color="", rgb=None):
        '''
        Sets the color used to display the filled region of this rectangle.

        @type color: string
        @type rgb: int
        @param color: will override rgb
        @rtype: void
        '''
        self.fillColor = color
        if(color != None and color != ""):
            rgb = _gcolor.color_to_rgb(color)

        if(rgb == None): return

        color = _gcolor.rgb_to_hex(rgb)
        _platform.Platform().gobject_set_fill_color(self, color)

    def getFillColor(self):
        '''
        Returns the color used to display the filled region of this rectangle.  If
        none has been set, getFillColor returns the empty string.

        @rtype: string
        '''
        return self.fillColor

    def getType(self):
        '''
        Returns the type of this object

        @rtype: string
        '''
        return "GRect"

    def toString(self):
        '''
        Returns a string form of this object

        @rtype: string
        '''
        return "GRect(" + str(self.x) + ", " + str(self.y) + ", " + \
                str(self.width) + ", " + str(self.height) + ")"



class GRoundRect(GRect):
    '''
    This class represents a graphical object whose appearance consists
    of a rectangular box with rounded corners.
    '''

    def __init__(self, width, height, x = 0, y = 0, corner = __DEFAULT_CORNER__):
        '''
        Initializes a new rectangle with the specified width and height.  If
        the x and y parameters are specified, they
        are used to specify the origin.  The corner parameter
        specifies the diameter of the arc forming the corner.

        @type width: float
        @type height: float
        @type x: float
        @type y: float
        @type corner: float
        @rtype: void
        '''
        GRect.__init__(self, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.corner = corner
        self.fillFlag = False
        self.fillColor = ""
        _platform.Platform().groundrect_constructor(self, width, height, corner)
        self.setLocation(x=x, y=y)

    def getType(self):
        '''
        Returns the type of this object

        @rtype: string
        '''
        return "GRoundRect"

    def toString(self):
        '''
        Returns a string version of this object

        @rtype: string
        '''
        return "GRoundRect(" + str(self.x) + ", " + str(self.y) + ", " + \
                str(self.width) + ", " + str(self.height) + ", " + \
                str(self.corner) + ")"

class G3DRect(GRect):
    '''
    This graphical object subclass represents a rectangular box that can
    be raised or lowered.
    '''

    def __init__(self, width, height, x = 0, y = 0, raised = False):
        '''
        Initializes a new 3D rectangle with the specified width and height.  If
        the x and y parameters are specified, they
        are used to specify the origin.  The raised parameter
        determines whether the rectangle should be drawn with highlights that
        suggest that it is raised about the background.

        @type width: float
        @type height: float
        @type x: float
        @type y: float
        @type raised: boolean
        @rtype: void
        '''
        GRect.__init__(self, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.raised = raised
        self.fillFlag = False
        self.fillColor = ""
        _platform.Platform().g3drect_constructor(self, width, height, str(raised).lower())
        self.setLocation(x=x, y=y)

    def setRaised(self, raised):
        '''
        Indicates whether this object appears raised.

        @type raised: boolean
        @rtype: void
        '''
        self.raised = raised
        _platform.Platform().g3drect_set_raised(self, str(raised).lower())

    def isRaised(self):
        '''
        Returns true if this object appears raised.

        @rtype: boolean
        '''
        return self.raised

    def getType(self):
        '''
        Returns the type of this object

        @rtype: string
        '''
        return "G3DRect"

    def toString(self):
        '''
        Returns the string form of this object

        @rtype: string
        '''
        return "G3DRect(" + str(self.x) + ", " + str(self.y) + ", " + \
                str(self.width) + ", " + str(self.height) + ", " + \
                str(self.raised).lower() + ")"

class GOval(GFillableObject):
    '''
    This graphical object subclass represents an oval inscribed in
    a rectangular box.  For example, the following code displays a
    filled green oval inscribed in the graphics window::

        gw = _gwindow.GWindow()
        print("This program draws a green oval filling the window.")
        oval = gobjects.GOval(gw.getWidth(), gw.getHeight())
        oval.setFilled(true)
        oval.setColor("GREEN")
        gw.add(oval)
    '''

    def __init__(self, width, height, x=0, y=0):
        '''
        Initializes a new oval inscribed in the specified rectangle.  The
        first form is positioned at the origin; the second at the coordinates
        given by x and y.

        @type width: float
        @type height: float
        @type x: float
        @type y: float
        @rtype: void
        '''
        GObject.__init__(self)
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.fillFlag = False
        self.fillColor = ""
        _platform.Platform().goval_constructor(self, width, height)
        self.setLocation(x=x, y=y)

    def setSize(self, width=None, height=None, size=None):
        '''
        Changes the size of the bounding rectangle to the specified width
        and height.

        @type width: float
        @type height: float
        @type size: GDimension
        @param size: will override height and width parameters
        @rtype: void
        '''
        if(self.transformed): raise Exception("setSize: Object has been transformed")
        if(size != None):
            width = size.width
            height = size.height

        self.width = width
        self.height = height
        _platform.Platform().gobject_set_size(self, width, height)

    def setBounds(self, x=None, y=None, width=None, height=None, bounds=None):
        '''
        Changes the bounds of the oval to the specified values.

        @type x: float
        @type y: float
        @type width: float
        @type height: float
        @type bounds: GRectangle
        @param bounds: will override all other parameters
        @rtype: void
        '''
        if(bounds != None):
            x, y, width, height = bounds

        self.setLocation(x=x, y=y)
        self.setSize(width, height)

    def getBounds(self):
        '''
        Returns the GRectangle bounding this object

        @rtype: GRectangle
        '''
        if(self.transformed): return _platform.Platform().gobject_get_bounds(self)
        return _gtypes.GRectangle(self.x, self.y, self.width, self.height)

    def contains(self, x, y):
        '''
        Returns whether or not the oval contains the given point x, y

        @rtype: boolean
        '''
        if(self.transformed): return _platform.Platform().gobject_contains(self, x, y)
        rx = self.width / 2
        ry = self.height / 2
        if(rx == 0 or ry == 0): return False
        dx = x - (self.x + rx)
        dy = y - (self.y + ry)
        return (dx * dx) / (rx * rx) + (dy * dy) / (ry * ry) <= 1.0

    def setFilled(self, flag):
        '''
        Sets the fill status for the oval, where false is
        outlined and true is filled.

        @type flag: boolean
        @rtype: void
        '''
        self.fillFlag = flag
        _platform.Platform().gobject_set_filled(self, flag)

    def isFilled(self):
        '''
        Returns true if the oval is filled.

        @rtype: boolean
        '''
        return self.fillFlag

    def setFillColor(self, color = None, rgb = None):
        '''
        Sets the color used to display the filled region of this oval.

        @type color: string
        @type rgb: int
        @param color: will override rgb parameter
        @rtype: void
        '''
        self.fillColor = color
        if(color != None and color != ""):
            rgb = _gcolor.color_to_rgb(color)
        if(rgb != None):
            self.fillColor = _gcolor.rgb_to_hex(rgb)
        _platform.Platform().gobject_set_fill_color(self, self.fillColor)

    def getFillColor(self):
        '''
        Returns the color used to display the filled region of this oval.  If
        none has been set, getFillColor returns the empty string.

        @rtype: string
        '''
        return self.fillColor

    def getType(self):
        '''
        Returns the type of this object

        @rtype: string
        '''
        return "GOval"

    def toString(self):
        '''
        Returns the string form of this object

        @rtype: string
        '''
        return "GOval(" + str(self.x) + ", " + str(self.y) + ", " + \
                str(self.width) + ", " + str(self.height) + ")"

class GArc(GObject):
    '''
    This graphical object subclass represents an elliptical arc.  The
    arc is specified by the following parameters::

        - The coordinates of the bounding rectangle (x, y, width, height)
        - The angle at which the arc starts (start)
        - The number of degrees that the arc covers (sweep)

    All angles in a GArc description are measured in
    degrees moving counterclockwise from the +x axis.  Negative
    values for either start or sweep indicate
    motion in a clockwise direction.
    '''

    def __init__(self, width, height, start, sweep, x=0, y=0):
        '''
        Initializes a new GArc object consisting of an elliptical arc.
        The first form creates a GArc whose origin is the point
        (0, 0); the second form positions the GArc at the
        point (x, y).

        @type width: float
        @type height: float
        @type start: float
        @param start: degrees
        @type sweep: float
        @param sweep: degrees
        @type x: float
        @type y: float
        @rtype: void
        '''
        GObject.__init__(self)
        self.x = x
        self.y = y
        self.frameWidth = width
        self.frameHeight = height
        self.start = start
        self.sweep = sweep
        self.fillFlag = False
        self.fillColor = ""
        _platform.Platform().garc_constructor(self, width, height, start, sweep)
        self.setLocation(x=x, y=y)

    def setStartAngle(self, start):
        '''
        Sets the starting angle for this GArc object.

        @type start: float
        @param start: degrees
        @rtype: void
        '''
        self.start = start
        _platform.Platform().garc_set_start_angle(self, start)

    def getStartAngle(self):
        '''
        Returns the starting angle for this GArc object.

        @rtype: float
        @return: degrees
        '''
        return self.start

    def setSweepAngle(self, sweep):
        '''
        Sets the sweep angle for this GArc object.

        @type sweep: float
        @param sweep: degrees
        @rtype: void
        '''
        self.sweep = sweep
        _platform.Platform().garc_set_sweep_angle(self, sweep)

    def getSweepAngle(self):
        '''
        Returns the sweep angle for this GArc object.

        @return: degrees
        @rtype: float
        '''
        return self.sweep

    def getStartPoint(self):
        '''
        Returns the point at which the arc starts.

        @rtype: GPoint
        '''
        return getArcPoint(self.start)

    def getEndPoint(self):
        '''
        Returns the point at which the arc ends.

        @rtype: GPoint
        '''
        return getArcPoint(self.start + self.sweep)

    def setFrameRectangle(self, x=None, y=None, width=None, height=None, rect=None):
        '''
        Changes the boundaries of the rectangle used to frame the arc.

        @type x: float
        @type y: float
        @type width: float
        @type height: float
        @type rect: GRectangle
        @param rect: bounding frame, will override other parameters
        @rtype: void
        '''
        if(rect != None):
            x = rect.getX()
            y = rect.getY()
            width = rect.getWidth()
            height = rect.getHeight()

        self.x = x
        self.y = y
        self.frameWidth = width
        self.frameHeight = height
        _platform.Platform().garc_set_frame_rectangle(self, x, y, width, height)

    def getFrameRectangle(self):
        '''
        Returns the boundaries of the rectangle used to frame the arc.

        @rtype: GRectangle
        '''
        return _gtypes.GRectangle(0,0,0,0) #!!

    def setFilled(self, flag):
        '''
        Sets the fill status for the arc, where false is
        outlined and true is filled.  If a GArc is
        unfilled, the figure consists only of the arc itself.  If a
        GArc is filled, the figure consists of the
        pie-shaped wedge formed by connecting the endpoints of the arc to
        the center.  As an example, the following program draws a 270-degree
        arc starting at 45 degrees, filled in yellow, much like the character
        in the PacMan video game::

            gw = _gwindow.GWindow()
            print("This program draws the PacMan character.")
            cx = gw.getWidth() / 2
            cy = gw.getHeight() / 2
            r = 25
            pacman = gobjects.GArc(cx - r, cy - r, 2*r, 2*r, 45, 270)
            pacman.setFilled(True)
            pacman.setFillColor("YELLOW")
            gw.add(pacman)

        @type flag: boolean
        @rtype: void
        '''
        self.fillFlag = flag
        _platform.Platform().gobject_set_filled(self, flag)

    def getFilled(self):
        '''
        Returns true if the arc is filled.

        @rtype: boolean
        '''
        return self.fillFlag

    def setFillColor(self, color=None, rgb=None):
        '''
        Sets the color used to display the filled region of this arc.
        Colors are specified as strings as described in the notes for the setColor method.

        @type color: string
        @type rgb: int
        @param color: will override rgb
        @rtype: void
        '''
        self.fillColor = color
        if(color != None and color != ""):
            rgb = _gcolor.color_to_rgb(color)
        if(rgb != None):
            self.fillColor = _gcolor.rgb_to_hex(rgb)
        _platform.Platform().gobject_set_fill_color(self, self.fillColor)

    def getFillColor(self):
        '''
        Returns the color used to display the filled region of this arc.  If
        none has been set, getFillColor returns the empty string.

        @rtype: string
        '''
        return self.fillColor

    def getBounds(self):
        '''
        Gets the bounding rectangle for this object

        @rtype: GRectangle
        '''
        if(self.transformed): return _platform.Platform().gobject_get_bounds(self)
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
        if (self.containsAngle(0)): xMax = cx + rx
        if (self.containsAngle(90)): yMin = cy - ry
        if (self.containsAngle(180)): xMin = cx - rx
        if (self.containsAngle(270)): yMax = cy + ry
        if (self.isFilled()):
            xMin = min(xMin, cx)
            yMin = min(yMin, cy)
            xMax = max(xMax, cx)
            yMax = max(yMax, cy)
        return _gtypes.GRectangle(xMin, yMin, xMax - xMin, yMax - yMin)

    def contains(self, x, y):
        '''
        Returns whether or not this object contains the point x, y

        @type x: float
        @type y: float
        @rtype: boolean
        '''
        if(self.transformed): return _platform.Platform().gobject_contains(self, x, y)
        rx = frameWidth / 2
        ry = frameHeight / 2
        if (rx == 0 or ry == 0): return False
        dx = x - (self.x + rx)
        dy = y - (self.y + ry)
        r = (dx * dx) / (rx * rx) + (dy * dy) / (ry * ry)
        if(self.fillFlag):
            if (r > 1.0): return False
        else:
            t = ARC_TOLERANCE / ((rx + ry) / 2) #!!
            if (abs(1.0 - r) > t): return False
        return self.containsAngle(math.atan2(-dy, dx) * 180 / _gmath.PI)

    def getType(self):
        '''
        Returns the type of this object

        @rtype: string
        '''
        return "GArc"

    def toString(self):
        '''
        Returns the string form of this object

        @rtype: string
        '''
        return "GArc(" + str(self.x) + ", " + str(self.y) + ", " + \
                str(self.frameWidth) + ", " + str(self.frameHeight) + ", " + \
                str(self.start) + ", " + str(self.sweep) + ")"

    def getArcPoint(self, theta):
        '''
        Internal method
        '''
        rx = self.frameWidth / 2
        ry = self.frameHeight / 2
        cx = self.x + rx
        cy = self.y + ry
        radians = theta * _gmath.PI / 180
        return _gtypes.GPoint(cx + rx * math.cos(radians), cy - ry * math.sin(radians))

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
        _platform.Platform().gline_constructor(self, self._x0, self._y0, self._x1, self._y1)

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
        end_x, end_y = start_point
        self._x1 = end_x
        self._y1 = end_y
        _platform.Platform().gline_set_start_point(self, self._x1, self._y1)

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

class GImage(GObject):
    '''
    This graphical object subclass represents an image from a file.
    For example, the following code displays a GImage
    containing the Stanford tree at the center of the window, assuming
    that the image file StanfordTree.png exists, either in
    the current directory or an images subdirectory::

        gw = _gwindow.GWindow()
        print("This program draws the Stanford tree.")
        tree = gobjects.GImage("StanfordTree.png")
        x = (gw.getWidth() - tree.getWidth()) / 2
        y = (gw.getHeight() - tree.getHeight()) / 2
        gw.add(tree, x, y)
    '''

    def __init__(self, filename, x=0, y=0):
        '''
        Initializes a new image by loading the image from the specified
        file, which is either in the current directory or a subdirectory named
        images.  By default, the upper left corner of the image
        appears at the origin; the second form automatically sets the location
        to the point (x, y).

        @type filename: string
        @type x: float
        @type y: float
        @rtype: void
        '''
        GObject.__init__(self)
        self.filename = filename
        size = _platform.Platform().gimage_constructor(self, filename)
        self.width = size.getWidth()
        self.height = size.getHeight()
        self.setLocation(x=x, y=y)

    def getBounds(self):
        '''
        Returns the bounding rectangle for this object

        @rtype: GRectangle
        '''
        if(self.transformed): return _platform.Platform().gobject_get_bounds(self)
        return _gtypes.GRectangle(self.x, self.y, self.width, self.height)

    def __str__(self):
        return 'GImage("{}")'.format(self.filename)

class GLabel(GObject):
    '''
    This graphical object subclass represents a text string.  For
    example, the following code adds a GLabel containing
    the string "hello, world" to the center of the window::

        gw = _gwindow.GWindow()
        print("This program draws the 'hello, world' message.")
        label = gobjects.GLabel("hello, world")
        label.setFont("SansSerif-18")
        x = (gw.getWidth() - label.getWidth()) / 2
        y = (gw.getHeight() + label.getFontAscent()) / 2
        gw.add(label, x, y)

    Controlling the appearance and positioning of a GLabel
    depends on understanding the following terms:

        - The baseline is the horizontal line on which the characters rest.
        - The origin is the point on the baseline at which the label begins.
        - The height is the distance that separate two successive lines.
        - The ascent is the maximum distance a character in this font extends above the baseline.
        - The descent is the maximum distance a character in this font extends below the baseline.
    '''

    def __init__(self, str, x=0, y=0):
        '''
        Initializes a GLabel object containing the specified string.
        By default, the baseline of the first character appears at the origin;
        the second form automatically resets the location of the
        GLabel to the point (x, y).

        @type str: string
        @type x: float
        @type y: float
        @rtype: void
        '''
        GObject.__init__(self)
        self.str = str
        _platform.Platform().glabel_constructor(self, str)
        self.setFont(__DEFAULT_GLABEL_FONT__)
        size = _platform.Platform().glabel_get_size(self)
        self.width = size.width
        self.height = size.height
        self._ascent = _platform.Platform().glabel_get_font_ascent(self)
        self._descent = _platform.Platform().glabel_get_font_descent(self)
        self.setLocation(x=x, y=y)

    def setFont(self, font):
        '''
        Changes the font used to display the GLabel as specified by
        the string font, which has the following format:

        family-style-size

        where both style and size are optional.
        If any of these elements are missing or specified as an asterisk,
        the existing value is retained.

        @type font: string
        @rtype: void
        '''
        self.font = font
        _platform.Platform().glabel_set_font(self, font)
        size = _platform.Platform().glabel_get_size(self)
        self.width = size.width
        self.height = size.height
        self._ascent = _platform.Platform().glabel_get_font_ascent(self)
        self._descent = _platform.Platform().glabel_get_font_descent(self)

    def getFont(self):
        '''
        Returns the current font for the GLabel.

        @rtype: string
        '''
        return self.font

    def setLabel(self, str):
        '''
        Changes the string stored within the GLabel object, so that
        a new text string appears on the display.

        @type str: string
        @rtype: void
        '''
        self.str = str
        _platform.Platform().setLabel(self, str)
        size = _platform.Platform().glabel_get_size(self)
        self.width = size.width
        self.height = size.height

    def getLabel(self):
        '''
        Returns the string displayed by this object.

        @rtype: string
        '''
        return self.str

    @property
    def ascent(self):
        """Return the maximum distance strings in this font ascend above the baseline."""
        return self._ascent

    @property
    def descent(self):
        """Return the maximum distance strings in this font descend below the baseline."""
        return self._descent

    def getFontAscent(self):
        '''
        Returns the maximum distance strings in this font extend above
        the baseline.

        @rtype: float
        '''
        return self.ascent

    def getFontDescent(self):
        '''
        Returns the maximum distance strings in this font descend below
        the baseline.

        @rtype: float
        '''
        return self._descent

    def getBounds(self):
        '''
        Returns the bounding rectangle for this object

        @rtype: GRectangle
        '''
        if(self.transformed): return _platform.Platform().gobject_get_bounds(self)
        return _gtypes.GRectangle(self.x, self.y - self._ascent, self.width, self.height)

    def getType(self):
        '''
        Returns the type of this object

        @rtype: string
        '''
        return "GLabel"

    def toString(self):
        '''
        Returns the string form of this object

        @rtype: string
        '''
        return "GLabel(\"" + self.str + "\")"

class GPolygon(GObject):
    '''
    This graphical object subclass represents a polygon bounded by
    line segments.  The GPolygon constructor creates an
    empty polygon.  To complete the figure, you need to add vertices
    to the polygon using the methods addVertex, addEdge, addPolarEdge.
    As an example, the following code adds a filled red octagon to
    the center of the window::

        gw = _gwindow.GWindow()
        print("This program draws a red octagon.")
        edge = 75
        stopSign = gobjects.GPolygon()
        stopSign.addVertex(-edge / 2, edge / 2 + edge / math.sqrt(2.0))
        for i in range(8):
            stopSign.addPolarEdge(edge, 45i)
        stopSign.setFilled(True)
        stopSign.setColor("RED")
        gw.add(stopSign, gw.getWidth() / 2, gw.getHeight() / 2)
    '''

    def __init__(self):
        '''
        Initializes a new empty polygon at the origin.

        @rtype: void
        '''
        GObject.__init__(self)
        self.fillFlag = False
        self.fillColor = ""
        self.cx = None
        self.cy = None
        self.vertices = []
        _platform.Platform().gpolygon_constructor(self)

    def addVertex(self, x, y):
        '''
        Adds a vertex at (x, y) relative to the polygon
        origin.

        @type x: float
        @type y: float
        @rtype: void
        '''
        self.cx = x
        self.cy = y
        self.vertices.append(_gtypes.GPoint(x, y))
        _platform.Platform().gpolygon_add_vertex(self, x, y)

    def addEdge(self, dx, dy):
        '''
        Adds an edge to the polygon whose components are given by the displacements
        dx and dy from the last vertex.

        @type dx: float
        @type dy: float
        @rtype: void
        '''
        self.addVertex(self.cx + dx, self.cy + dy)

    def addPolarEdge(self, r, theta):
        '''
        Adds an edge to the polygon specified in polar coordinates.  The length
        of the edge is given by r, and the edge extends in
        direction theta, measured in degrees counterclockwise
        from the +x axis.

        @type r: float
        @type theta: float
        @param theta: degrees
        @rtype: void
        '''
        self.addEdge(r*math.cos(theta*_gmath.PI/180), \
                    -r*math.sin(theta*_gmath.PI/180))

    def getVertices(self):
        '''
        Returns a list of the points in the polygon.

        @rtype: [GPoint]
        @return: list of GPoints
        '''
        return self.vertices

    def setFilled(self, flag):
        '''
        Sets the fill status for the polygon, where false is
        outlined and true is filled.

        @type flag: boolean
        @rtype: void
        '''
        self.fillFlag = flag
        _platform.Platform().gobject_set_filled(self, flag)

    def isFilled(self):
        '''
        Returns true if the polygon is filled.

        @rtype: boolean
        '''
        return self.fillFlag

    def setFillColor(self, color=None, rgb=None):
        '''
        Sets the color used to display the filled region of this polygon.

        @type color: string
        @type rgb: int
        @param color: will override rgb
        @rtype: void
        '''
        self.fillColor = color
        if(color != None and color != ""):
            rgb = _gcolor.color_to_rgb(color)
        if(rgb != None):
            self.fillColor = _gcolor.rgb_to_hex(rgb)
        _platform.Platform().gobject_set_fill_color(self, self.fillColor)

    def getFillColor(self):
        '''
        Returns the color used to display the filled region of this polygon.  If
        none has been set, getFillColor returns the empty string.

        @rtype: string
        '''
        return self.fillColor

    def getBounds(self):
        '''
        Returns the bounding rectangle for this object

        @rtype: GRectangle
        '''
        if(self.transformed): return _platform.Platform().gobject_get_bounds(self)
        xMin = 0
        yMin = 0
        xMax = 0
        yMax = 0
        for i in range(len(self.vertices)):
            x = vertices[i].getX()
            y = vertices[i].getY()
            if(i==0 or x < xMin): xMin = x
            if(i==0 or y < yMin): yMin = y
            if(i==0 or x > xMax): xMax = x
            if(i==0 or y > yMax): yMax = y
        return _gtypes.GRectangle(xMin, yMin, xMax - xMin, yMax - yMin)

    def contains(self, x, y):
        '''
        Returns whether or not this object contains the point x, y

        @type x: float
        @type y: float
        @rtype: boolean
        '''
        if(self.transformed): return _platform.Platform().gobject_contains(self, x, y)
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

    def __str__(self):
        return "GPolygon(num_vertices={})".format(len(self.vertices))


class GCompound(GObject, collections.abc.MutableSequence):
    """A collection of other graphics objects.

    Once assembled, the contained :class:`GObject`s can be manipulated as a unit.

    The :class:`GCompound` has its own position, and items within in are drawn
    relative to that position.

    Internally, the :class:`GCompound` just holds a stack of its :class:`GObject`s.
    """

    def __init__(self):
        """Create an empty :class:`GCompound`."""
        super().__init__(self)
        self.contents = []
        _platform.Platform().gcompound_constructor(self)

    def add(self, gobj, x=None, y=None):
        '''
        Adds a new graphical object to the GCompound.  The second
        form moves the object to the point (x, y) first.

        @type gobj: GObject
        @type x: float
        @type y: float
        @rtype: void
        '''
        if(x != None and y != None):
            gobj.setLocation(x=x, y=y)

        _platform.Platform().gcompound_add(self, gobj)
        self.contents.append(gobj)
        gobj.parent = self

    def remove(self, gobj):
        '''
        Removes the specified object from the GCompound.

        @type gobj: GObject
        @rtype: void
        '''
        index = self.findGObject(gobj)
        if(index != -1): self.removeAt(index)
        # TODO(sredmond): Return a boolean value here.

    def removeAll(self):
        '''
        Removes all graphical objects from the GCompound.

        @rtype: void
        '''
        while(len(self.contents) > 0):
            self.removeAt(0)

    def getElementCount(self):
        '''
        Returns the number of graphical objects stored in the
        GCompound.

        @rtype: int
        '''
        return len(self.contents)

    def getElement(self, index):
        '''
        Returns the graphical object at the specified index,
        numbering from back to front in the the z dimension.

        @rtype: GObject
        '''
        return self.contents[index]

    def getBounds(self):
        '''
        Returns a bounding rectangle for this compound.

        @rtype: GRectangle
        '''
        if(self.transformed): return _platform.Platform().gobject_get_bounds(self)
        import sys
        xMin = sys.float_info.max
        yMin = sys.float_info.max
        xMax = sys.float_info.min
        yMax = sys.float_info.min
        for i in range(len(self.contents)):
            bounds = self.contents[i].getBounds()
            xMin = min(xMin, bounds.getX())
            yMin = min(yMin, bounds.getY())
            xMax = max(xMax, bounds.getX())
            yMax = max(yMax, bounds.getY())

        return _gtypes.GRectangle(xMin, yMin, xMax - xMin, yMax - yMin)

    def contains(self, x, y):
        '''
        Checks if this GCompound contains the given point

        @type x: float
        @type y: float
        @rtype: boolean
        '''
        if(self.transformed): return _platform.Platform().gobject_contains(self, x, y)
        for i in range(len(self.contents)):
            if(self.contents[i].contains(x, y)): return True
        return False

    def sendForward(self, gobj):
        '''
        Internal method
        '''
        index = self.findGObject(gobj)
        if(index == -1): return
        if(index != len(self.contents)-1):
            self.contents.pop(index)
            self.contents.insert(index + 1, gobj)
            _platform.Platform().gobject_send_forward(gobj)

    def sendToFront(self, gobj):
        '''
        Internal method
        '''
        index = self.findGObject(gobj)
        if(index == -1): return
        if(index != len(self.contents)-1):
            self.contents.pop(index)
            self.contents.append(gobj)
            _platform.Platform().gobject_send_to_front(gobj)

    def sendBackward(self, gobj):
        '''
        Internal method
        '''
        index = self.findGObject(gobj)
        if(index == -1): return
        if(index != 0):
            self.contents.pop(index)
            self.contents.insert(index - 1, gobj)
            _platform.Platform().gobject_send_backward(gobj)

    def sendToBack(self, gobj):
        '''
        Internal method
        '''
        index = self.findGObject(gobj)
        if(index == -1): return
        if(index != 0):
            self.contents.pop(index)
            self.contents.insert(0, gobj)
            _platform.Platform().gobject_send_to_back(gobj)

    def findGObject(self, gobj):
        '''
        Internal method
        '''
        n = len(self.contents)
        for i in range(n):
            if(self.contents[i] == gobj): return i # comparison ok? I think so
        return -1

    def removeAt(self, index):
        '''
        Internal method
        '''
        gobj = self.contents[index]
        self.contents.pop(index)
        _platform.Platform().gobject_remove(gobj)
        gobj.parent = None

    def __iter__(self):
        return iter(self.contents)
