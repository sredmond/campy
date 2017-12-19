"""
This file defines the <code>GWindow</code> class which supports
drawing graphical objects on the screen.
"""
from collections import namedtuple as _nt
import math

import spgl.graphics.gtypes as _gtypes
import spgl.graphics.gobjects as _gobjects
import spgl.private.platform as _platform
import spgl.graphics.gcolor as _gcolor

####
import enum as _enum

DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 500
CENTER_MAGIC_VALUE = 999999


@_enum.unique
class Alignment(_enum.Enum):
    ALIGN_LEFT   = 0
    ALIGN_CENTER = 1
    ALIGN_RIGHT  = 2

@_enum.unique
class Region(_enum.Enum):
    REGION_CENTER = 0
    REGION_EAST   = 1
    REGION_NORTH  = 2
    REGION_SOUTH  = 3
    REGION_WEST   = 4

@_enum.unique
class CloseOperation(_enum.Enum):
    CLOSE_DO_NOTHING = 0
    CLOSE_HIDE       = 1
    CLOSE_DISPOSE    = 2
    CLOSE_EXIT       = 3


####

__ID__ = 0

class GWindowData:
	'''
	This block contains all data pertaining to the window.  Shallow copying
	of the GWindow object ensures that all copies refer to the
	same onscreen window.

	Only for use internally by the gwindow module
	'''
	def __init__(self,
				 windowWidth=0,
				 windowHeight=0,
				 visible=False,
				 windowTitle="",
				 windowColor="",
				 top=None):
		global __ID__
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		self.windowTitle = windowTitle
		self.windowColor = windowColor
		self.visible = visible
		self.top = top
		self.ID = "GWindow-" + str(__ID__)
		__ID__ = __ID__ + 1

	def __eq__(self, other):
		if(other == None): return False
		return self.windowWidth == other.windowWidth and \
			   self.windowHeight == other.windowHeight and \
			   self.visible == other.visible and \
			   self.windowTitle == other.windowTitle and \
			   self.windowColor == other.windowColor and \
			   self.top == other.top

	def __ne__(self, other):
		return not(self.__eq__(other))


class GWindow:
	'''
	This class represents a graphics window that supports simple graphics.
	Each GWindow consists of two layers.  The background layer
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

	A GWindow object may be freely copied, after which all
	copies refer to the same window.
	'''

	DEFAULT_WIDTH = 500
	DEFAULT_HEIGHT = 500

	def __init__(self, gwd=None, width=None, height=None, visible=True):
		'''
		Creates a window, either of the specified size or a default size.

		@type gwd: GWindowData
		@type width: float
		@type height: float
		@type visible: boolean
		@rtype: void
		'''
		if(gwd != None):
			self.gwd = gwd
			return

		if(width == None): width=GWindow.DEFAULT_WIDTH
		if(height == None): height=GWindow.DEFAULT_HEIGHT
		self.__initGWindow(width, height, visible)

	def __initGWindow(self, width, height, visible):
		self.gwd = GWindowData(width, height, visible)
		self.gwd.top = _gobjects.GCompound()

		_platform.Platform().gwindow_constructor(self, width, height, self.gwd.top)

		self.setColor("BLACK")
		self.setVisible(visible)

	def __eq__(self, other):
		'''
		Defines equality for a GWindow, namely that the objects share the same GWindowData

		@type other: GWindow
		@rtype: boolean
		'''
		if(other == None): return False
		return self.gwd.ID == other.gwd.ID

	def __ne__(self, other):
		'''
		Defines inequality for a GWindow, opposite of equality

		@type other: GWindow
		@rtype: boolean
		'''
		return not(self == other)

	def close(self):
		'''
		Deletes the window from the screen.

		@rtype: void
		'''
		_platform.Platform().gwindow_close(self)
		_platform.Platform().gwindow_delete(self)

	def requestFocus(self):
		'''
		Asks the system to assign the keyboard focus to the window, which
		brings it to the top and ensures that key events are delivered to
		the window.  Clicking in the window automatically requests the focus.

		@rtype: void
		'''
		_platform.Platform().gwindow_request_focus(self)

	def clear(self):
		'''
		Clears the contents of the window.

		@rtype: void
		'''
		self.gwd.top.removeAll()
		_platform.Platform().gwindow_clear(self)

	def setVisible(self, flag):
		'''
		Determines whether the window is visible on the screen.

		@rtype: void
		'''
		self.gwd.visible = flag
		_platform.Platform().gwindow_set_visible(flag, gw=self)

	def isVisible(self):
		'''
		Tests whether the window is visible.

		@rtype: boolean
		'''
		return self.gwd.visible

	def drawLine(self, p0=None, p1=None,
				 x0=None, y0=None, x1=None, y1=None):
		'''
		Draws a line connecting the specified points. If p0 and p1 are both valid
		GPoints they will override any x, y values passed in

		@type p0: GPoint
		@type p1: GPoint
		@type x0: float
		@type y0: float
		@type x1: float
		@type y1: float
		@rtype: void
		'''
		if(p0 != None and p1 != None):
			x0 = p0.getX()
			y0 = p0.getY()
			x1 = p1.getX()
			y1 = p1.getY()

		if(x0 == None or y0 == None or x1 == None or y1 == None): return

		line = GLine(x0, y0, x1, y1)
		line.setColor(self.gwd.color)
		self.draw(line)

	def drawPolarLine(self, r, theta, p0=None, x0=None, y0=None):
		'''
		Draws a line of length r in the direction theta
		from the initial point.  The angle theta is measured in
		degrees counterclockwise from the +x axis.  The method returns
		the end point of the line.

		@type r: float
		@type theta: float
		@param theta: degrees
		@type p0: GPoint
		@param p0: if p0 is passed in it will override x0, y0
		@type x0: float
		@type y0: float
		@rtype: GPoint
		@return: the end point of the line drawn
		'''
		if(p0 != None):
			x0 = p0.getX()
			y0 = p0.getY()

		if(x0 == None or y0 == None): return None

		x1 = x0 + r * math.cos(math.radians(theta))
		y1 = y0 - r * math.sin(math.radians(theta))
		self.drawLine(x0=x0, y0=y0, x1=x1, y1=y1)
		return GPoint(x1, y1)

	def drawOval(self, bounds=None,
				 x=None, y=None, width=None, height=None):
		'''
		Draws the frame of a oval with the specified bounds.

		@type bounds: GRectangle
		@param bounds: will override explict x, y, width and height parameters
		@type x: float
		@type y: float
		@type width: float
		@type height: float
		@rtype: void
		'''
		if(bounds != None):
			x = bounds.getX()
			y = bounds.getY()
			width = bounds.getWidth()
			height = bounds.getHeight()

		if(x == None or y == None or width == None or height == None): return

		oval = GOval(x, y, width, height)
		oval.setColor(self.gwd.color)
		oval.setFilled(True)
		self.draw(oval)

	def fillOval(self, bounds=None,
				 x=None, y=None, width=None, height=None):
		'''
		Fills the frame of a oval with the specified bounds.

		@type bounds: GRectangle
		@param bounds: will override explict x, y, width and height parameters
		@type x: float
		@type y: float
		@type width: float
		@type height: float
		@rtype: void
		'''
		if(bounds != None):
			x = bounds.getX()
			y = bounds.getY()
			width = bounds.getWidth()
			height = bounds.getHeight()

		if(x == None or y == None or width == None or height == None): return

		oval = GOval(x, y, width, height)
		oval.setColor(self.gwd.color)
		oval.setFilled(True)
		self.draw(oval)

	def drawRect(self, bounds=None,
				 x=None, y=None, width=None, height=None):
		'''
		Draws the frame of a rectangle with the specified bounds.

		@type bounds: GRectangle
		@param bounds: will override explict x, y, width and height parameters
		@type x: float
		@type y: float
		@type width: float
		@type height: float
		@rtype: void
		'''
		if(bounds != None):
			x = bounds.getX()
			y = bounds.getY()
			width = bounds.getWidth()
			height = bounds.getHeight()

		if(x == None or y == None or width == None or height == None): return

		rect = GRect(x, y, width, height)
		rect.setColor(self.gwd.color)
		self.draw(rect)

	def fillRect(self, bounds=None,
				 x=None, y=None, width=None, height=None):
		'''
		Fills the frame of a rectangle with the specified bounds.

		@type bounds: GRectangle
		@param bounds: will override explict x, y, width and height parameters
		@type x: float
		@type y: float
		@type width: float
		@type height: float
		@rtype: void
		'''
		if(bounds != None):
			x = bounds.getX()
			y = bounds.getY()
			width = bounds.getWidth()
			height = bounds.getHeight()

		if(x == None or y == None or width == None or height == None): return

		rect = GRect(x, y, width, height)
		rect.setColor(self.gwd.color)
		rect.setFilled(True)
		self.draw(rect)

	def setColor(self, color=None, rgb=None):
		'''
		Sets the color used for drawing.  The color parameter is
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

		self.gwd.color = _gcolor.rgb_to_hex(rgb)

	def getColor(self):
		'''
		Returns the current color as a string in the form "#rrggbb".
		In this string, the values rr, gg,
		and bb are two-digit hexadecimal values representing
		the red, green, and blue components of the color, respectively.

		@rtype: string
		'''
		return self.gwd.color

	@property
	def width(self):
		"""Return the width of the GWindow.

		:return int: the width of the GWindow in pixels."""
		return self.gwd.windowWidth

	def getWidth(self):
		'''
		Returns the width of the graphics window in pixels.

		@rtype: float
		'''
		return self.gwd.windowWidth

	@property
	def height(self):
		return self.gwd.windowHeight

	def getHeight(self):
		'''
		Returns the height of the graphics window in pixels.

		@rtype: float
		'''
		return self.gwd.windowHeight

	def repaint(self):
		'''
		Schedule a repaint on this window.

		@rtype: void
		'''
		_platform.Platform().gwindow_repaint(self)

	@property
	def title(self):
		return self.gwd.windowTitle

	@title.setter
	def title(self, title):
		self.gwd.windowTitle = title
		_platform.Platform().gwindow_set_window_title(self, title)

	def setWindowTitle(self, title):
		'''
		Sets the title of the graphics window.

		@type title: string
		@rtype: void
		'''
		self.gwd.windowTitle = title
		_platform.Platform().gwindow_set_window_title(self, title)

	def getWindowTitle(self):
		'''
		Returns the title of the graphics window.

		@rtype: string
		'''
		return gwd.windowtitle

	def draw(self, gobj, x=None, y=None):
		'''
		Draws the GObject on the background layer.  For convenience,
		the gobj parameter may be passed either as a constant
		reference or as a pointer.  If the x and y
		parameters are included, the object is moved to that location before
		drawing.

		@type gobj: GObject
		@type x: float
		@type y: float
		@rtype: void
		'''
		if(x != None and y != None):
			gobj.setLocation(x=x, y=y)
		_platform.Platform().gwindow_draw(self, gobj)

	def add(self, gobj, x=None, y=None):
		'''
		Adds the GObject to the foreground layer of the window.
		The second form of the call sets the location of the object to
		(x, y) first.

		In terms of memory management, adding a GObject pointer to
		a GWindow transfers control of that object from the client to
		the window manager.  Deleting a GWindow automatically deletes
		any GObjects it contains.


		@type gobj: GObject
		@type x: float
		@type y: float
		@rtype: void
		'''
		if(x != None and y != None):
			gobj.setLocation(x=x, y=y)
		self.gwd.top.add(gobj)

	def remove(self, gobj):
		'''
		Removes the object from the window.

		@type gobj: GObject
		@rtype: void
		'''
		self.gwd.top.remove(gobj)

	def addToRegion(self, gobj, region):
		'''
		Adds the interactor (which can also be a GLabel) to
		the control strip specified by the region parameter.
		The region parameter must be one of the strings
		"NORTH", "EAST", "SOUTH",
		or "WEST".

		@type gobj: GObject
		@type region: string
		@rtype: void
		'''
		_platform.Platform().gwindow_add_to_region(self, gobj, region)

	def removeFromRegion(self, gobj, region):
		'''
		Adds the interactor (which can also be a GLabel) to
		the control strip specified by the region parameter.
		The region parameter must be one of the strings
		"NORTH", "EAST", "SOUTH",
		or "WEST".

		@type gobj: GObject
		@type region: string
		@rtype: void
 		'''
		_platform.Platform().gwindow_remove_from_region(self, gobj, region)

	def getObjectAt(self, x, y):
		'''
		Returns a pointer to the topmost GObject containing the
		point (x, y), or NULL if no such
		object exists.

		@type x: float
		@type y: float
		@rtype: GObject
		'''
		count = self.gwd.top.getElementCount()
		for i in range(count):
			gobj = self.gwd.top.getElement(i)
			if(gobj.contains(x=x, y=y)): return gobj

		return None

	def setRegionAlignment(self, region, align):
		'''
		Sets the alignment of the specified side region as specified by the
		string align.  The region parameter must be
		one of the strings "NORTH", "EAST",
		"SOUTH", or "WEST" and the align
		parameter must be "LEFT", "RIGHT", or
		"CENTER".  By default, side panels use
		CENTER alignment.

		@type region: string
		@type align: string
		'''
		_platform.Platform().gwindow_set_region_alignment(self, region, align)

def pause(milliseconds):
	'''
	Pauses for the indicated number of milliseconds.  This function is
	useful for animation where the motion would otherwise be too fast.

	@type milliseconds: int
	@rtype: void
	'''
	# TODO(sredmond): What to replace this with?
	_platform.Platform().gtimer_pause(milliseconds)

def getScreenWidth():
	'''
	Returns the width of the entire display screen.

	@rtype: float
	'''
	return _platform.Platform().gwindow_get_screen_width()

def getScreenHeight():
	'''
	Returns the height of the entire display screen.

	@rtype: float
	'''
	return _platform.Platform().gwindow_get_screen_height();

def exitGraphics():
    '''
    Closes all graphics windows and exits from the application without
    waiting for any additional user interaction.

    @rtype: void
    '''
    _platform.Platform().gwindow_exit_graphics()
