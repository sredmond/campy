# File: pgl.py

"""
The pgl module implements the Portable Graphics Library (pgl) on top of
Tkinter, which is the most common graphics package for use with Python.
"""

PGL_VERSION = 0.83
PGL_DATE = "06-Nov-2018"

import atexit
import inspect
import math
import sys
import time

try:
    import tkinter
    try:
        import tkinter.font as tkFont
    except Exception:
        import tkFont
except Exception as e:
    print('Could not load tkinter: ' + str(e))

try:
    from PIL import ImageTk, Image
    _imageModel = "PIL"
except Exception:
    _imageModel = "PhotoImage"

# Class GWindow

class GWindow(object):
    """
    This class represents a graphics window that can contain graphical
    objects.
    """

# Public constants

    DEFAULT_WIDTH = 500
    DEFAULT_HEIGHT = 300

# Constructor: GWindow

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        """
        The constructor takes either of the following forms:

        <pre>
           GWindow()
           GWindow(width, height)
        </pre>

        If the dimensions are missing, the constructor creates a
        <code>GWindow</code> with a default size.
        """
        global _rootWindow
        tk = tkinter._default_root # For compatibility with filechooser.py
        if tk is None:
            tk = tkinter.Tk()
        else:
            tk.deiconify()
        self.windowWidth = width
        self.windowHeight = height
        self.tk = tk
        self.tk.protocol("WM_DELETE_WINDOW", sys.exit)
        self.canvas = tkinter.Canvas(tk, width=width, height=height)
        self.canvas.pack()
        self.canvas.update()
        self.images = { }
        self.base = GCompound()
        self.base.gw = self
        self.eventManager = _EventManager(self)

        self.setWindowTitle(getProgramName())

        _rootWindow = tk
        def eventLoop():
            print("Hello! here")
            tk.mainloop()
        atexit.register(eventLoop)

    def __eq__(self, other):
        if type(other) is GWindow:
            return self.canvas is other.canvas
        return False

# Public method: close

    def close(self):
        """
        Deletes the window from the screen.
        """
        global _rootWindow
        _rootWindow.destroy()

# Public method: requestFocus

    def requestFocus(self):
        """
        Asks the system to assign the keyboard focus to the window, which
        brings it to the top and ensures that key events are delivered to
        the window.  Clicking in the window automatically requests the focus.
        """
        raise Exception("Not yet implemented")

# Public method: clear

    def clear(self):
        """
        Clears the contents of the window.
        """
        self.base.removeAll()

# Public method: getWidth

    def getWidth(self):
        """
        Returns the width of the graphics window in pixels.
        """
        return self.windowWidth

# Public method: getHeight

    def getHeight(self):
        """
        Returns the height of the graphics window in pixels.
        """
        return self.windowHeight

# Public method: addEventListener

    def addEventListener(self, type, fn):
        """
        Adds an event listener of the specified type to the window.
        """
        self.eventManager.addEventListener(type, fn)

# Public method: repaint

    def repaint(self):
        """
        Schedule a repaint on this window.
        """
        pass

# Public method: setWindowTitle

    def setWindowTitle(self, title):
        """
        Sets the title of the graphics window.
        """
        self.windowTitle = title
        self.tk.title(title)

# Public method: getWindowTitle

    def getWindowTitle(self):
        """
        Returns the title of the graphics window.
        """
        return self.windowTitle

# Public method: add

    def add(self, gobj, x=None, y=None):
        """
        Adds the <code>GObject</code> to the window.  The first parameter
        is the object to be added.  The <code>x</code> and <code>y</code>
        parameters are optional.  If they are supplied, the location of
        the object is set to (<code>x</code>, <code>y</code>).
        """
        self.base.add(gobj, x, y)

# Public method: remove

    def remove(self, gobj):
        """
        Removes the object from the window.
        """
        self.base.remove(gobj)

# Public method: getElementAt

    def getElementAt(self, x, y):
        """
        Returns the topmost <code>GObject</code> containing the
        point (x, y), or <code>None</code> if no such object exists.
        """
        return self.base.getElementAt(x, y)

# Public method: createTimer

    def createTimer(self, fn, delay):
        """
        Creates a new timer object that calls fn after the specified
        delay, which is measured in milliseconds.  The timer must be
        started by calling the <code>start</code> method.
        """
        return GTimer(self, fn, delay)

# Public method: setTimeout

    def setTimeout(self, fn, delay):
        """
        Creates and starts a one-shot timer that calls fn after the
        specified delay, which is measured in milliseconds.  The
        setTimeout method returns the <code>GTimer</code> object.
        """
        timer = GTimer(self, fn, delay)
        timer.start()
        return timer

# Private method: _rebuild

    def _rebuild(self):
        """
        Rebuilds the tkinter data structure for the window.  This
        operation is triggered if a global update is necessary.
        """
        self.canvas.delete("all")
        self.base._install(self, _SimpleTransform())

# Class: GObject

class GObject(object):
    """
    This class is the common superclass of all graphical objects that can
    be displayed on a graphical window. For examples illustrating the use
    of the <code>GObject</code> class, see the descriptions of the
    individual subclasses.
    """

# Constructor: GObject

    def __init__(self):
        """
        Creates a new <code>GObject</code>.  The constructor is called
        only by subclasses.
        """
        self.x = 0.0
        self.y = 0.0
        self.color = "Black"
        self.lineWidth = 1.0
        self.visible = True
        self.parent = None
        self.tkid = None
        self.gw = None

# Public method: getX

    def getX(self):
        """
        Returns the x-coordinate of the object.
        """
        return self.x

# Public method: getY

    def getY(self):
        """
        Returns the y-coordinate of the object.
        """
        return self.y

# Public method: getLocation

    def getLocation(self):
        """
        Returns the location of this object as a <code>GPoint</code>.
        """
        return GPoint(self.x, self.y)

# Public method: setLocation

    def setLocation(self, x, y):
        """
        Sets the location of this object to the specified point.
        """
        if type(x) is GPoint:
            x, y = x.getX(), x.getY()
        elif type(x) is dict:
            x, y = x.x, x.y
        self.x = x
        self.y = y
        self._updateLocation()

# Public method: move

    def move(self, dx, dy):
        """
        Moves the object on the screen using the displacements
        <code>dx</code> and <code>dy</code>.
        """
        self.setLocation(self.x + dx, self.y + dy)

# Public method: movePolar

    def movePolar(self, r, theta):
        """
        Moves the object on the screen the distance <i>r</i> in the
        direction <i>theta</i>.
        """
        dx = r * math.cos(math.radians(theta))
        dy = -r * math.sin(math.radians(theta))
        self.move(dx, dy)

# Public method: getWidth

    def getWidth(self):
        """
        Returns the width of this object, which is defined to be the width of
        the bounding box.
        """
        return self.getBounds().getWidth()

# Public method: getHeight

    def getHeight(self):
        """
        Returns the height of this object, which is defined to be the height
        of the bounding box.
        """
        return self.getBounds().getHeight()

# Public method: getSize

    def getSize(self):
        """
        Returns the size of the object as a <code>GDimension</code>.
        """
        bounds = self.getBounds()
        return GDimension(bounds.getWidth(), bounds.getHeight())

# Public method: setLineWidth

    def setLineWidth(self, lineWidth):
        """
        Sets the width of the line used to draw this object.
        """
        self.lineWidth = lineWidth
        self.updateProperties(width=lineWidth)

# Public method: getLineWidth

    def getLineWidth(self):
        """
        Returns the width of the line used to draw this object.
        """
        return self.lineWidth

# Public method: setColour

    def setColour(self, color):
        """
        Alternate spelling for <code>setColor</code>.
        """
        self.setColor(color)

# Public method: setColor

    def setColor(self, color):
        """
        Sets the color used to display this object.  The color parameter is
        usually one of the CSS color names.  The color can also be specified
        as a string in the form <code>"#rrggbb"</code> where <code>rr</code>,
        <code>gg</code>, and <code>bb</code> are pairs of hexadecimal digits
        indicating the red, green, and blue components of the color.
        """
        rgb = convertColorToRGB(color)
        self.color = convertRGBToColor(rgb)
        self.updateColor()

# Public method: getColour

    def getColour(self):
        """
        Alternate spelling for <code>getColor</code>.
        """
        return self.getColor()

# Public method: getColor

    def getColor(self):
        """
        Returns the current color as a string in the form
        <code>"#rrggbb"</code>.  In this string, the values <code>rr</code>,
        <code>gg</code>, and <code>bb</code> are two-digit hexadecimal
        values representing the red, green, and blue components.
        """
        return self.color

# Public method: scale

    def scale(self, sf):
        """
        Scales the object by the specified scale factor.
        """
        raise Exception("Not yet implemented")

# Public method: rotate

    def rotate(self, theta):
        """
        Transforms the object by rotating it theta degrees counterclockwise
        around its origin.
        """
        raise Exception("Not yet implemented")

# Public method: setVisible

    def setVisible(self, flag):
        """
        Sets whether this object is visible.
        """
        self.visible = flag
        raise Exception("Not yet implemented")

# Public method: isVisible

    def isVisible(self):
        """
        Returns true if this object is visible.
        """
        return self.visible

# Public method: sendForward

    def sendForward(self):
        """
        Moves this object one step toward the front in the z dimension.
        If it was already at the front of the stack, nothing happens.
        """
        parent = self.getParent()
        if parent is not None: parent._sendForward(self)

# Public method: sendToFront

    def sendToFront(self):
        """
        Moves this object to the front of the display in the z dimension.
        By moving it to the front, this object will appear to be on top of the
        other graphical objects on the display and may hide any objects that
        are further back.
        """
        parent = self.getParent()
        if parent is not None: parent._sendToFront(self)

# Public method: sendBackward

    def sendBackward(self):
        """
        Moves this object one step toward the back in the z dimension.
        If it was already at the back of the stack, nothing happens.
        """
        parent = self.getParent()
        if parent is not None: parent._sendBackward(self)

# Public method: sendToBack

    def sendToBack(self):
        """
        Moves this object to the back of the display in the z dimension.
        By moving it to the back, this object will appear to be behind
        the other graphical objects on the display and may be obscured
        by other objects in front.
        """
        parent = self.getParent()
        if parent is not None: parent._sendToBack(self)

# Public method: contains

    def contains(self, x, y):
        """
        Returns true if the specified point is inside the object.
        """
        if type(x) is GPoint:
            x, y = x.getX(), x.getY()
        elif type(x) is dict:
            x, y = x.x, x.y
        bounds = self.getBounds()
        if bounds is None: return False
        return bounds.contains(x, y)

# Public method: getParent

    def getParent(self):
        """
        Returns a pointer to the <code>GCompound</code> that contains this
        object.  Every <code>GWindow</code> is initialized to contain a
        single <code>GCompound</code> that is aligned with the window.
        Adding objects to the window adds them to that <code>GCompound</code>,
        which means that every object you add to the window has a parent.
        Calling <code>getParent</code> on the top-level <code>GCompound</code>
        returns <code>None</code>.
        """
        return self.parent

# Abstract method: getType

    def getType(self):
        """
        Returns the concrete type of the object as a string, as in
        "GOval" or "GRect".
        """
        raise Exception("getType is not defined in the GObject class")

# Abstract method: getBounds

    def getBounds(self):
        """
        Returns the bounding box of this object, which is defined to be the
        smallest rectangle that covers everything drawn by the figure.  The
        coordinates of this rectangle do not necessarily match the location
        returned by <code>getLocation</code>.  Given a <code>GLabel</code>
        object, for example, <code>getLocation</code> returns the
        coordinates of the point on the baseline at which the string begins.
        The <code>getBounds</code> method, by contrast, returns a rectangle
        that covers the entire window area occupied by the string.
        """
        raise Exception("getBounds is not defined in the GObject class")

# Private method: updateProperties

    def updateProperties(self, **options):
        """
        Updates the specified properties of the object, if it is installed
        in a window.
        """
        gw = self.getWindow()
        if gw is None: return
        tkc = gw.canvas
        tkc.itemconfig(self.tkid, **options)

# Private method: _updateLocation

    def _updateLocation(self):
        """
        Updates the location for this object from the stored x and y
        values.  Some subclasses need to override this method.
        """
        gw = self.getWindow()
        if gw is None: return
        tkc = gw.canvas
        coords = tkc.coords(self.tkid)
        offx = 0
        offy = 0
        gobj = self.getParent()
        while gobj is not None:
           offx += gobj.x
           offy += gobj.y
           gobj = gobj.getParent()
        dx = (self.x + offx) - coords[0]
        dy = (self.y + offy) - coords[1]
        tkc.move(self.tkid, dx, dy)

# Private method: updateColor

    def updateColor(self):
        """
        Updates the color properties.  Some subclasses need to override
        this method.
        """
        self.updateProperties(fill=self.color)

# Private method: getWindow

    def getWindow(self):
        """
        Returns the <code>GWindow</code> in which this <code>GObject</code>
        is installed.  If the object is not installed in a window, this
        method returns <code>None</code>.
        """
        gobj = self
        while (gobj.parent is not None):
            gobj = gobj.parent
        return gobj.gw

# Private abstract method: _install

    def _install(self, target, ctm):
        """
        Installs the object in the target, creating any tkinter objects
        that are necessary.
        """
        raise Exception("_install is not defined in the GObject class")

# Class: GFillableObject

class GFillableObject(GObject):
    """
    This abstract class is the superclass of all objects that are fillable.
    """

# Constructor: GFillableObject

    def __init__(self):
        """
        Initializes a <code>GFillableObject</code>.  Because this is an
        abstract class, clients should not call this constructor explicitly.
        """
        GObject.__init__(self)
        self.fillFlag = False
        self.fillColor = ""

# Public method: setFilled

    def setFilled(self, flag):
        """
        Sets the fill status for the object, where <code>False</code>
        is outlined and <code>True</code> is filled.
        """
        self.fillFlag = flag
        self.updateColor()

# Public method: isFilled

    def isFilled(self):
        """
        Returns <code>True</code> if the object is filled.
        """
        return self.fillFlag

# Public method: setFillColor

    def setFillColor(self, color):
        """
        Sets the color used to display the filled region of the object.
        """
        rgb = convertColorToRGB(color)
        self.fillColor = convertRGBToColor(rgb)
        self.updateColor()

# Public method: getFillColor

    def getFillColor(self):
        """
        Returns the color used to display the filled region of this
        object.  If no fill color has been set, <code>getFillColor</code>
        returns the empty string.
        """
        return self.fillColor

# Override method: updateColor

    def updateColor(self):
        """
        Updates the color properties for a <code>GFillableObject</code>.
        """
        outline = self.color
        if self.fillFlag:
            fill = self.fillColor
            if fill is None or fill == "":
                fill = outline
        else:
            fill = ""
        self.updateProperties(outline=outline, fill=fill)

# Class: GRect

class GRect(GFillableObject):
    """
    This class represents a graphical object whose appearance consists of
    a rectangular box.
    """

# Constructor: GRect

    def __init__(self, a1, a2, a3=None, a4=None):
        """
        The <code>GRect</code> constructor takes either of the following
        forms:

        <pre>
           GRect(width, height)
           GRect(x, y, width, height)
        </pre>

        If the <code>x</code> and <code>y</code> parameters are missing,
        the origin is set to (0, 0).
        """
        GFillableObject.__init__(self)
        if a3 is None:
            x = 0
            y = 0
            width = a1
            height = a2
        else:
            x = a1
            y = a2
            width = a3
            height = a4
        self.width = width
        self.height = height
        self.setLocation(x, y)

# Public method: setSize

    def setSize(self, width, height=None):
        """
        Changes the size of this rectangle as specified.
        """
        if type(width) is GDimension:
            width, height = width.getWidth(), width.getHeight()
        self.width = width
        self.height = height
        gw = self.getWindow()
        if gw is None: return
        tkc = gw.canvas
        coords = tkc.coords(self.tkid)
        tkc.coords(self.tkid, coords[0], coords[1],
                              coords[0] + width, coords[1] + height)

# Public method: setBounds

    def setBounds(self, x, y=None, width=None, height=None):
        """
        Changes the bounds of this rectangle to the specified values.
        """
        if type(x) is GRectangle:
            width, height = x.getWidth(), x.getHeight()
            x, y = x.getX(), x.getY()
        self.setLocation(x, y)
        self.setSize(width, height)

# Override method: getBounds

    def getBounds(self):
        """
        Returns the bounds of this <code>GRect</code>.
        """
        return GRectangle(self.x, self.y, self.width, self.height)

# Override method: getType

    def getType(self):
        """
        Returns the type of this object.
        """
        return "GRect"

# Override method: _install

    def _install(self, target, ctm):
        """
        Installs the <code>GRect</code> in the canvas.
        """
        gw = target
        tkc = gw.canvas
        pt = ctm.transform(GPoint(self.getX(), self.getY()))
        x = pt.getX()
        y = pt.getY()
        self.tkid = tkc.create_rectangle(x, y,
                                         x + self.width, y + self.height,
                                         width=self.lineWidth)
        self.updateColor()

# Override method: __str__

    def __str__(self):
        return ("GRect(" + str(self.x) + ", " + str(self.y) + ", " +
                str(self.width) + ", " + str(self.height) + ")")

# Class: GOval

class GOval(GFillableObject):
    """
    This graphical object subclass represents an oval inscribed in
    a rectangular box.
    """

# Constructor: GOval

    def __init__(self, a1, a2, a3=None, a4=None):
        """
        The <code>GOval</code> constructor takes either of the following
        forms:

        <pre>
           GOval(width, height)
           GOval(x, y, width, height)
        </pre>

        If the <code>x</code> and <code>y</code> parameters are missing,
        the origin is set to (0, 0).
        """
        GFillableObject.__init__(self)
        if a3 is None:
            x = 0
            y = 0
            width = a1
            height = a2
        else:
            x = a1
            y = a2
            width = a3
            height = a4
        self.width = width
        self.height = height
        self.setLocation(x, y)

# Public method: setSize

    def setSize(self, width, height=None):
        """
        Changes the size of this oval as specified.
        """
        if type(width) is GDimension:
            width, height = width.getWidth(), width.getHeight()
        self.width = width
        self.height = height
        gw = self.getWindow()
        if gw is None: return
        tkc = gw.canvas
        coords = tkc.coords(self.tkid)
        tkc.coords(self.tkid, coords[0], coords[1],
                              coords[0] + width, coords[1] + height)

# Public method: setBounds

    def setBounds(self, x, y=None, width=None, height=None):
        """
        Changes the bounds of this rectangle to the specified values.
        """
        if type(x) is GRectangle:
            width, height = x.getWidth(), x.getHeight()
            x, y = x.getX(), x.getY()
        self.setLocation(x, y)
        self.setSize(width, height)

# Override method: getBounds

    def getBounds(self):
        """
        Returns the bounds of this <code>GOval</code>.
        """
        return GRectangle(self.x, self.y, self.width, self.height)

# Override method: contains

    def contains(self, x, y):
      rx = self.width / 2
      ry = self.height / 2
      tx = x - (self.x + rx)
      ty = y - (self.y + ry)
      return (tx * tx) / (rx * rx) + (ty * ty) / (ry * ry) <= 1.0

# Override method: getType

    def getType(self):
        """
        Returns the type of this object.
        """
        return "GOval"

# Override method: _install

    def _install(self, target, ctm):
        """
        Installs the <code>GOval</code> in the canvas.
        """
        gw = target
        tkc = gw.canvas
        pt = ctm.transform(GPoint(self.x, self.y))
        x = pt.getX()
        y = pt.getY()
        self.tkid = tkc.create_oval(x, y,
                                    x + self.width, y + self.height,
                                    width=self.lineWidth)

        self.updateColor()

# Override method: __str__

    def __str__(self):
        return ("GOval(" + str(self.x) + ", " + str(self.y) + ", " +
                str(self.width) + ", " + str(self.height) + ")")

# Class: GCompound

class GCompound(GObject):
    """
    This graphical object subclass consists of a collection of other
    graphical objects.  Once assembled, the internal objects can be
    manipulated as a unit.  The <code>GCompound</code> keeps track
    of its own position, and all items within it are drawn relative
    to that location.
    """

# Constructor: GCompound

    def __init__(self):
        """
        Creates a <code>GCompound</code> with no internal components.
        """
        GObject.__init__(self)
        self.contents = [ ]

# Public method: add

    def add(self, gobj, x=None, y=None):
        """
        Adds a new graphical object to the <code>GCompound</code>.  The
        first parameter is the object to be added.  The <code>x</code>
        and <code>y</code> parameters are optional.  If they are supplied,
        the location of the object is set to (<code>x</code>, <code>y</code>).
        """
        if x is not None:
            gobj.setLocation(x, y)
        self.contents.append(gobj)
        gobj.parent = self
        if self.gw is None:
            gw = self.getWindow()
            if gw is not None:
                gw._rebuild()
        else:
            gobj._install(self.gw, _SimpleTransform())


# Public method: remove

    def remove(self, gobj):
        """
        Removes the specified object from the <code>GCompound</code>.
        """
        index = self.findGObject(gobj)
        if index != -1: self.removeAt(index)
        gw = self.getWindow()
        if gw is not None:
            gw._rebuild()

# Public method: removeAll

    def removeAll(self):
        """
        Removes all graphical objects from the <code>GCompound</code>.
        """
        while (len(self.contents) > 0):
            self.removeAt(0)
        gw = self.getWindow()
        if gw is not None:
            gw._rebuild()

# Public method: getElementAt

    def getElementAt(self, x, y):
        """
        Returns the topmost <code>GObject</code> containing the
        point (x, y), or <code>None</code> if no such object exists.
        Coordinates are interpreted relative to the reference point.
        """
        for gobj in reversed(self.contents):
            if gobj.contains(x, y):
                return gobj
        return None

# Public method: getElementCount

    def getElementCount(self):
        """
        Returns the number of graphical objects stored in the
        <code>GCompound</code>.
        """
        return len(self.contents)

# Public method: getElement

    def getElement(self, index):
        """
        Returns the graphical object at the specified index, numbering
        from back to front in the the <i>z</i> dimension.
        """
        return self.contents[index]

# Override method: getBounds

    def getBounds(self):
        """
        Returns a bounding rectangle for this compound.
        """
        x0 = self.getX()
        y0 = self.getY()
        if len(self.contents) == 0:
            return GRectangle(x0, y0, 0, 0)
        xMin = sys.float_info.max
        yMin = sys.float_info.max
        xMax = sys.float_info.min
        yMax = sys.float_info.min
        for gobj in self.contents:
            bounds = gobj.getBounds()
            xMin = min(xMin, x0 + bounds.getX())
            yMin = min(yMin, y0 + bounds.getY())
            xMax = max(xMax, x0 + bounds.getX())
            yMax = max(yMax, y0 + bounds.getY())
            xMin = min(xMin, x0 + bounds.getX() + bounds.getWidth())
            yMin = min(yMin, y0 + bounds.getY() + bounds.getHeight())
            xMax = max(xMax, x0 + bounds.getX() + bounds.getWidth())
            yMax = max(yMax, y0 + bounds.getY() + bounds.getHeight())
        return GRectangle(xMin, yMin, xMax - xMin, yMax - yMin)

# Public method: contains

    def contains(self, x, y):
        """
        Returns true if the specified point is inside the object.
        """
        refpt = self.getLocation()
        tx = x - refpt.getX()
        ty = y - refpt.getY()
        for gobj in self.contents:
            if gobj.contains(tx, ty): return True
        return False

# Override method: getType

    def getType(self):
        """
        Returns the type of this object
        """
        return "GCompound"

# Public method: __str__

    def __str__(self):
        return "GCompound(...)"

# Override method: _updateLocation

    def _updateLocation(self):
        """
        Updates the location for this <code>GCompound</code> by
        rebuilding the entire window if the component is installed.
        """
        gw = self.getWindow()
        if gw is not None:
            gw._rebuild()

# Override method: _install

    def _install(self, target, ctm):
        pt = ctm.transform(GPoint(self.getX(), self.getY()))
        ctm2 = _SimpleTransform(pt.getX(), pt.getY())
        for gobj in self.contents:
            gobj._install(target, ctm2)

# Internal method: _sendForward

    def _sendForward(self, gobj):
        index = self.findGObject(gobj)
        if index == -1: return
        if index != len(self.contents)-1:
            self.contents.pop(index)
            self.contents.insert(index + 1, gobj)
            gw = self.getWindow()
            if gw is not None:
                gw._rebuild()

# Internal method: _sendToFront

    def _sendToFront(self, gobj):
        index = self.findGObject(gobj)
        if index == -1: return
        if index != len(self.contents)-1:
            self.contents.pop(index)
            self.contents.append(gobj)
            gw = self.getWindow()
            if gw is not None:
                gw._rebuild()

# Internal method: _sendBackward

    def _sendBackward(self, gobj):
        index = self.findGObject(gobj)
        if index == -1: return
        if index != 0:
            self.contents.pop(index)
            self.contents.insert(index - 1, gobj)
            gw = self.getWindow()
            if gw is not None:
                gw._rebuild()

# Internal method: _sendToBack

    def _sendToBack(self, gobj):
        index = self.findGObject(gobj)
        if index == -1: return
        if index != 0:
            self.contents.pop(index)
            self.contents.insert(0, gobj)
            gw = self.getWindow()
            if gw is not None:
                gw._rebuild()

# Internal method: findGObject

    def findGObject(self, gobj):
        n = len(self.contents)
        for i in range(n):
            if self.contents[i] == gobj: return i
        return -1

# Internal method: removeAt

    def removeAt(self, index):
        gobj = self.contents[index]
        self.contents.pop(index)
        gobj.parent = None

# Class: GRoundRect

class GRoundRect(GRect):
    """
    This class represents a graphical object whose appearance consists
    of a rectangular box with rounded corners.
    """

# Constructor: GRoundRect

    def __init__(self, a1, a2, a3=None, a4=None, a5=None):
        """
        The <code>GRoundRect</code> constructor takes any of the following
        forms:

        <pre>
           GRoundRect(width, height)
           GRoundRect(x, y, width, height)
           GRoundRect(width, height, corner)
           GRoundRect(x, y, width, height, corner)
        </pre>

        If the <code>x</code> and <code>y</code> parameters are missing,
        the origin is set to (0, 0).  If <code>corner</code> is missing,
        the constructor substitutes a default value.
        """
        raise Exception("Not yet implemented")
        if a3 is None:
            x = 0
            y = 0
            width = a1
            height = a2
            corner = a3
        else:
            x = a1
            y = a2
            width = a3
            height = a4
            corner = a5
        GRect.__init__(self, width, height)
        self.corner = corner
        Platform().createGRoundRect(self, width, height, corner)
        self.setLocation(x, y)

# Override method: getType

    def getType(self):
        """
        Returns the type of this object.
        """
        return "GRoundRect"

# Public method: __str__

    def __str__(self):
        return ("GRoundRect(" + str(self.x) + ", " + str(self.y) + ", " +
                str(self.width) + ", " + str(self.height) + ", " +
                str(self.corner) + ")")

# Class: G3DRect

class G3DRect(GRect):
    """
    This graphical object subclass represents a rectangular box that can
    be raised or lowered.
    """

# Constructor: G3DRect

    def __init__(self, a1, a2, a3=None, a4=None, a5=None):
        """
        The <code>G3DRect</code> constructor takes any of the following
        forms:

        <pre>
           G3DRect(width, height)
           G3DRect(x, y, width, height)
           G3DRect(width, height, raised)
           G3DRect(x, y, width, height, raised)
        </pre>

        If the <code>x</code> and <code>y</code> parameters are missing,
        the origin is set to (0, 0).  If <code>raised</code> is missing,
        the constructor assumes that the value is <code>False</code>.
        """
        raise Exception("Not yet implemented")
        if a3 is None:
            x = 0
            y = 0
            width = a1
            height = a2
            raised = a3
        else:
            x = a1
            y = a2
            width = a3
            height = a4
            raised = a5
        GRect.__init__(self, width, height)

class G3DRect(GRect):
    """
    This graphical object subclass represents a rectangular box that can
    be raised or lowered.
    """

# Constructor: G3DRect

    def __init__(self, width, height, x=0, y=0, raised=False):
        """
        Initializes a new 3D rectangle with the specified width and height.
        If the x and y parameters are specified, they are used to specify
        the origin.  The raised parameter determines whether the rectangle
        should be drawn with highlights that suggest that it is raised about
        the background.
        """
        GRect.__init__(self, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.raised = raised
        self.fillFlag = False
        self.fillColor = ""
        self.setRaised(raised)
        Platform().createG3DRect(self, width, height, str(raised).lower())
        self.setLocation(x, y)

# Public method: setRaised

    def setRaised(self, raised):
        """
        Sets whether this object appears raised.
        """
        self.raised = raised
        Platform().setRaised(self, str(raised).lower())

# Public method: isRaised

    def isRaised(self):
        """
        Returns <code>True</code> if this object appears raised.
        """
        return self.raised

# Override method: getType

    def getType(self):
        """
        Returns the type of this object.
        """
        return "G3DRect"

# Public method: __str__

    def __str__(self):
        return ("G3DRect(" + str(self.x) + ", " + str(self.y) + ", " +
                str(self.width) + ", " + str(self.height) + ", " +
                str(self.raised).lower() + ")")

# Class: GArc

class GArc(GFillableObject):
    """
    This graphical object subclass represents an elliptical arc.  The
    arc is specified by the following parameters::

    <ul>
       <li>The coordinates of the bounding rectangle (x, y, width, height)</li>
       <li>The angle at which the arc starts (start)</li>
       <li>The number of degrees that the arc covers (sweep)</li>
    </ul>

    All angles in a <code>GArc</code> description are measured in
    degrees moving counterclockwise from the +<i>x</i> axis.  Negative
    values for either <code>start</code> or <code>sweep</code> indicate
    motion in a clockwise direction.
    """

# Constructor: GArc

    def __init__(self, a1, a2, a3=None, a4=None, a5=None, a6=None):
        """
        The <code>GArc</code> constructor takes either of the following
        forms:

        <pre>
           GArc(width, height, start, sweep)
           GArc(x, y, width, height, start, sweep)
        </pre>

        If the <code>x</code> and <code>y</code> parameters are missing,
        the origin is set to (0, 0).
        """
        GFillableObject.__init__(self)
        if a5 is None:
            x = 0
            y = 0
            width = a1
            height = a2
            start = a3
            sweep = a4
        else:
            x = a1
            y = a2
            width = a3
            height = a4
            start = a5
            sweep = a6
        self.frameWidth = width
        self.frameHeight = height
        self.start = start
        self.sweep = sweep
        self.setLocation(x, y)

# Public method: setStartAngle

    def setStartAngle(self, start):
        """
        Sets the starting angle for this <code>GArc</code> object.
        """
        self.start = start
        self.updateProperties(start=start)

# Public method: getStartAngle

    def getStartAngle(self):
        """
        Returns the starting angle for this GArc object.
        """
        return self.start

# Public method: setSweepAngle

    def setSweepAngle(self, sweep):
        """
        Sets the sweep angle for this GArc object.
        """
        self.sweep = sweep
        self.updateProperties(extent=sweep)

# Public method: getSweepAngle

    def getSweepAngle(self):
        """
        Returns the sweep angle for this GArc object.
        """
        return self.sweep

# Public method: getStartPoint

    def getStartPoint(self):
        """
        Returns the point at which the arc starts.
        """
        return getArcPoint(self.start)

# Public method: getEndPoint

    def getEndPoint(self):
        """
        Returns the point at which the arc ends.
        """
        return getArcPoint(self.start + self.sweep)

# Public method: setFrameRectangle

    def setFrameRectangle(self, x, y=None, width=None, height=None):
        """
        Changes the boundaries of the rectangle used to frame the arc.
        """
        if type(x) is GRectangle:
            width, height = x.getWidth(), x.getHeight()
            x, y = x.getX(), x.getY()
        self.setLocation(x, y)
        gw = self.getWindow()
        if gw is None: return
        tkc = gw.canvas
        coords = tkc.coords(self.tkid)
        tkc.coords(self.tkid, coords[0], coords[1],
                              coords[0] + width, coords[1] + height)

# Public method: getFrameRectangle

    def getFrameRectangle(self):
        """
        Returns the boundaries of the rectangle used to frame the arc.
        """
        return GRectangle(self.x, self.y, self.frameWidth, self.frameHeight)

# Override method: setFilled

    def setFilled(self, flag):
        """
        Sets the fill status for the arc, where <code>False</code> is
        outlined and <code>True</code> is filled.  If a <code>GArc</code>
        is unfilled, the figure consists only of the arc itself.  If a
        <code>GArc</code> is filled, the figure consists of the
        pie-shaped wedge formed by connecting the endpoints of the arc to
        the center.
        """
        GFillableObject.setFilled(self, flag)
        style = tkinter.ARC
        if flag:
            style = tkinter.PIESLICE
        self.updateProperties(style=style)

# Public method: getBounds

    def getBounds(self):
        """
        Gets the bounding rectangle for this object
        """
        rx = self.frameWidth / 2
        ry = self.frameHeight / 2
        cx = self.x + rx
        cy = self.y + ry
        startRadians = self.start * math.pi / 180
        sweepRadians = self.sweep * math.pi / 180
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
        if self.isFilled():
            xMin = min(xMin, cx)
            yMin = min(yMin, cy)
            xMax = max(xMax, cx)
            yMax = max(yMax, cy)
        return GRectangle(xMin, yMin, xMax - xMin, yMax - yMin)

# Public method: contains

    def contains(self, x, y):
        """
        Returns true if the specified point is inside the object.
        """
        rx = self.frameWidth / 2
        ry = self.frameHeight / 2
        if rx == 0 or ry == 0: return False
        dx = x - (self.x + rx)
        dy = y - (self.y + ry)
        r = (dx * dx) / (rx * rx) + (dy * dy) / (ry * ry)
        if self.fillFlag:
            if r > 1.0: return False
        else:
            t = ARC_TOLERANCE / ((rx + ry) / 2) #!!
            if abs(1.0 - r) > t: return False
        return self.containsAngle(math.atan2(-dy, dx) * 180 / math.pi)

# Override method: getType

    def getType(self):
        """
        Returns the type of this object
        """
        return "GArc"

# Public method: __str__

    def __str__(self):
        return ("GArc(" + str(self.x) + ", " + str(self.y) + ", " +
                str(self.frameWidth) + ", " + str(self.frameHeight) + ", " +
                str(self.start) + ", " + str(self.sweep) + ")")

# Override method: _install

    def _install(self, target, ctm):
        """
        Installs the <code>GArc</code> in the canvas.
        """
        gw = target
        tkc = gw.canvas
        pt = ctm.transform(GPoint(self.getX(), self.getY()))
        x = pt.getX()
        y = pt.getY()
        style = tkinter.ARC
        if self.isFilled():
            style = tkinter.PIESLICE
        self.tkid = tkc.create_arc(x, y,
                                   x + self.frameWidth, y + self.frameHeight,
                                   start=self.start, extent=self.sweep,
                                   width=self.lineWidth, style=style)
        self.updateColor()

# Private method: getArcPoint

    def getArcPoint(self, theta):
        rx = self.frameWidth / 2
        ry = self.frameHeight / 2
        cx = self.x + rx
        cy = self.y + ry
        radians = theta * math.pi / 180
        return GPoint(cx + rx * math.cos(radians), cy - ry * math.sin(radians))

# Private method: containsAngle

    def containsAngle(self, theta):
        start = min(self.start, self.start + self.sweep)
        sweep = abs(self.sweep)
        if sweep >= 360: return True
        if theta < 0: theta = 360 - math.fmod(-theta, 360)
        else: theta = math.fmod(theta, 360)
        if start < 0: start = 360 - math.fmod(-start, 360)
        else: start = math.fmod(start, 360)
        if start + sweep > 360:
            return (theta >= start or theta <= start + sweep - 360)
        else:
            return (theta >= start and theta <= start + sweep)

# Class: GLine

class GLine(GObject):
    """
    This graphical object subclass represents a line segment.
    """

# Constructor: GLine

    def __init__(self, x0, y0, x1, y1):
        """
        Initializes a line segment from its endpoints.  The point
        (<code>x0</code>, <code>y0</code>) defines the start of the
        line and the point (<code>x1</code>, <code>y1</code>) defines
        the end.
        """
        GObject.__init__(self)
        self.x = x0
        self.y = y0
        self.dx = x1 - x0
        self.dy = y1 - y0

# Public method: setStartPoint

    def setStartPoint(self, x, y):
        """
        Sets the initial point to (<code>x</code>, <code>y</code>),
        leaving the end point unchanged.  This method is therefore
        different from <code>setLocation</code>, which moves both
        components of the line segment.
        """
        self.dx += self.x - x
        self.dy += self.y - y
        self.x = x
        self.y = y
        self.updatePoints()

# Public method: getStartPoint

    def getStartPoint(self):
        """
        Returns the point at which the line starts.
        """
        return GPoint(self.x, self.y)

# Public method: setEndPoint

    def setEndPoint(self, x, y):
        """
        Sets the end point in the line to (x, y), leaving the start point
        unchanged.
        """
        self.dx = x - self.x
        self.dy = y - self.y
        self.updatePoints()

# Public method: getEndPoint

    def getEndPoint(self):
        """
        Returns the point at which the line ends.
        """
        return GPoint(self.x + self.dx, self.y + self.dy)

# Overload method: contains

    def contains(self, x, y):
        """
        Returns true if the specified point is inside the object.
        """
        x0 = self.getX()
        y0 = self.getY()
        x1 = x0 + self.dx
        y1 = y0 + self.dy
        tSquared = __LINE_TOLERANCE__ * __LINE_TOLERANCE__
        if dsq(x, y, x0, y0) < tSquared: return True
        if dsq(x, y, x1, y1) < tSquared: return True
        if x < min(x0, x1) - __LINE_TOLERANCE__: return False
        if x > max(x0, x1) + __LINE_TOLERANCE__: return False
        if y < min(y0, y1) - __LINE_TOLERANCE__: return False
        if y > max(y0, y1) + __LINE_TOLERANCE__: return False
        if (x0 - x1) == 0 and (y0 - y1) == 0: return False
        d = dsq(x0, y0, x1, y1)
        u = ((x - x0) * (x1 - x0) + (y - y0) * (y1 - y0)) / d
        return dsq(x, y, x0 + u * (x1 - x0), y0 + u * (y1 - y0)) < tSquared

# Override method: getType

    def getType(self):
        """
        Returns the type of this object
        """
        return "GLine"

# Public method: __str__

    def __str__(self):
        return ("GLine(" + str(self.x) + ", " + str(self.y) + ", " +
                           str(self.x + self.dx) + ", " +
                           str(self.y + self.dy) + ")")

# Override method: getBounds

    def getBounds(self):
        """
        Returns the bounds of this <code>GLine</code>.
        """
        x0 = min(self.x, self.x + self.dx)
        y0 = min(self.y, self.y + self.dy)
        x1 = max(self.x, self.x + self.dx)
        y1 = max(self.y, self.y + self.dy)
        return GRectangle(x0, y0, x1 - x0, y1 - y0)

# Override method: getType

    def getType(self):
        """
        Returns the type of this object.
        """
        return "GLine"

# Override method: _install

    def _install(self, target, ctm):
        """
        Installs the <code>GLine</code> in the canvas.
        """
        gw = target
        tkc = gw.canvas
        pt = ctm.transform(GPoint(self.getX(), self.getY()))
        x = pt.getX()
        y = pt.getY()
        self.tkid = tkc.create_line(x, y, x + self.dx, y + self.dy,
                                    width=self.getLineWidth(),
                                    fill=self.color)

# Private method: updatePoints

    def updatePoints(self):
        """
        Updates the points in the <code>GLine</code>.
        """
        gw = self.getWindow()
        if gw is None: return
        tkc = gw.canvas
        tkc.coords(self.tkid, self.x, self.y,
                              self.x + self.dx, self.y + self.dy)

# Class: GImage

class GImage(GObject):
    """
    This graphical object subclass represents an image from a file.
    """

    def __init__(self, source, x=0, y=0):
        """
        Initializes a new image by loading the image from the specified
        source, which is either the name of a file in the current directory
        or a two-dimensional array of pixels.
        """
        GObject.__init__(self)
        self.source = source
        self.imageModel = _imageModel
        if _imageModel == "PIL":
            if type(source) is str:
                self.image = Image.open(source)
                self.image.load();
            else:
                width = len(source[0])
                height = len(source)
                ba = bytearray(4 * width * height)
                for i in range(height):
                    for j in range(width):
                        argb = source[i][j]
                        base = 4 * (i * width + j)
                        ba[base] = (argb >> 16) & 0xFF
                        ba[base + 1] = (argb >> 8) & 0xFF
                        ba[base + 2] = argb & 0xFF
                        ba[base + 3] = (argb >> 24) & 0xFF
                self.image = Image.frombytes("RGBA", (width,height), bytes(ba))
            self.photo = ImageTk.PhotoImage(self.image)
        else:
            if type(source) is str:
                self.photo = tkinter.PhotoImage(file=source)
            else:
                raise ImportError("getPixelArray requires the Pillow library")
        self.setLocation(x, y)
        self.sf = 1

# Public method: getBounds

    def getBounds(self):
        """
        Returns the bounding rectangle for this object
        """
        photo = self.photo
        return GRectangle(self.x, self.y, photo.width(), photo.height())

# Public method: getPixelArray

    def getPixelArray(self):
        """
        Returns a two-dimensional array of integers containing the pixel data.
        """
        if self.imageModel == "PIL":
            image = self.image;
            width = image.width;
            height = image.height;
        else:
            width = self.photo.width();
            height = self.photo.height();
        pixels = height * [ [ 0 ] ]
        for y in range(height):
            pixels[y] = width * [ 0 ]
        if self.imageModel == "PIL":
            data = image.convert("RGBA").getdata()
            i = 0;
            for i in range(height):
                for j in range(width):
                    rgba = data[i * width + j]
                    p = rgba[3] << 24 | rgba[0] << 16 | rgba[1] << 8 | rgba[2]
                    pixels[i][j] = p
        return pixels

# Override method: scale

    def scale(self, sf):
        """
        Scales the GImage by the specified scale factor.
        """
        if self.imageModel != "PIL":
           raise Exception("Image scaling is available only if PIL is loaded")
        self.sf *= sf
        gw = self.getWindow()
        if gw is not None:
            gw._rebuild()


# Override method: getType

    def getType(self):
        """
        Returns the type of this object.
        """
        return "GImage"

# Override method: _install

    def _install(self, target, ctm):
        """
        Installs the <code>GImage</code> in the canvas.
        """
        gw = target
        tkc = gw.canvas
        pt = ctm.transform(GPoint(self.getX(), self.getY()))
        x = pt.getX()
        y = pt.getY()
        if self.sf != 1:
            w = round(self.image.width * self.sf)
            h = round(self.image.height * self.sf)
            img = self.image.resize((w, h), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(img)
        self.tkid = tkc.create_image(x, y,
                                     anchor=tkinter.NW,
                                     image=self.photo)

# Static method: getRed

    @staticmethod
    def getRed(pixel):
        """
        Returns the red component of the pixel.
        """
        return pixel >> 16 & 0xFF

# Static method: getGreen

    @staticmethod
    def getGreen(pixel):
        """
        Returns the green component of the pixel.
        """
        return pixel >> 8 & 0xFF

# Static method: getBlue

    @staticmethod
    def getBlue(pixel):
        """
        Returns the blue component of the pixel.
        """
        return pixel & 0xFF

# Static method: getAlpha

    @staticmethod
    def getAlpha(pixel):
        """
        Returns the alpha component of the pixel.
        """
        return pixel >> 24 & 0xFF

# Static method: createRGBPixel

    @staticmethod
    def createRGBPixel(a1=None, a2=None, a3=None, a4=None, **kw):
        """
        Creates an RGB pixel from the arguments.  The kw dictionary allows
        clients to name these parameters to override the conventional order.
        """
        if a4 is None:
            a = 0xFF
            r = a1
            g = a2
            b = a3
        else:
            a = a1
            r = a2
            g = a3
            b = a4
        if "alpha" in kw:
            a = kw["alpha"]
        if "red" in kw:
            r = kw["red"]
        if "green" in kw:
            g = kw["green"]
        if "blue" in kw:
            b = kw["blue"]
        return a << 24 | (r & 0xFF) << 16 | (g & 0xFF) << 8 | (b & 0xFF)

# Public method: __str__

    def __str__(self):
        if type(self.source) is str:
            return "GImage(\"" + self.source + "\")"
        else:
            return "GImage(<data>)"

# Class: GLabel

class GLabel(GObject):
    """
    This graphical object subclass represents a text string.
    """

# Constants

    DEFAULT_FONT = "13pt 'Helvetica Neue','Helvetica','Arial','Sans-Serif'"

# Constructor: GLabel

    def __init__(self, text, x=0, y=0):
        """
        Initializes a <code>GLabel</code> object containing the specified
        string.  By default, the baseline of the first character appears
        at the origin.
        """
        GObject.__init__(self)
        self.text = text
        self.font = self.DEFAULT_FONT
        self.tkFont = decodeFont(self.font)
        self.setLocation(x, y)

# Public method: setFont

    def setFont(self, font):
        """
        Changes the font used to display the GLabel as specified by
        <code>font</code>, which has the form <code>family-style-size</code>,
        where both <code>style</code> and <code>size</code> are optional.
        """
        self.font = font
        self.tkFont = decodeFont(self.font)
        self.updateProperties(font=self.tkFont)
        self._updateLocation()

# Public method: getFont

    def getFont(self):
        """
        Returns the current font for the GLabel.
        """
        return self.font

# Public method: setLabel

    def setLabel(self, text):
        """
        Changes the string stored within the GLabel object, so that
        a new text string appears on the display.
        """
        self.text = text
        self.updateProperties(text=text)

# Public method: getLabel

    def getLabel(self):
        """
        Returns the string displayed by this object.
        """
        return self.text

# Public method: getAscent

    def getAscent(self):
        """
        Returns the maximum distance strings in this font extend above
        the baseline.
        """
        return self.tkFont.metrics("ascent")

# Public method: getDescent

    def getDescent(self):
        """
        Returns the maximum distance strings in this font descend below
        the baseline.
        """
        return self.tkFont.metrics("descent")

# Override method: getWidth

    def getWidth(self):
        """
        Returns the width for this <code>GLabel</code>.
        """
        return self.tkFont.measure(self.text)

# Override method: getHeight

    def getHeight(self):
        """
        Returns the height for this <code>GLabel</code>.
        """
        return self.tkFont.metrics("linespace")

# Override method: getBounds

    def getBounds(self):
        """
        Returns the bounding rectangle for this object.
        """
        return GRectangle(self.x, self.y - self.getAscent(),
                          self.getWidth(), self.getHeight())

# Override method: getType

    def getType(self):
        """
        Returns the type of this object.
        """
        return "GLabel"

# Override method: _updateLocation

    def _updateLocation(self):
        """
        Updates the location for this <code>GLabel</code> from the stored
        x and y values.  This override is necessary to adjust for the
        baseline.
        """
        gw = self.getWindow()
        if gw is None: return
        tkc = gw.canvas
        coords = tkc.coords(self.tkid)
        offx = 0
        offy = self.getHeight() - self.getAscent()
        gobj = self.getParent()
        while gobj is not None:
           offx += gobj.x
           offy += gobj.y
           gobj = gobj.getParent()
        dx = (self.x + offx) - coords[0]
        dy = (self.y + offy) - coords[1]
        tkc.move(self.tkid, dx, dy)

# Override method: _install

    def _install(self, target, ctm):
        """
        Installs the <code>GLabel</code> in the canvas.
        """
        gw = target
        tkc = gw.canvas
        pt = ctm.transform(GPoint(self.getX(), self.getY()))
        x = pt.getX()
        y = pt.getY()
        baseline = y + self.getHeight() - self.getAscent()
        self.tkid = tkc.create_text(x,
                                    baseline,
                                    text=self.text,
                                    font=self.tkFont,
                                    fill=self.color,
                                    anchor="sw")

# Override method: __str__

    def __str__(self):
        return "GLabel(\"" + self.str + "\")"

# Class: GPolygon

class GPolygon(GFillableObject):
    """
    This graphical object subclass represents a polygon bounded by line
    segments.  The <code>GPolygon</code> constructor creates an empty
    polygon.  To complete the figure, you need to add vertices to the
    polygon using some combination of the methods <code>addVertex</code>,
    <code>addEdge</code>, and <code>addPolarEdge</code>.
    """

# Constructor: GPolygon

    def __init__(self):
        """
        Initializes a new empty polygon at the origin.
        """
        GFillableObject.__init__(self)
        self.cx = None
        self.cy = None
        self.vertices = [ ]

# Public method: addVertex

    def addVertex(self, x, y):
        """
        Adds a vertex at (<code>x</code>, <code>y</code>) relative to the
        polygon origin.
        """
        self.cx = x
        self.cy = y
        self.vertices.append(GPoint(x, y))

# Public method: addEdge

    def addEdge(self, dx, dy):
        """
        Adds an edge to the polygon whose components are given by the
        displacements <code>dx</code> and <code>dy</code> from the
        last vertex.
        """
        self.addVertex(self.cx + dx, self.cy + dy)

# Public method: addPolarEdge

    def addPolarEdge(self, r, theta):
        """
        Adds an edge to the polygon specified in polar coordinates.  The
        length of the edge is given by <code>r</code>, and the edge extends
        in direction <code>theta</code>, measured in degrees counterclockwise
        from the +<i>x</i> axis.
        """
        self.addEdge(r * math.cos(theta * math.pi / 180),
                     -r * math.sin(theta * math.pi / 180))

# Public method: getVertices

    def getVertices(self):
        """
        Returns a list of the points in the polygon.
        """
        return self.vertices

# Public method: getBounds

    def getBounds(self):
        """
        Returns the bounding rectangle for this object.
        """
        xMin = 0
        yMin = 0
        xMax = 0
        yMax = 0
        for i in range(len(self.vertices)):
            x = self.vertices[i].getX()
            y = self.vertices[i].getY()
            if i == 0 or x < xMin: xMin = x
            if i == 0 or y < yMin: yMin = y
            if i == 0 or x > xMax: xMax = x
            if i == 0 or y > yMax: yMax = y
        x0 = self.getX()
        y0 = self.getY()
        return GRectangle(x0 + xMin, y0 + yMin, xMax - xMin, yMax - yMin)

# Public method: contains

    def contains(self, x, y):
        """
        Returns true if the specified point is inside the object.
        """
        tx = x - self.getX()
        ty = y - self.getY()
        crossings = 0
        n = len(self.vertices)
        if n < 2: return False
        if self.vertices[0] == self.vertices[n - 1]: n = n - 1
        x0 = self.vertices[0].getX()
        y0 = self.vertices[0].getY()
        for i in range(1, n + 1):
            x1 = self.vertices[i % n].getX()
            y1 = self.vertices[i % n].getY()
            if ((y0 > ty) != (y1 > ty) and
                        tx - x0 < (x1 - x0) * (ty - y0) / (y1 - y0)):
                crossings = crossings + 1
            x0 = x1
            y0 = y1
        return (crossings % 2 == 1)

# Override method: getType

    def getType(self):
        """
        Returns the type of this object.
        """
        return "GPolygon"

# Public method: __str__

    def __str__(self):
        return "GPolygon(" + str(len(self.vertices)) + " vertices)"

# Override method: _updateLocation

    def _updateLocation(self):
        """
        Updates the location for this object from the stored x and y
        values.  Some subclasses need to override this method.
        """
        gw = self.getWindow()
        if gw is None: return
        tkc = gw.canvas
        coords = tkc.coords(self.tkid)
        dx = self.x - coords[0]
        dy = self.y - coords[1]
        tkc.move(self.tkid, dx, dy)

# Override method: _install

    def _install(self, target, ctm):
        """
        Installs the <code>GPolygon</code> in the canvas.
        """
        gw = target
        tkc = gw.canvas
        pt = ctm.transform(GPoint(self.getX(), self.getY()))
        x = pt.getX()
        y = pt.getY()
        coords = [ ]
        for pt in self.vertices:
            coords.append(pt.getX() + x)
            coords.append(pt.getY() + y)
        self.tkid = tkc.create_polygon(*coords, width=self.lineWidth)
        self.updateColor()

# Class: GPoint

class GPoint:
    """
    This class contains real-valued x and y fields. It is used to represent
    a location on the graphics plane.
    """

# Constructor: GPoint

    def __init__(self, x=0, y=0):
        """Initializes a point with the specified coordinates."""
        self._x = x
        self._y = y

# Public method: getX

    def getX(self):
        """Returns the x component of the point."""
        return self._x

# Public method: getY

    def getY(self):
        """Returns the y component of the point."""
        return self._y

# Public method: __str__

    def __str__(self):
        """Returns the string representation of a point."""
        return "(" + str(self._x) + ", " + str(self._y) + ")"

# Public method: __eq__

    def __eq__(self, other):
        """Returns a Boolean indicating whether two points are equal."""
        if type(other) is GPoint:
            return self._x == other._x and self._y == other._y
        return False

# Class: GDimension

class GDimension:
    """
    This class contains real-valued witdth and height fields.  It is
    used to indicate the size of a graphical object.
    """

# Constructor: GDimension

    def __init__(self, width=0.0, height=0.0):
        """
        Initializes a <code>GDimension</code> object with the specified size.
        """
        self._width = width
        self._height = height

# Public method: getWidth

    def getWidth(self):
        """
        Returns the width component of the <code>GDimension</code>.
        """
        return self._width

# Public method: getHeight

    def getHeight(self):
        """
        Returns the height component of the <code>GDimension</code>.
        """
        return self._height

# Public method: __str__

    def __str__(self):
        return "(" + str(self._width) + ", " + str(self._height) + ")"

# Public method: __eq__

    def __eq__(self, other):
        if type(other) is GDimension:
            return self._width == other._width and self._height == other._height
        return False

# Class: GRectangle

class GRectangle:
    """
    This type contains real-valued x, y, width, and height fields. It is
    used to represent the bounding box of a graphical object.
    """

# Constructor: GRectangle

    def __init__(self, x=0.0, y=0.0, width=0.0, height=0.0):
        """
        Initializes a <code>GRectangle</code> object with the specified
        fields.
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height

# Public method: getX

    def getX(self):
        """
        Returns the x component of the upper left corner.
        """
        return self._x

# Public method: getY

    def getY(self):
        """
        Returns the x component of the upper left corner.
        """
        return self._y

# Public method: getWidth

    def getWidth(self):
        """
        Returns the width component of the GRectangle.
        """
        return self._width

# Public method: getHeight

    def getHeight(self):
        """
        Returns the width component of the GRectangle.
        """
        return self._height

# Public method: isEmpty

    def isEmpty(self):
        """
        Returns <code>True</code> if the rectangle is empty.
        """
        return width <= 0 or height <= 0

# Public method: contains

    def contains(self, x, y):
        """
        Returns <code>True</code> if the specified point is inside the
        rectangle.
        """
        if type(x) is GPoint:
            x, y = x.getX(), x.getY()
        elif type(x) is dict:
            x, y = x.x, x.y
        return (x >= self._x and
                y >= self._y and
                x < self._x + self._width and
                y < self._y + self._height)

# Public method: __str__

    def __str__(self):
        return ("(" + str(self._x) + ", " + str(self._y) + ", " +
                      str(self._width) + ", " + str(self._height) + ")")

# Public method: __eq__

    def __eq__(self, other):
        if type(other) is GRectangle:
            return (self._x == other._x and
                    self._y == other._y and
                    self._width == other._width and
                    self._height == other._height)
        return False

# Class: GButton

class GButton(GCompound):

# Constants

    BUTTON_FONT = "14px 'Lucida Grande','Helvetica Neue','Sans-Serif'"
    BUTTON_MARGIN = 10
    BUTTON_MIN_WIDTH = 125
    BUTTON_DEFAULT_HEIGHT = 20
    BUTTON_ASCENT_DELTA = -1

# Constructor: GButton

    def __init__(self, text, fn=None):
        GCompound.__init__(self)
        label = GLabel(text)
        label.setFont(self.BUTTON_FONT)
        width = max(self.BUTTON_MIN_WIDTH,
                    2 * self.BUTTON_MARGIN + label.getWidth())
        frame = GRect(width, self.BUTTON_DEFAULT_HEIGHT)
        frame.setFilled(True)
        frame.setFillColor("White")
        self.add(frame)
        self.add(label)
        self.text = text
        self.label = label
        self.frame = frame
        self.fn = fn
        self._recenter()

# Public method: setSize

    def setSize(self, width, height):
        """
        Sets the dimensions of the button.
        """
        self.frame.setSize(width, height)
        self._recenter()

# Public method: setFont

    def setFont(self, font):
        """
        Sets the font for the button.
        """
        self.label.setFont(font)
        self._recenter()

# Public method: getFont

    def getFont(self):
        """
        Returns the font for the button.
        """
        return self.label.getFont()

# Public method: setLabel

    def setLabel(self, label):
        """
        Sets the label for the button.
        """
        self.label.setLabel(label)
        self._recenter()

# Public method: getLabel

    def getLabel(self):
        """
        Returns the label for the button.
        """
        return self.label.getLabel()

    def __str__(self):
        return "<Button " + self.text + ">"

    def _install(self, target, ctm):
        GCompound._install(self, target, ctm)
        if isinstance(target, GWindow):
            target.addEventListener("click", self._clickAction)

    def _clickAction(self, e):
        if self.contains(e.getX(), e.getY()):
            self.fn()

    def _recenter(self):
        x = (self.frame.getWidth() - self.label.getWidth()) / 2
        y = (self.frame.getHeight() + self.label.getAscent()) / 2
        self.label.setLocation(x, y + self.BUTTON_ASCENT_DELTA)

# Class: GTimer

class GTimer:
    """
    This type implements a timer running in the window.  This class supports
    both one-shot and interval timers.
    """

    def __init__(self, gw, fn, delay):
        self.gw = gw
        self.fn = fn
        self.delay = delay
        self.repeats = False

    def timerTicked(self):
        self.fn()
        if self.repeats:
            tkc = self.gw.canvas
            tkc.after(self.delay, self.timerTicked)

    def setRepeats(self, flag):
        self.repeats = flag

    def start(self):
        tkc = self.gw.canvas
        tkc.after(self.delay, self.timerTicked)

    def stop(self):
        self.repeats = False     #// Reimplement this

# Class: GEvent

class GEvent(object):
    """
    This type is the abstract superclass for all events in the graphics
    package.
    """

# Constructor: GEvent

    def __init__(self):
        """
        Creates a new <code>GEvent</code> object.  This method should
        not be called by clients.
        """

# Public abstract method: getSource
        """
        Returns the source of this event.  Subclasses must override this
        method with an appropriate definition.
        """
        raise Exception("getSource is not defined in the base class")

# Class: GMouseEvent

class GMouseEvent(GEvent):
    """
    This class maintains the data for a mouse event.
    """

# Constructor: GMouseEvent

    def __init__(self, tke):
        """
        Creates a new <code>GMouseEvent</code> from the corresponding
        tkinter event tke.
        """
        self.x = tke.x
        self.y = tke.y

# public method: getX

    def getX(self):
        """
        Returns the x coordinate of the mouse event.
        """
        return self.x

# public method: getY

    def getY(self):
        """
        Returns the y coordinate of the mouse event.
        """
        return self.y

# public method: getY

    def getY(self):
        """
        Returns the y coordinate of the mouse event.
        """
        return self.y

# Override method: getSource

    def getSource():
        """
        Returns the source of the mouse event, which is always the
        root window.
        """
        global rootWindow
        return rootWindow

# Function: pause

def pause(milliseconds):
    """
    Pauses for the indicated number of milliseconds.  This function is
    useful for animation where the motion would otherwise be too fast.
    """
    time.sleep(milliseconds / 1000)

# Function: getScreenWidth

def getScreenWidth():
    """
    Returns the width of the entire display screen.
    """
    return rootWindow.winfo_screenwidth()

# Function: getScreenHeight

def getScreenHeight():
    """
    Returns the height of the entire display screen.
    """
    return rootWindow.winfo_screenheight()

# Function: convertColorToRGB

def convertColorToRGB(colorName):
    """
    Converts a color name into an integer that encodes the
    red, green, and blue components of the color.
    """
    if colorName == "": return -1
    if colorName[0] == "#":
        colorName = "0x" + colorName[1:]
        return int(colorName, 16)
    name = canonicalColorName(colorName)
    if not name in COLOR_TABLE:
        raise Exception("setColor: Illegal color - " + colorName)
    return COLOR_TABLE[name]

# Function: convertRGBToColor

def convertRGBToColor(rgb):
    """
    Converts an rgb value into a name in the form <code>"#rrggbb"</code>.
    Each of the <code>rr</code>, <code>gg</code>, and <code>bb</code>
    values are two-digit hexadecimal numbers indicating the intensity
    of that component.
    """
    hexString = hex(0xFF000000 | rgb)
    return "#" + hexString[4:].upper()

# Function: exitGraphics

def exitGraphics():
    """
    Closes all graphics windows and exits from the application without
    waiting for any additional user interaction.
    """
    sys.exit()

# Function: getProgramName

def getProgramName():
    """
    Returns the name of the program.
    """
    # Patch by sredmond 01-28
    return "Python Program Name"

    # name = None
    # stack = inspect.stack()
    # i = len(stack) - 1
    # while (i >= 0 and name is None):
    #     if stack[i].filename:
    #         name = stack[i].filename
    #     i = i - 1
    # name = name[name.rfind("/") + 1:]
    # dot = name.find(".")
    # if dot != -1:
    #     name = name[:dot]
    # return name

# Private function: canonicalColorName

def canonicalColorName(str):
    result = ""
    for char in str:
        if not char.isspace() and char != "_": result += char.lower()
    return result

# Private function: dsq

def dsq(x0, y0, x1, y1):
    """
    Returns the square of the distance between two points.
    """
    return (x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)

# Function: decodeFont

def decodeFont(name):
    """
    Parses a font string into a tkinter <code>Font</code> object.
    This method accepts a font in either the <code>Font.decode</code>
    used by Java or in the form of a CSS-based style string.
    """
    font = parseJSFont(name)
    if font is None:
        font = parseJavaFont(name)
    return font

def parseJSFont(name):
    """
    Attempts to parse a font specification as a JavaScript font.
    If the parse succeeds, <code>parseJSFont</code> returns the font.
    If the parse fails, <code>parseJSFont</code> returns <code>None</code>.
    """
    name = name.lower().strip()
    family = None
    size = -1
    weight = "normal"
    slant = "roman"
    start = 0
    while (size == -1):
        sp = name.find(" ", start)
        if sp == -1:
            return None
        token = name[start:sp]
        start = sp + 1
        if token == "bold":
            weight = "bold"
        elif token == "italic":
            slant = "italic"
        elif token[0].isdigit():
            size = parseJSUnits(token)
            if size == -1:
                return None
        else:
            return None
    families = name[start:].split(",")
    if len(families) == 0:
        return None
    for family in families:
        if family.startswith("'") or family.startswith("\""):
            family = family[1:-1]
        #// Add code to test for existence of font family
        return tkFont.Font(family=family, size=-size,
                           weight=weight, slant=slant)
    return None

def parseJavaFont(name):
    """
    Attempts to parse a font specification as a Java font.
    If the parse succeeds, <code>parseJavaFont</code> returns the font.
    If the parse fails, <code>parseJavaFont</code> returns <code>None</code>.
    """
    components = name.lower().strip().split("-")
    family = components[0]
    weight = "normal"
    slant = "roman"
    if components[1][0].isdigit():
        size = components[1]
    else:
        size = components[2]
        if "bold" in components[1]:
            weight = "bold"
        if "italic" in components[1]:
            slant = "italic"
    return tkFont.Font(family=family, size=-size,
                       weight=weight, slant=slant)

def parseJSUnits(spec):
    ux = len(spec)
    while (ux > 0 and spec[ux - 1] >= "A"):
        ux = ux - 1
    if ux == 0 or ux == len(spec):
        return -1
    value = float(spec[:ux])
    units = spec[ux:]
    if units == "em":
        return round(16 * value)
    elif units == "pt":
        return round(value / 0.75)
    else:
        return round(value)

# Private class: _SimpleTransform

class _SimpleTransform:

    def __init__(self, tx=0.0, ty=0.0, rotation=0.0, sf=1.0):
        self.tx = tx
        self.ty = ty
        self.rotation = rotation
        self.sf = sf

    def getTX(self):
        return self.tx

    def getTY(self):
        return self.ty

    def getRotation(self):
        return self.rotation

    def getSF(self):
        return self.sf

    # Current stub implementation assumes no rotation and scaling

    def transform(self, pt):
        x0 = pt.getX()
        y0 = pt.getY()
        if self.rotation == 0:
            x1 = self.tx + self.sf * x0
            y1 = self.ty + self.sf * y0
        else:
            ct = math.cos(math.radians(self.rotation))
            st = math.sin(math.radians(self.rotation))
            x1 = self.tx + self.sf * (x0 * ct + y0 * st)
            y1 = self.ty + self.sf * (y0 * ct - x0 * st)
        return GPoint(x1, y1)

    def compose(self, transform):
        return _SimpleTransform(self.tx + transform.getTX(),
                                self.ty + transform.getTY())

# Private class: _EventManager

class _EventManager:
    CLICK_MAX_DISTANCE = 2
    CLICK_MAX_DELAY = 0.5
    pressHandler = None
    releaseHandler = None
    motionHandler = None
    dragHandler = None
    clickListeners = [ ]
    dblclickListeners = [ ]
    mousedownListeners = [ ]
    mouseupListeners = [ ]
    mousemoveListeners = [ ]
    dragListeners = [ ]
    downX = None
    downY = None
    downTime = None

    def __init__(self, gw):
        self.gw = gw
        self.downX = -1
        self.downY = -1

    def pressAction(self, tke):
        self.downX = tke.x
        self.downY = tke.y
        self.downTime = time.time()
        e = GMouseEvent(tke)
        for fn in self.mousedownListeners:
            fn(e)

    def releaseAction(self, tke):
        e = GMouseEvent(tke)
        for fn in self.mouseupListeners:
            fn(e)
        if (abs(self.downX - e.x) <= self.CLICK_MAX_DISTANCE and
                  abs(self.downY - e.y) <= self.CLICK_MAX_DISTANCE and
                  time.time() - self.downTime < self.CLICK_MAX_DELAY):
            for fn in self.clickListeners:
                fn(e)
        #// Implement dblclick

    def motionAction(self, tke):
        e = GMouseEvent(tke)
        for fn in self.mousemoveListeners:
            fn(e)

    def dragAction(self, tke):
        e = GMouseEvent(tke)
        for fn in self.dragListeners:
            fn(e)

    def addEventListener(self, type, fn):
        tkc = self.gw.canvas
        if type == "click":
            if self.pressHandler is None:
                self.pressHandler = self.pressAction
                tkc.bind("<ButtonPress-1>", self.pressHandler)
            if self.releaseHandler is None:
                self.releaseHandler = self.releaseAction
                tkc.bind("<ButtonRelease-1>", self.releaseHandler)
            if fn not in self.clickListeners:
                self.clickListeners.append(fn)
        elif type == "mousedown" or type == "press":
            if self.pressHandler is None:
                self.pressHandler = self.pressAction
                tkc.bind("<ButtonPress-1>", self.pressHandler)
            if fn not in self.mousedownListeners:
                self.mousedownListeners.append(fn)
        elif type == "mouseup" or type == "release":
            if self.releaseHandler is None:
                self.releaseHandler = self.releaseAction
                tkc.bind("<ButtonRelease-1>", self.releaseHandler)
            if fn not in self.mouseupListeners:
                self.mouseupListeners.append(fn)
        elif type == "dblclick":
            if self.pressHandler is None:
                self.pressHandler = self.pressAction
                tkc.bind("<ButtonPress-1>", self.pressHandler)
            if self.releaseHandler is None:
                self.releaseHandler = self.releaseAction
                tkc.bind("<ButtonRelease-1>", self.releaseHandler)
            if fn not in self.dblclickListeners:
                self.dblclickListeners.append(fn)
        elif type == "mousemove" or type == "move":
            if self.motionHandler is None:
                self.motionHandler = self.motionAction
                tkc.bind("<Motion>", self.motionHandler)
            if fn not in self.mousemoveListeners:
                self.mousemoveListeners.append(fn)
        elif type == "drag":
            if self.dragHandler is None:
                self.dragHandler = self.dragAction
                tkc.bind("<B1-Motion>", self.dragHandler)
            if fn not in self.dragListeners:
                self.dragListeners.append(fn)
        else:
            raise Exception("Illegal event type: " + type)

# Constants

__LINE_TOLERANCE__ = 2
__ARC_TOLERANCE__ = 2

# Color table

COLOR_TABLE = {
    "aliceblue" : 0xF0F8FF,
    "antiquewhite" : 0xFAEBD7,
    "aqua" : 0x00FFFF,
    "aquamarine" : 0x7FFFD4,
    "azure" : 0xF0FFFF,
    "beige" : 0xF5F5DC,
    "bisque" : 0xFFE4C4,
    "black" : 0x000000,
    "blanchedalmond" : 0xFFEBCD,
    "blue" : 0x0000FF,
    "blueviolet" : 0x8A2BE2,
    "brown" : 0xA52A2A,
    "burlywood" : 0xDEB887,
    "cadetblue" : 0x5F9EA0,
    "chartreuse" : 0x7FFF00,
    "chocolate" : 0xD2691E,
    "coral" : 0xFF7F50,
    "cornflowerblue" : 0x6495ED,
    "cornsilk" : 0xFFF8DC,
    "crimson" : 0xDC143C,
    "cyan" : 0x00FFFF,
    "darkblue" : 0x00008B,
    "darkcyan" : 0x008B8B,
    "darkgoldenrod" : 0xB8860B,
    "darkgray" : 0xA9A9A9,
    "darkgrey" : 0xA9A9A9,
    "darkgreen" : 0x006400,
    "darkkhaki" : 0xBDB76B,
    "darkmagenta" : 0x8B008B,
    "darkolivegreen" : 0x556B2F,
    "darkorange" : 0xFF8C00,
    "darkorchid" : 0x9932CC,
    "darkred" : 0x8B0000,
    "darksalmon" : 0xE9967A,
    "darkseagreen" : 0x8FBC8F,
    "darkslateblue" : 0x483D8B,
    "darkslategray" : 0x2F4F4F,
    "darkslategrey" : 0x2F4F4F,
    "darkturquoise" : 0x00CED1,
    "darkviolet" : 0x9400D3,
    "deeppink" : 0xFF1493,
    "deepskyblue" : 0x00BFFF,
    "dimgray" : 0x696969,
    "dimgrey" : 0x696969,
    "dodgerblue" : 0x1E90FF,
    "firebrick" : 0xB22222,
    "floralwhite" : 0xFFFAF0,
    "forestgreen" : 0x228B22,
    "fuchsia" : 0xFF00FF,
    "gainsboro" : 0xDCDCDC,
    "ghostwhite" : 0xF8F8FF,
    "gold" : 0xFFD700,
    "goldenrod" : 0xDAA520,
    "gray" : 0x808080,
    "grey" : 0x808080,
    "green" : 0x008000,
    "greenyellow" : 0xADFF2F,
    "honeydew" : 0xF0FFF0,
    "hotpink" : 0xFF69B4,
    "indianred" : 0xCD5C5C,
    "indigo" : 0x4B0082,
    "ivory" : 0xFFFFF0,
    "khaki" : 0xF0E68C,
    "lavender" : 0xE6E6FA,
    "lavenderblush" : 0xFFF0F5,
    "lawngreen" : 0x7CFC00,
    "lemonchiffon" : 0xFFFACD,
    "lightblue" : 0xADD8E6,
    "lightcoral" : 0xF08080,
    "lightcyan" : 0xE0FFFF,
    "lightgoldenrodyellow" : 0xFAFAD2,
    "lightgray" : 0xD3D3D3,
    "lightgrey" : 0xD3D3D3,
    "lightgreen" : 0x90EE90,
    "lightpink" : 0xFFB6C1,
    "lightsalmon" : 0xFFA07A,
    "lightseagreen" : 0x20B2AA,
    "lightskyblue" : 0x87CEFA,
    "lightslategray" : 0x778899,
    "lightslategrey" : 0x778899,
    "lightsteelblue" : 0xB0C4DE,
    "lightyellow" : 0xFFFFE0,
    "lime" : 0x00FF00,
    "limegreen" : 0x32CD32,
    "linen" : 0xFAF0E6,
    "magenta" : 0xFF00FF,
    "maroon" : 0x800000,
    "mediumaquamarine" : 0x66CDAA,
    "mediumblue" : 0x0000CD,
    "mediumorchid" : 0xBA55D3,
    "mediumpurple" : 0x9370DB,
    "mediumseagreen" : 0x3CB371,
    "mediumslateblue" : 0x7B68EE,
    "mediumspringgreen" : 0x00FA9A,
    "mediumturquoise" : 0x48D1CC,
    "mediumvioletred" : 0xC71585,
    "midnightblue" : 0x191970,
    "mintcream" : 0xF5FFFA,
    "mistyrose" : 0xFFE4E1,
    "moccasin" : 0xFFE4B5,
    "navajowhite" : 0xFFDEAD,
    "navy" : 0x000080,
    "oldlace" : 0xFDF5E6,
    "olive" : 0x808000,
    "olivedrab" : 0x6B8E23,
    "orange" : 0xFFA500,
    "orangered" : 0xFF4500,
    "orchid" : 0xDA70D6,
    "palegoldenrod" : 0xEEE8AA,
    "palegreen" : 0x98FB98,
    "paleturquoise" : 0xAFEEEE,
    "palevioletred" : 0xDB7093,
    "papayawhip" : 0xFFEFD5,
    "peachpuff" : 0xFFDAB9,
    "peru" : 0xCD853F,
    "pink" : 0xFFC0CB,
    "plum" : 0xDDA0DD,
    "powderblue" : 0xB0E0E6,
    "purple" : 0x800080,
    "rebeccapurple" : 0x663399,
    "red" : 0xFF0000,
    "rosybrown" : 0xBC8F8F,
    "royalblue" : 0x4169E1,
    "saddlebrown" : 0x8B4513,
    "salmon" : 0xFA8072,
    "sandybrown" : 0xF4A460,
    "seagreen" : 0x2E8B57,
    "seashell" : 0xFFF5EE,
    "sienna" : 0xA0522D,
    "silver" : 0xC0C0C0,
    "skyblue" : 0x87CEEB,
    "slateblue" : 0x6A5ACD,
    "slategray" : 0x708090,
    "slategrey" : 0x708090,
    "snow" : 0xFFFAFA,
    "springgreen" : 0x00FF7F,
    "steelblue" : 0x4682B4,
    "tan" : 0xD2B48C,
    "teal" : 0x008080,
    "thistle" : 0xD8BFD8,
    "tomato" : 0xFF6347,
    "turquoise" : 0x40E0D0,
    "violet" : 0xEE82EE,
    "wheat" : 0xF5DEB3,
    "white" : 0xFFFFFF,
    "whitesmoke" : 0xF5F5F5,
    "yellow" : 0xFFFF00,
    "yellowgreen" : 0x9ACD32,
    "color.black" : 0x000000,
    "color.darkgray" : 0x595959,
    "color.gray" : 0x999999,
    "color.lightgray" : 0xBFBFBF,
    "color.white" : 0xFFFFFF,
    "color.red" : 0xFF0000,
    "color.yellow" : 0xFFFF00,
    "color.green" : 0x00FF00,
    "color.cyan" : 0x00FFFF,
    "color.blue" : 0x0000FF,
    "color.magenta" : 0xFF00FF,
    "color.orange" : 0xFFC800,
    "color.pink" : 0xFFAFAF
}

# Global static variables

_rootWindow = None

# Check for successful compilation

if __name__ == "__main__":
    print("pgl.py compiled successfully")
