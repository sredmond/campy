"""Interact with the graphics libraries via key events.

NOTE(sredmond): This module is still heavily under development, and should be
considered incomplete by all users.

Usage::

    @campy.onkeypress('a', modifier=SHIFT | CTRL)
    campy.keypress('a')
"""
# See: https://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
import campy.private.platform as _platform

import enum

@enum.unique
class Modifier(enum.Enum):
    SHIFT_DOWN     = 1 << 0
    CTRL_DOWN      = 1 << 1
    META_DOWN      = 1 << 2
    ALT_DOWN       = 1 << 3
    ALT_GRAPH_DOWN = 1 << 4
    BUTTON1_DOWN   = 1 << 5
    BUTTON2_DOWN   = 1 << 6
    BUTTON3_DOWN   = 1 << 7

@enum.unique
class KeyCodes(enum.Enum):
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


def onkeypress(key, modifiers=None):
    pass


def keypress(key, modifiers=None):
    """Fire a key-pressed event."""
    pass


def setup():
    # self._window.bind("<Key>", lambda event: self.__callback_key_pressed(event))
    pass


# def onkeypress(letter):
#     foobar

# @campy.register(letter, function)
