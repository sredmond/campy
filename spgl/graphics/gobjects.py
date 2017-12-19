'''
This file exports a hierarchy of graphical shapes based on
the model developed for the ACM Java Graphics.
'''
import spgl.graphics.gtypes as _gtypes
import spgl.graphics.gcolor as _gcolor
import spgl.private.platform as _platform
import spgl.graphics.gmath as _gmath
import math

__ID__ = 0 # ID for next GObject
__LINE_TOLERANCE__ = 1.5 # Default line tolerance
__ARC_TOLERANCE__ = 2.5 # Default arc tolerance
__DEFAULT_CORNER__ = 10 # Default corner rounding
__DEFAULT_GLABEL_FONT__ = "Dialog-13" # Default label font

def dsq(x0, y0, x1, y1):
	'''
	Internal method to find the difference between two points squared
	'''
	return (x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)

# SECTION: Graphical Mixins
class Fillable:
	"""Represents a graphical object that can be filled.

	Adds a _filled attribute to the subclass instance as
	well as a _fill_color.
	"""
	def __init__(self, filled=False, fill_color=''):
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

class GObject:
	'''
	This class is the common superclass of all graphical objects that can
	be displayed on a graphical window. For examples illustrating the use of the GObject class, see
	the descriptions of the individual subclasses.
	'''

	def __init__(self):
		'''
		Initializes a GObject

		@rtype: void
		'''
		global __ID__
		self.x = 0.0
		self.y = 0.0
		self.color = ""
		self.lineWidth = 1.0
		self.transformed = False
		self.visible = True
		self.parent = None
		self.ID = "GObject-" + str(__ID__)
		__ID__ = __ID__ + 1

	def getX(self):
		'''
		Returns the x-coordinate of the object.

		@rtype: float
		'''
		return self.x

	def getY(self):
		'''
		Returns the y-coordinate of the object.

		@rtype: float
		'''
		return self.y

	@property
	def location(self):
		"""Get or set the location of this object as a GPoint."""
		return _gtypes.GPoint(self.x, self.y)

	@location.setter
	def location(self, location):
		x, y = location
		self.x = x
		self.y = y
		_platform.Platform().gobject_set_location(self, x, y)

	def getLocation(self):
		'''
		Returns the location of this object as a GPoint.

		@rtype: GPoint
		'''
		return _gtypes.GPoint(self.x, self.y)

	def setLocation(self, pt=None, x=None, y=None):
		'''
		Sets the location of this object to the specified point.

		@type pt: GPoint
		@type x: float
		@type y: float
		@param pt: new location, will override x and y
		@rtype: void
		'''
		if(pt != None):
			x = pt.getX()
			y = pt.getY()

		if(x == None or y == None): return

		self.x = x
		self.y = y
		_platform.Platform().gobject_set_location(self, x, y)

	def move(self, dx, dy):
		'''
		Moves the object on the screen using the displacements
		dx and dy.

		@type dx: float
		@type dy: float
		@rtype: void
		'''
		self.setLocation(x=self.x + dx, y=self.y + dy)

	def getWidth(self):
		'''
		Returns the width of this object, which is defined to be the width of
		the bounding box.

		@rtype: float
		'''
		bounds = self.getBounds()
		if (bounds != None): return bounds.width
		return None

	def getHeight(self):
		'''`
		Returns the height of this object, which is defined to be the height
		of the bounding box.

		@rtype: float
		'''
		bounds = self.getBounds()
		if (bounds != None): return bounds.height
		return None

	def getSize(self):
		'''
		Returns the size of the object as a GDimension.

		@rtype: GDimension
		'''
		bounds = self.getBounds()
		if(bounds != None): return _gtypes.GDimension(bounds.width, bounds.height)
		return None

	def getBounds(self):
		'''
		Returns the bounding box of this object, which is defined to be the
		smallest rectangle that covers everything drawn by the figure.  The
		coordinates of this rectangle do not necessarily match the location
		returned by getLocation.  Given a GLabel
		object, for example, getLocation returns the coordinates
		of the point on the baseline at which the string begins; the
		getBounds method, by contrast, returns a rectangle that
		covers the entire window area occupied by the string.

		@rtype: GRectangle
		'''
		return None

	def setLineWidth(self, lineWidth):
		'''
		Sets the width of the line used to draw this object.

		@type lineWidth: int
		@rtype: void
		'''
		self.lineWidth = lineWidth
		_platform.Platform().gobject_set_line_width(self, lineWidth)

	def getLineWidth(self):
		'''
		Returns the width of the line used to draw this object.

		@rtype: int
		'''
		return self.lineWidth

	def setColor(self, color=None, rgb=None):
		'''
		Sets the color used to display this object.  The color parameter is
		usually one of the predefined color names:

			- BLACK,
			- BLUE,
			- CYAN,
			- DARK_GRAY,
			- GRAY,
			- GREEN,
			- LIGHT_GRAY,
			- MAGENTA,
			- ORANGE,
			- PINK,
			- RED,
			- WHITE,
			- YELLOW.

		The case of the individual letters in the color name is ignored, as
		are spaces and underscores, so that the color DARK_GRAY
		can be written as "Dark Gray".

		The color can also be specified as a string in the form
		"#rrggbb" where rr, gg, and
		bb are pairs of hexadecimal digits indicating the
		red, green, and blue components of the color.

		@type color: string
		@param color: takes precedence over rgb
		@type rgb: int
		@rtype: void
		'''
		if(color != None):
			rgb = _gcolor.color_to_rgb(color)

		if(rgb == None): return

		self.color = _gcolor.rgb_to_hex(rgb)
		_platform.Platform().gobject_set_color(self, self.color)

	def getColor(self):
		'''
		Returns the current color as a string in the form "#rrggbb".
		In this string, the values rr, gg,
		and bb are two-digit hexadecimal values representing
		the red, green, and blue components of the color, respectively.

		@rtype: string
		'''
		return self.color

	def scale(self, sf=None, sx=None, sy=None):
		'''
		Scales the object by the specified scale factors.  Most clients will use
		the first form, which scales the object by sf in both
		dimensions, so that invoking gobj.scale(2) doubles the
		size of the object.  The second form applies independent scale factors
		to the x and y dimensions.

		@type sf: float
		@type sx: float
		@type sy: float
		@param sf: scale factor, will override sx and sy
		@rtype: void
		'''
		if(sf != None):
			sx = sf
			sy = sf

		if(sx == None or sy == None): return

		self.transformed = True
		_platform.Platform().gobject_scale(self, sx, sy)

	def rotate(self, theta):
		'''
		Transforms the object by rotating it theta degrees
		counterclockwise around its origin.

		@type theta: float
		@param theta: degrees
		@rtype: void
		'''
		self.transformed = True
		_platform.Platform().gobject_rotate(self, sx, sy)

	def setVisible(self, flag):
		'''
		Sets whether this object is visible.

		@type flag: boolean
		@rtype: void
		'''
		self.visible = flag
		_platform.Platform().gwindow_set_visible(flag, gobj = self)

	def isVisible(self):
		'''
		Returns true if this object is visible.

		@rtype: boolean
		'''
		return self.visible

	def sendForward(self):
		'''
		Moves this object one step toward the front in the z dimension.
		If it was already at the front of the stack, nothing happens.

		@rtype: void
		'''
		parent = self.getParent()
		if(parent != None): parent.sendForward(self)

	def sendToFront(self):
		'''
		Moves this object to the front of the display in the z dimension.
		By moving it to the front, this object will appear to be on top of the
		other graphical objects on the display and may hide any objects that
		are further back.

		@rtype: void
		'''
		parent = self.getParent()
		if(parent != None): parent.sendToFront(self)

	def sendBackward(self):
		'''
		Moves this object one step toward the back in the z dimension.
		If it was already at the back of the stack, nothing happens.

		@rtype: void
		'''
		parent = self.getParent()
		if(parent != None): parent.sendBackward(self)

	def sendToBack(self):
		'''
		Moves this object to the back of the display in the z dimension.
		By moving it to the back, this object will appear to be behind the other
		graphical objects on the display and may be obscured by other objects
		in front.

		@rtype: void
		'''
		parent = self.getParent()
		if(parent != None): parent.sendToBack(self)

	def contains(self, pt=None, x=None, y=None):
		'''
		Returns true if the specified point is inside the object.

		@type pt: GPoint
		@type x: float
		@type y: float
		@param pt: point to check, will override x and y
		@rtype: boolean
		'''
		if(pt != None):
			x = pt.getX()
			y = pt.getY()

		if(x == None or y == None): return False

		if(self.transformed):
			return _platform.Platform().gobject_contains(self, x, y)

		bounds = self.getBounds()
		if(bounds == None): return False
		return (x, y) in bounds

	def getType(self):
		'''
		Returns the concrete type of the object as a string, as in
		"GOval" or "GRect".

		@rtype: string
		'''
		return None

	def toString(self):
		'''
		Returns a print(ble representation of the object.)

		@rtype: string
		'''
		return None

	def getParent(self):
		'''
		Returns a pointer to the GCompound that contains this
		object.  Every GWindow is initialized to contain a single
		GCompound that is aligned with the window.  Adding
		objects to the window adds them to that GCompound,
		which means that every object you add to the window has a parent.
		Calling getParent on the top-level GCompound
		returns None.

		@rtype: GObject
		'''
		return self.parent

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

class GCompound(GObject):
	'''
	This graphical object subclass consists of a collection
	of other graphical objects.  Once assembled, the internal objects
	can be manipulated as a unit.  The GCompound keeps
	track of its own position, and all items within it are drawn
	relative to that location.
	'''

	def __init__(self):
		'''
		Creates a GCompound object with no internal components.

		@rtype: void
		'''
		GObject.__init__(self)
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

	def getType(self):
		'''
		Returns the type of this object

		@rtype: string
		'''
		return "GCompound"

	def toString(self):
		'''
		Returns a string form of this object

		@rtype: string
		'''
		return "GCompound(...)"

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

class GOval(GObject, Fillable):
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
	'''
	This graphical object subclass represents a line segment.  For
	example, the following code adds lines that mark the diagonals
	of the graphics window::

		gw = _gwindow.GWindow()
		print("This program draws the diagonals on the window.")
		gw.add(gobjects.GLine(0, 0, gw.getWidth(), gw.getHeight()))
		gw.add(gobjects.GLine(0, gw.getHeight(), gw.getWidth(), 0))
	'''

	def __init__(self, x0, y0, x1, y1):
		'''
		Initializes a line segment from its endpoints.  The point
		(x0, y0) defines the start of the
		line and the point (x1, y1) defines
		the end.

		@type x0: float
		@type x1: float
		@type y0: float
		@type y1: float
		@rtype: void
		'''
		GObject.__init__(self)
		self.x0 = x0
		self.y0 = y0
		self.dx = x1 - x0
		self.dy = y1 - y0
		_platform.Platform().gline_constructor(self, x0, y0, x1, y1)

	def setStartPoint(self, x, y):
		'''
		Sets the initial point in the line to (x, y),
		leaving the end point unchanged.  This method is therefore different from
		setLocation, which moves both components of the line segment.

		@type x: float
		@type y: float
		@rtype: void
		'''
		self.dx += self.x - x
		self.dy += self.y - y
		self.x = x
		self.y = y
		_platform.Platform().gline_set_start_point(self, x, y)

	def getStartPoint(self):
		'''
		Returns the point at which the line starts.

		@rtype: GPoint
		'''
		return _gtypes.GPoint(self.x,self.y)

	def setEndPoint(self, x, y):
		'''
		Sets the end point in the line to (x, y),
		leaving the start point unchanged.  This method is therefore different from
		setLocation, which moves both components of the line segment.

		@type x: float
		@type y: float
		@rtype: void
		'''
		self.dx = x - self.x
		self.dy = y - self.y
		_platform.Platform().gline_set_end_point(self, x, y)

	def getEndPoint(self):
		'''
		Returns the point at which the line ends.

		@rtype: GPoint
		'''
		return _gtypes.GPoint(self.x + self.dx, self.y + self.dy)

	def contains(self, x, y):
		'''
		Returns whether or not this object contains the point x, y

		@type x: float
		@type y: float
		@rtype: boolean
		'''
		if(self.transformed): return _platform.Platform().gline_contains(self, x, y)
		x0 = self.getX()
		y0 = self.getY()
		x1 = x0 + self.dx
		y1 = y0 + self.dy
		tSquared = __LINE_TOLERANCE__ * __LINE_TOLERANCE__ #!!
		if(dsq(x, y, x0, y0) < tSquared): return True
		if(dsq(x, y, x1, y1) < tSquared): return True
		if(x < min(x0, x1) - __LINE_TOLERANCE__): return False
		if(x > max(x0, x1) + __LINE_TOLERANCE__): return False
		if(y < min(y0, y1) - __LINE_TOLERANCE__): return False
		if(y > max(y0, y1) + __LINE_TOLERANCE__): return False
		if((x0 - x1) == 0 and (y0 - y1) == 0): return False
		u = ((x - x0) * (x1 - x0) + (y - y0) * (y1 - y0)) / dsq(x0, y0, x1, y1)
		return dsq(x, y, x0 + u * (x1 - x0), y0 + u * (y1 - y0)) < tSquared

	def getType(self):
		'''
		Returns the type of this object

		@rtype: string
		'''
		return "GLine"

	def toString(self):
		'''
		Returns the string form of this object

		@rtype: string
		'''
		return "GLine(" + str(self.x) + ", " + str(self.y) + ", " \
				+ str(x + dx) + ", " + str(y + dy) + ")"

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
