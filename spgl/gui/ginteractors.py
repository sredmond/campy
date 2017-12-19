"""Graphical Interactors similar to those in the Java Swing libraries.

Provides a common interface for constructing GInteractors.

GButton:
GCheckbox:
GSlider:
GTextField:
GChooser:

"""
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
		self._action_command = ""

	@property
	def action_command(self):
		"""Get or set the action command to the indicated string.

		If the string is nonempty, activating the interactor generates a GActionEvent.

		:param str command: The action command to set or get.
		"""
		return self._action_command

	@action_command.setter
	def action_command(self, cmd):
		self._action_command = cmd
		_platform.Platform().setActionCommand(self, cmd)

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
			width = size.width
			height = size.height
		_platform.Platform().gobject_set_size(self, width, height)

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
			x,y,width,height = rect
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
	"""An onscreen button.

	The following program displays a button that, when pressed, generates the
	message: "Please do not press this button again!" (credit Douglas Adams)::

		gw = GWindow()
		button = GButton("RED")
		gw.add_to_region(button, "SOUTH")

		while True:
			e = gevents.wait_for_event(ACTION_EVENT | CLICK_EVENT)
			if e.event_type == MOUSE_CLICKED:
				break

		print("Please do not press this button again!")
	"""

	def __init__(self, label):
		"""Construct a GButton with the specified label.

		Also sets the action command for this button to the label.

		:param str label: A label for this GButton.
		"""
		super().__init__()
		self.label = label
		self.action_command = label
		_platform.Platform().gbutton_constructor(self, label)

	def __str__(self):
		return 'GButton("{}")'.format(self.label)


class GCheckBox(GInteractor):
	"""An onscreen check box.

	Clicking once on the check box selects it; clicking again removes the
	selection.

	If a GCheckBox has an action command, clicking on the box generates a
	GActionEvent.
	"""

	def __init__(self, label):
		"""
		Creates a GCheckBox with the specified label.

		In contrast to the GButton constructor, this constructor does not set an
		action command.

		:param str label: A label for this GCheckBox.
		"""
		super().__init__()
		self.label = label
		_platform.Platform().gcheckbox_constructor(self, label)

	@property
	def selected(self):
		"""Get or set whether the checkbox is selected.

		:param bool state: Whether the state is selected.
		"""
		return _platform.Platform().gcheckbox_is_selected(self)

	@selected.setter
	def selected(self, state):
		return _platform.Platform().gcheckbox_set_selected(self, state)

	def __str__(self):
		return 'GCheckBox("{}")'.format(self.label)


class GSlider(GInteractor):
	"""An onscreen slider.

	Dragging the slider handle generates a GActionEvent if the GSlider has a
	nonempty action command.
	"""

	def __init__(self, min_value=0, max_value=100, starting_value=50):
		"""Create a horizontal GSlider.

		The client can specify a minimum value, maximum value, and starting
		value.

		:param int min_value: The minimum value of this GSlider.
		:param int max_value: The maximum value of this GSlider. Should be >=
			min_value, but this is not currently enforced.
		:param int starting_value: The starting value of this GSlider. Should be
			between min_value and max_value. If not, is set to min_value.
		"""
		super().__init__()
		self.min_value = min_value
		self.max_value = max_value
		# TODO(sredmond): Error check that max_value >= min_value.
		if not min_value <= starting_value <= max_value:
			starting_value = min_value
		_platform.Platform().gslider_constructor(self, min_value, max_value, starting_value)

	@property
	def value(self):
		"""Get or set the current value of the GSlider.

		:param int value: The value of the GSlider.
		"""
		return _platform.Platform().gslider_get_value(self)

	@value.setter
	def value(self, new_value):
		_platform.Platform().gslider_set_value(self, value)

	def __str__(self):
		return "GSlider(value={}, min={}, max={})".format(self.value, self.min_value, self.max_value)


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

	@property
	def text(self):
		"""Get or set the contents of the text field."""
		return _platform.Platform().getText(self)

	@text.setter
	def text(self, content):
		_platform.Platform().setText(self, content)

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

	@property
	def selected_item(self):
		"""Return the current item selected in this GChooser.

		@rtype: string"""
		return _platform.Platform().getSelectedItem(self)

	@selected_item.setter
	def selected_item(self, item):
		"""Sets the chooser so that it shows the specified item.  If the item
		does not exist in the chooser, no change occurs.

		@type item: string
		@rtype: void"""
		_platform.Platform().setSelectedItem(self, item)

	def __str__(self):
		return "GChooser()"
