"""Interact with the graphics libraries via window events.

There are only two types of window events to which a caller can subscribe:

- WindowClosed: The graphical window was closed.
- WindowResized: The graphical window was resized.
"""
import campy.private.platform as _platform

class GWindowEvent:
    def __init__(self, gwindow, x, y, width, height):
        """Construct a"""
        self._gwindow = gwindow
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def window(self):
        return self._gwindow

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __str__(self):
        return "GWindowEvent(x={}, y={}, width={}, height={})".format(self.x, self.y, self.width, self.height)

def onwindowresized(function):
    _platform.Platform().event_add_window_changed_handler(function)


def onwindowmoved(function):
    pass

# Define decorators for all of the common types of events.
def onwindowclosed(function):
    """

    If it returns a False-y value, the default action is taken.
    If it returns a Truth-y value, the default action is skipped.

    Note that this is OPPOSITE how Javascript does things.

    There can be only one window closed handler per window.
    """
    _platform.Platform().event_set_window_closed_handler(function)

