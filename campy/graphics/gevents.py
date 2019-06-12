#!/usr/bin/env python3 -tt
"""
This file defines the event types used in the Stanford Portable Graphics Libraries.
The structure of this package is adapted from the Java event model.

EventClassType
==============
This _enumeration definest the vent classes. The element values are each a single bit
and can be added or ORed together to generate an event mask. The CLICK_EVENT class
responds only to the MOUSE_CLICKED event type. The ANY_EVENT class selects any event.

    - NULL_EVENT
    - ACTION_EVENT
    - KEY_EVENT
    - TIMER_EVENT
    - WINDOW_EVENT
    - MOUSE_EVENT
    - CLICK_EVENT
    - ANY_EVENT

EventType
=========
This _enumeration type defines the event types for all events.

    - WINDOW_CLOSED
    - WINDOW_RESIZED
    - ACTION_PERFORMED
    - MOUSE_CLICKED
    - MOUSE_PRESSED
    - MOUSE_RELEASED
    - MOUSE_MOVED
    - MOUSE_DRAGGED
    - KEY_PRESSED
    - KEY_RELEASED
    - KEY_TYPED
    - TIMER_TICKED


ModifierCodes
=============
This _enumeration type defines a set of constants used to check whether
modifiers are in effect.

    - SHIFT_DOWN
    - CTRL_DOWN
    - META_DOWN
    - ALT_DOWN
    - ALT_GRAPH_DOWN
    - BUTTON1_DOWN
    - BUTTON2_DOWN
    - BUTTON3_DOWN

KeyCodes
========
This type defines the names of the key codes returned in a key event

    - BACKSPACE_KEY
    - TAB_KEY
    - ENTER_KEY
    - CLEAR_KEY
    - ESCAPE_KEY
    - PAGE_UP_KEY
    - PAGE_DOWN_KEY
    - END_KEY
    - HOME_KEY
    - LEFT_ARROW_KEY
    - UP_ARROW_KEY
    - RIGHT_ARROW_KEY
    - DOWN_ARROW_KEY
    - F1_KEY
    - F2_KEY
    - F3_KEY
    - F4_KEY
    - F5_KEY
    - F6_KEY
    - F7_KEY
    - F8_KEY
    - F9_KEY
    - F10_KEY
    - F11_KEY
    - F12_KEY
    - DELETE_KEY
    - HELP_KEY

TODO:
    Reconsider using EventClassType. Instead use inheritance?
    Deduplicate events that capture a GWindow.
    Check for validity on property access.
"""
import enum as _enum


@_enum.unique
class EventClassType(_enum.Enum):
    NULL_EVENT   = 0x000
    ACTION_EVENT = 0x010
    KEY_EVENT    = 0x020
    TIMER_EVENT  = 0x040
    WINDOW_EVENT = 0x080
    MOUSE_EVENT  = 0x100
    CLICK_EVENT  = 0x200
    ANY_EVENT    = 0x3F0


@_enum.unique
class EventType(_enum.Enum):
    WINDOW_CLOSED    = EventClassType.WINDOW_EVENT.value + 1
    WINDOW_RESIZED   = EventClassType.WINDOW_EVENT.value + 2
    CONSOLE_CLOSED   = EventClassType.WINDOW_EVENT.value + 3
    ACTION_PERFORMED = EventClassType.ACTION_EVENT.value + 1
    MOUSE_CLICKED    = EventClassType.MOUSE_EVENT.value + 1
    MOUSE_PRESSED    = EventClassType.MOUSE_EVENT.value + 2
    MOUSE_RELEASED   = EventClassType.MOUSE_EVENT.value + 3
    MOUSE_MOVED      = EventClassType.MOUSE_EVENT.value + 4
    MOUSE_DRAGGED    = EventClassType.MOUSE_EVENT.value + 5
    KEY_PRESSED      = EventClassType.KEY_EVENT.value + 1
    KEY_RELEASED     = EventClassType.KEY_EVENT.value + 2
    KEY_TYPED        = EventClassType.KEY_EVENT.value + 3
    TIMER_TICKED     = EventClassType.TIMER_EVENT.value + 1


@_enum.unique
class ModifierCodes(_enum.Enum):
    SHIFT_DOWN     = 1 << 0
    CTRL_DOWN      = 1 << 1
    META_DOWN      = 1 << 2
    ALT_DOWN       = 1 << 3
    ALT_GRAPH_DOWN = 1 << 4
    BUTTON1_DOWN   = 1 << 5
    BUTTON2_DOWN   = 1 << 6
    BUTTON3_DOWN   = 1 << 7


@_enum.unique
class KeyCodes(_enum.Enum):
    BACKSPACE_KEY = 8
    TAB_KEY = 9
    ENTER_KEY = 10
    CLEAR_KEY = 12
    ESCAPE_KEY = 27
    PAGE_UP_KEY = 33
    PAGE_DOWN_KEY = 34
    END_KEY = 35
    HOME_KEY = 36
    LEFT_ARROW_KEY = 37
    UP_ARROW_KEY = 38
    RIGHT_ARROW_KEY = 39
    DOWN_ARROW_KEY = 40
    F1_KEY = 112
    F2_KEY = 113
    F3_KEY = 114
    F4_KEY = 115
    F5_KEY = 116
    F6_KEY = 117
    F7_KEY = 118
    F8_KEY = 119
    F9_KEY = 120
    F10_KEY = 121
    F11_KEY = 122
    F12_KEY = 123
    DELETE_KEY = 127
    HELP_KEY = 156

class GEvent:
    """
    This class is the root of the hierarchy for all events.

    The standard paradigm for using GEvent is illustrated
    by the following program, which allows the user to draw lines on the
    graphics window::

        gw = _gwindow.GWindow()
        print("This program lets the user draw lines by dragging.")
        while(True):
            e = gevents.waitForEvent(gevents.EventClassType.MOUSE_EVENT)
            if(e.getEventType() == gevents.EventType.MOUSE_PRESSED):
                line = gobjects.GLine(e.getX(), e.getY(), e.getX(), e.getY());
                gw.add(line);
            elif (e.getEventType() == gevents.EventType.MOUSE_DRAGGED)
                line.setEndPoint(e.getrX(), e.getY());

    Attributes:
        event_class [EventClassType]: Enumerated type constant indicating the class of the event.
        event_type [EventType]: Enumerated type constant corresponding to the specific event type.
        time [float]: System time in milliseconds at which the event occurred.
        valid [bool]: Whether this event represents a fully-initialized valid event.
        modifiers [int]: Integer whose bits indicate what modifiers are in effect.

    Notes:
        To ensure portability among systems that represent time in different
        ways, this library uses a float to
        represent time, which is always encoded as the number of milliseconds
        that have elapsed since 00:00:00 UTC on January 1, 1970, which is
        the conventional zero point for computer-based time systems.

        To check whether the shift key is down, for example, one could use
        the following code::

            if e.modifiers & SHIFT_DOWN: ...
    """

    def __init__(self):
        '''
        Ensures that an event is properly initialized to a NULL event.

        @rtype: void
        '''
        self._event_class = EventClassType.NULL_EVENT
        self._event_type = None
        self._valid = False

        self._time = None
        self._modifiers = 0

    # "Enforce" read-only properties.
    # TODO(sredmond): This is somewhat gross and ill-advised.

    @property
    def event_class(self):
        return self._event_class

    @property
    def event_type(self):
        return self._event_type

    @property
    def valid(self):
        return self._valid

    @property
    def time(self):
        return self._time

    @property
    def modifiers(self):
        return self._modifiers

    def __str__(self):
        return "GEvent(NULL)";

class GWindowEvent(GEvent):
    '''
    This event subclass represents a window event.
    Each GWindowEvent keeps track of the event type
    (WINDOW_CLOSED, WINDOW_RESIZED) along
    with the identity of the window.

    Attributes:
        gwindow [GWindow]: Reference to the GWindow in which this event took place
    '''

    def __init__(self, event_type=None, gwindow=None):
        '''
        Creates a GWindowEvent using the specified parameters

        @type type: EventType
        @param type: type of event
        @type gw: GWindow
        @param gw: GWindow event took place in
        '''
        super().__init__()
        if event_type != None and gwindow != None:
            self._event_class = EventClassType.WINDOW_EVENT
            self._event_type = event_type
            self._valid = True

        self._gwindow = gwindow

    @property
    def gwindow(self):
        # TODO(sredmond): Do we have to recreate a new GWindow with the existing data?
        return self._gwindow

    # def getGWindow(self):
    #     '''
    #     Returns the graphics window in which this event occurred.

    #     @rtype: L{GWindow}
    #     '''
    #     import campy.graphics.gwindow as _gwindow
    #     return _gwindow.GWindow(gwd = self.gwd)

    def __str__(self):
        if not self.valid:
            return "GWindowEvent(?)"
        return  "GWindowEvent({})".format(self.event_type.name)

class GActionEvent(GEvent):
    '''
    This event subclass represents an action event.
    Action events are generated by the classes in the
    L{GInteractor}
    hierarchy.  As an example, the following program displays
    a button that, when pushed, generates the message
    &ldquo;Please do not press this button again&rdquo;
    (with thanks to Douglas Adams&rsquo;s Hitchhiker&rsquo;s
    Guide to the Galaxy)::

        gw = _gwindow.GWindow
        button = ginteractors.GButton("RED");
        gw.addToRegion(button, "SOUTH");
        while(True):
            e = gevents.waitForEvent(ACTION_EVENT | CLICK_EVENT);
            if(e.getEventType() == MOUSE_CLICKED):
                break;
            print("Please do not press this button again.")

    Attributes:
        source [GObject]: GInteractor from which event originated.
        action_command [string]: GInteractor command.
    '''

    def __init__(self, event_type=None, source=None, action_command=None):
        '''
        Creates a GActionEvent using the specified parameters.

        @type type: EventType
        @param type: type of event
        @type source: GObject
        @param source: interactor event originated from
        @type actionCommand: string
        @param actionCommand: interactor command
        @rtype: void
        '''
        super().__init__()
        if event_type != None and source != None and action_command != None:
            self._event_class = EventClassType.ACTION_EVENT
            self._event_type = event_type
            self._valid = True

        self._source = source
        self._action_command = action_command

    @property
    def source(self):
        return self._source

    @property
    def action_command(self):
        return self._action_command

    def __str__(self):
        if not valid:
            return "GActionEvent(?)"
        return "GActionEvent({}, {})".format(self.event_type.name, self.action_command)

class GMouseEvent(GEvent):
    '''
    This event subclass represents a mouse event.  Each mouse event
    records the event type (MOUSE_PRESSED,
    MOUSE_RELEASED, MOUSE_CLICKED,
    MOUSE_MOVED, MOUSE_DRAGGED) along
    with the coordinates of the event.  Clicking the mouse generates
    three events in the following order: MOUSE_PRESSED,
    MOUSE_RELEASED, MOUSE_CLICKED.

    As an example, the following program uses mouse events to let
    the user draw rectangles on the graphics window.  The only
    complexity in this code is the use of the library functions
    min and abs to ensure that the
    dimensions of the rectangle are positive::

        gw = _gwindow.GWindow
        print("This program lets the user draw rectangles.")
        while(True):
            e = gevents.waitForEvent();
            if (e.getEventType() == MOUSE_PRESSED):
                startX = e.getX();
                startY = e.getY();
                rect = gobjects.GRect(startX, startY, 0, 0);
                rect.setFilled(True);
                gw.add(rect);
            elif(e.getEventType() == MOUSE_DRAGGED):
                x = min(e.getX(), startX);
                y = min(e.getY(), startY);
                width = abs(e.getX() - startX);
                height = abs(e.getY() - startY);
                rect.setBounds(x, y, width, height);

    Attributes:
        gwindow [GWindow]: GWindow in which MouseEvent occurred.
        x [float]: The x-coordinate at which the event occurred.
        y [float]: The y-coordinate at which the event occurred.

    Notes:
        The x- and y-coordinates are given relative to the window origin at
        the upper left corner of the window.
    '''

    def __init__(self, event_type=None, gwindow=None, x=None, y=None):
        '''
        Creates a GMouseEvent using the specified parameters.

        @type type: EventType
        @param type: type of event
        @type gw: GWindow
        @param gw: window event took place in
        @type x: float
        @param x: x location of event
        @type y: float
        @param y: y location of event
        @rtype: void
        '''
        super().__init__()
        if type != None and gwindow != None and x != None and y != None:
            self._event_class = EventClassType.MOUSE_EVENT
            self._event_type = event_type
            self._valid = True

        self._gwindow = gwindow
        self._x = x
        self._y = y

    @property
    def gwindow(self):
        # TODO(sredmond): Do we have to recreate a new GWindow with the existing data?
        return self._gwindow

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __str__(self):
        if not valid:
            return "GMouseEvent(?)"
        return "GMouseEvent({}, x={}, y={})".format(self.event_type.name, self.x, self.y)

class GKeyEvent(GEvent):
    '''
    This event subclass represents a key event.  Each key event records
    the event type along with two representations of the key.  The
    getKeyChar function is more generally useful and
    returns the character after taking into account modifier keys.
    The getKeyCode function returns an integer identifying
    the key, which can be a function key as well as a standard key.
    The codes return by getKeyCode are listed in the
    KeyCodes _enumeration.

    Attributes:
        gwindow [GWindow]: GWindow in which MouseEvent occurred.
        key_char [int]: Value of key.
        key_code [int]: Code of key.

    Notes:
        Returns the character represented by the keystroke, taking the modifier
        keys into account.  For example, if the user types the 'a'
        key with the shift key down, getKeyChar will return
        'A'.  If the key code in the event does not correspond
        to a character, getKeyChar returns the null character.
    '''

    def __init__(self, event_type=None, gwindow=None, key_char=None, key_code=None):
        '''
        Creates a GKeyEvent using the specified parameters.

        @type type: EventType
        @param type: type of event
        @type gw: GWindow
        @param gw: window event takes place in
        @type keyChar: int
        @param keyChar: value of key
        @type keyCode: KeyCodes
        @param keyCode: code of key
        @rtype: void
        '''
        super().__init__()
        if event_type != None and gwindow != None and key_char != None and key_code != None:
            self._event_class = EventClassType.KEY_EVENT
            self._event_type = event_type
            self._valid = True

        self._gwindow = gwindow
        self._key_char = key_char
        self._key_code = key_code

    @property
    def gwindow(self):
        # TODO(sredmond): Do we have to recreate a new GWindow with the existing data?
        return self._gwindow

    @property
    def key_char(self):
        return self._key_char

    @property
    def key_code(self):
        return self._key_code

    def __str__(self):
        if not valid:
            return "GKeyEvent(?)"
        # TODO(sredmond): The C++ libs use key_char for KEY_TYPED for some reason.
        # Investigate further.
        return "GKeyEvent({}, {})".format(self.event_type.name, chr(self.key_code))

class GTimerEvent(GEvent):
    '''
    This event subclass represents a timer event.  Timer events are
    generated by a GTimer
    object, which produces a new event at a fixed interval measured in
    milliseconds.  As an example, the following program generates a
    timer event every two seconds, stopping when the user clicks
    somewhere in the window::


        print("This program generates timer events.")
        timer = gtimer.GTimer(2000)
        timer.start()
        while(True):
            e = gevents.waitForEvent(CLICK_EVENT | TIMER_EVENT);
            if (e.getEventType() == MOUSE_CLICKED):
                break;
        print("Timer ticked")

    Attributes:
        timer [GTimer]: GTimer from which this event originated.
    '''

    def __init__(self, event_type=None, timer=None):
        '''
        Creates a GTimerEvent for the specified timer.

        @type type: EventType
        @param type: the event type
        @type timer: GTimer
        @param timer: timer associated with event
        @rtype: void
        '''
        super().__init__()
        if event_type != None and timer != None:
            self._event_class = EventClassType.TIMER_EVENT
            self._event_type = event_type
            self._valid = True

        self._timer = timer

    @property
    def timer(self):
        return self._timer

    def __str__():
        '''
        Converts the event to a human-readable representation of the event.

        @rtype: string
        '''
        if not valid:
            return "GTimerEvent(?)"
        return "GTimerEvent({})".format(self.event_type.name)

def wait_for_click():
    '''
    Waits for a mouse click in any window, discarding any other events.

    @rtype: void
    '''
    wait_for_event(EventClassType.CLICK_EVENT)

def wait_for_event(mask=EventClassType.ANY_EVENT):
    '''
    Dismisses the process until an event occurs whose type is covered by
    the event mask.  The mask parameter is a combination of the events of
    interest.  For example, to wait for a mouse event or an action event,
    clients can use the following call:

    e = waitForEvent(MOUSE_EVENT + ACTION_EVENT);

    The mask parameter is optional.  If it is missing,
    waitForEvent accepts any event.

    As a more sophisticated example, the following code is the canonical
    event loop for an animated application that needs to respond to mouse,
    key, and timer events::

        timer = gtimer.GTimer(ANIMATION_DELAY_IN_MILLISECONDS);
        timer.start()
        while(True):
            e = gevents.waitForEvent(TIMER_EVENT + MOUSE_EVENT + KEY_EVENT)
            if(e.getEventClass == gevents.EventClassType.TIMER_EVENT):
                takeAnimationStep()
            elif(e.getEventClass == gevents.EventClassType.MOUSE_EVENT):
                handleMouseEvent(e)
            elif(e.getEventClass == gevents.EventClassType.KEY_EVENT):
                handleKeyEvent(e)

    @type mask: EventClassType
    @param mask: EventClassType to wait for, defaults to ANY_EVENT
    @rtype: GEvent
    '''
    import campy.private.platform as _platform
    return _platform.Platform().waitForEvent(mask)

def get_next_event(mask=EventClassType.ANY_EVENT):
    '''
    Checks to see if there are any events of the desired type waiting on the
    event queue.  If so, this function returns the event in exactly the same
    fashion as waitForEvent; if not, getNextEvent
    returns an invalid event.  The mask parameter is optional.
    If it is missing, getNextEvent accepts any event.

    @type mask: EventClassType
    @param mask: EventClasstype to check for, defaults to ANY_EVENT
    @rtype: GEvent
    '''
    import campy.private.platform as _platform
    return _platform.Platform().getNextEvent(mask)
