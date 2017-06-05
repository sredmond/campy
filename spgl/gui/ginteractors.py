'''
This file exports a hierarchy of graphical interactors similar to those
provided in the Java Swing libraries.
'''
import spgl.graphics.gobjects as _gobjects
import spgl.graphics.gtypes as _gtypes
import spgl.private.platform as _platform

class GInteractor(_gobjects.GObject):
	'''
	This class is the superclass for all graphical interactors.
	In most applications, interactors will be added to a control strip
	along one of the sides of the GWindow, but they can
	also be placed in specific positions just like any other
	GObject.
	'''

	def __init__(self):
		'''
		Initializes GObject

		@rtype: void
		'''
		_gobjects.GObject.__init__(self)
		self.actionCommand = ""

	def setActionCommand(self, cmd):
		'''
		Sets the action command to the indicated string.  If the string is not
		empty, activating the interactor generates a GActionEvent.

		@type cmd: string
		@param cmd: action command
		@rtype: void
		'''
		self.actionCommand = cmd
		_platform.Platform().setActionCommand(self, cmd)

	def getActionCommand(self):
		'''
		Returns the action command associated with the interactor.

		@rtype: string
		'''
		return self.actionCommand

	def setSize(self, width=0.0, height=0.0, size = None):
		'''
		Changes the size of the interactor to the specified width and height.

		@type width: float
		@type height: float
		@type size: GDimension, overrides width and height parameters
		@rtype: void
		'''
		if(size != None):
			width = size.getWidth()
			height = size.getHeight()
		_platform.Platform().setSize(self, width, height)

	def setBounds(self, x=0.0, y=0.0, width=0.0, height=0.0, rect = None):
		'''
		Changes the bounds of the interactor to the specified values.

		@type x: float
		@type y: float
		@type width: float
		@type height: float
		@type rect: GRectangle
		@param rect: bounding GRectangle, overrides x, y ,width and height
		@rtype: void
		'''
		if(rect != None):
			x = rect.getX()
			y = rect.getY()
			width = rect.getWidth()
			height = rect.getHeight()
		self.setLocation(x, y)
		self.setSize(width, height)

	def getBounds(self):
		'''
		Returns the bounding GRectangle of the GInteractor

		@rtype: GRectangle
		'''
		size = _platform.Platform().getSize(self)
		return _gtypes.GRectangle(self.x, self.y, size.getWidth(), size.getHeight())

class GButton(GInteractor):
	'''
	This interactor subclass represents an onscreen button.  The following
	program displays a button that, when pressed, generates the message
	"Please do not press this button again"
	(with thanks to Douglas Adams's Hitchhiker's
	Guide to the Galaxy)::

		gw = gwindow.GWindow()
		button = ginteractors.GButton("RED")
		gw.addToRegion(button, "SOUTH")
		while(True):
			e = gevents.waitForEvent(ACTION_EVENT | CLICK_EVENT)
			if (e.getEventType() == MOUSE_CLICKED):
				break
		print("Please do not press this button again.")
	'''

	def __init__(self, label):
		'''
		Creates a GButton with the specified label.  This
		constructor also sets the action command for the button to the
		label string.

		@type label: string
		@rtype: void
		'''
		GInteractor.__init__(self)
		self.label = label
		_platform.Platform().createGButton(self, label)

	def getType(self):
		'''
		Returns the type of this object

		@rtype: string
		'''
		return "GButton"

	def toString(self):
		'''
		Converts this object into string form

		@rtype: string
		'''
		return "GButton(\"" + self.label + "\")"

class GCheckBox(GInteractor):
	'''
	This interactor subclass represents an onscreen check box.  Clicking
	once on the check box selects it; clicking again removes the selection.
	If a GCheckBox has an action command, clicking on the box
	generates a GActionEvent.
	'''

	def __init__(self, label):
		'''
		Creates a GCheckBox with the specified label.  In contrast
		to the GButton constructor, this constructor does not set
		an action command.

		@type label: string
		@rtype: void
		'''
		GInteractor.__init__(self)
		self.label = label
		_platform.Platform().createGCheckBox(self, label)

	def isSelected(self):
		'''
		Returns true if the check box is selected.

		@rtype: boolean
		'''
		return _platform.Platform().isSelected(self)

	def setSelected(self, state):
		'''
		Sets the state of the check box.

		@type state: boolean
		@rtype: void
		'''
		_platform.Platform().setSelected(self, state)

	def getType(self):
		'''
		Returns the type of this object

		@rtype: string
		'''
		return "GCheckBox"

	def toString(self):
		'''
		Converts this object into string form

		@rtype: string
		'''
		return "GCheckBox(\"" + self.label + "\")"

class GSlider(GInteractor):
	'''
	This interactor subclass represents an onscreen slider.  Dragging
	the slider control generates an ActionEvent if the
	slider has a nonempty action command.
	'''

	def __init__(self, min=0, max=100, value=50):
		'''
		Creates a horizontal GSlider.  The second form allows
		the client to specify the minimum value, maximum value, and current
		value of the slider.  The first form is equivalent to calling
		GSlider(0, 100, 50).  Assigning an action command
		to the slider causes the slider to generate an action event whenever
		the slider value changes.

		@type min: int
		@type max: int
		@type value: int
		@rtype: none
		'''
		GInteractor.__init__(self)
		self.min = min
		self.max = max
		_platform.Platform().createGSlider(self, min, max, value)

	def getValue(self):
		'''
		Returns the current value of the slider.

		@rtype: int
		'''
		return _platform.Platform().getValue(self)

	def setValue(self, value):
		'''
		Sets the current value of the slider.

		@type value: int
		@rtype: void
		'''
		_platform.Platform().setValue(self, value)

	def getType(self):
		'''
		Returns the type of this object

		@rtype: string
		'''
		return "GSlider"

	def toString(self):
		'''
		Converts this object into string form

		@rtype: string
		'''
		return "GSlider()"

class GTextField(GInteractor):
	'''
	This interactor subclass represents a text field for entering short
	text strings.  Hitting enter in a text field generates a
	GActionEvent if the text field has a nonempty action command.
	'''

	def __init__(self, nChars=10):
		'''
		Creates a text field capable of holding nChars characters,
		which defaults to 10.  Assigning an action command to the text field
		causes it to generate an action event whenever the user types the
		ENTER key.

		@type nChars: int
		@rtype: void
		'''
		GInteractor.__init__(self)
		_platform.Platform().createGTextField(self, nChars)

	def getText(self):
		'''
		Returns the contents of the text field.

		@rtype: string
		'''
		return _platform.Platform().getText(self)

	def setText(self, str):
		'''
		Sets the text of the field to the specified string.

		@type str: string
		@rtype: void
		'''
		_platform.Platform().setText(self, str)

	def getType(self):
		'''
		Returns the type of this object

		@rtype: string
		'''
		return "GTextField"

	def toString(self):
		'''
		Converts this object into string form

		@rtype: string
		'''
		return "GTextField()"

class GChooser(GInteractor):
	'''
	This interactor subclass represents a selectable list.  The
	GChooser constructor creates an empty chooser.
	Once the chooser has been created, clients can use addItem
	to add the options.  For example, the following code creates a
	GChooser containing the four strings
	"Small", "Medium", "Large",
	and "X-Large"::

		sizeChooser = ginteractors.GChooser()
		sizeChooser.addItem("Small");
		sizeChooser.addItem("Medium");
		sizeChooser.addItem("Large");
		sizeChooser.addItem("X-Large");
	'''

	def __init__(self):
		'''
		Creates a chooser that initially contains no items, which are added
		using the addItem method.  Assigning an action command
		to the chooser causes it to generate an action event whenever the
		user selects an item.

		@rtype: void
		'''
		GInteractor.__init__(self)
		_platform.Platform().createGChooser(self)

	def addItem(self, item):
		'''
		Adds a new item consisting of the specified string.

		@type item: string
		@rtype: void
		'''
		_platform.Platform().addItem(self, item)

	def getSelectedItem(self):
		'''
		Returns the current item selected in the chooser.

		@rtype: string
		'''
		return _platform.Platform().getSelectedItem(self)

	def setSelectedItem(self, item):
		'''
		Sets the chooser so that it shows the specified item.  If the item
		does not exist in the chooser, no change occurs.

		@type item: string
		@rtype: void
		'''
		_platform.Platform().setSelectedItem(self, item)

	def getType(self):
		'''
		Returns the type of this object

		@rtype: string
		'''
		return "GChooser"

	def toString(self):
		'''
		Converts this object into string form

		@rtype: string
		'''
		return "GChooser()"



