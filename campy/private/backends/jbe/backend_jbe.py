"""Construct a backend by using the Stanford Portable Library JAR.

This module handles the initialization of and connection to the backend JAR,
as well as all interprocess communications.

This specific backend should not be directly referenced by any client applications.
"""
# TODO(sredmond): - `multiprocessing.Queue` for events to backend.
from __future__ import print_function

__PLATFORM_INCLUDED = True

import subprocess
import time

import pathlib

import collections
import re
import sys
import os
import shlex
import threading
import queue

from campy.graphics import gevents
from campy.graphics import gtypes
from campy.util import strlib

from campy.system import error

from campy.private.backends.jbe.platformat import *
from campy.private.backends.jbe.platformatter import pformat

# Constants for dialog types, taken from Java's JFileChooser
SAVE_DIALOG = 1
OPEN_DIALOG = 1

# Whether to print all pipe communications to stdout
DEBUG_PIPE = True

def boolalpha(b):
    return "true" if b else "false"

class JavaBackend:

    SOURCE_TABLE = None
    TIMER_TABLE = None
    WINDOW_TABLE = None
    BACKEND = None
    EVENT_QUEUE = None
    Q = None

    def __init__(self):
        if(JavaBackend.BACKEND == None):
            print("Initializing...")

            from campy.private.backends.jbe.jbepipe import JavaBackendPipe
            JavaBackend.BACKEND = JavaBackendPipe()

            # self.startupMain()

            # JavaBackend.Q = queue.Queue()
            # def append_output_to_queue(out, queue):
            #     for line in iter(out.readline, b''):
            #         queue.put(line)
            #     out.close()

            # t = threading.Thread(target=append_output_to_queue, args=(JavaBackend.BACKEND.stdout, JavaBackend.Q))
            # t.daemon = True # thread dies with the program
            # t.start()

            JavaBackend.EVENT_QUEUE = collections.deque()  # TODO: make me threadsafe
            JavaBackend.SOURCE_TABLE = {}
            JavaBackend.TIMER_TABLE = {}
            JavaBackend.WINDOW_TABLE = {}

### Section: GWindow
    def gwindow_add_to_region(self, gw, gobj, region):
        command = pformat(GWindow_addToRegion, id=id(gw), gobj_id=id(gobj), region=region)
        self.put_pipe(command)

    def gwindow_constructor(self, gw, width, height, top_compound, visible=True):
        JavaBackend.WINDOW_TABLE[id(gw)] = gw
        command = pformat(GWindow_constructor, id=id(gw), width=width, height=height, top_compound=id(top_compound), visible=visible)
        self.put_pipe(command)
        self.get_status()

    def gwindow_delete(self, gw):
        del JavaBackend.WINDOW_TABLE[id(gw)]
        command = pformat(GWindow_delete, id=id(gw))
        self.put_pipe(command)

    def gwindow_close(self, gw):
        command = pformat(GWindow_close, id=id(gw))
        self.put_pipe(command)

    def gwindow_request_focus(self, gw):
        command = pformat(GWindow_requestFocus, id=id(gw))
        self.put_pipe(command)

    def gwindow_set_exit_on_close(self, gw, exit_on_close):
        command = pformat(GWindow_setExitOnClose, id=id(gw), value=exit_on_close)
        self.put_pipe(command)

    def gwindow_clear(self, gw, exit_on_close):
        command = pformat(GWindow_clear, id=id(gw))
        self.put_pipe(command)

    def gwindow_clear_canvas(self, gw, exit_on_close):
        command = pformat(GWindow_clearCanvas, id=id(gw))
        self.put_pipe(command)

    def gwindow_repaint(self, gw):
        command = pformat(GWindow_repaint, id=id(gw))
        self.put_pipe(command)

    def gwindow_set_visible(self, flag, gobj = None, gw = None):
        if(gw != None):
            command = pformat(GWindow_setVisible, id=id(gw), flag=flag)
            self.put_pipe(command)
        elif(gobj != None):
            command = pformat(GObject_setVisible, id=id(gobj), flag=flag)
            self.put_pipe(command)

    def gwindow_set_window_title(self, gw, title):
        command = pformat(GWindow_setTitle, id=id(gw), title=strlib.quote_string(title))
        self.put_pipe(command)

    def gwindow_get_screen_width(self):
        command = pformat(GWindow_getScreenWidth)
        self.put_pipe(command)
        return float(self.get_result())

    def gwindow_get_screen_height(self):
        command = pformat(GWindow_getScreenHeight)
        self.put_pipe(command)
        return float(self.get_result())

    def gwindow_exit_graphics(self):
        command = pformat(GWindow_exitGraphics)
        self.put_pipe(command)

    def gwindow_draw(self, gw, gobj):
        command = pformat(GWindow_draw, id=id(gw), obj_id=id(gobj))
        self.put_pipe(command)

    def gwindow_set_region_alignment(self, gw, region, align):
        command = pformat(GWindow_setRegionAlignmnet, id=id(gw), region=region, align=align)
        self.put_pipe(command)

    def gwindow_remove_from_region(self, gw, gobj, region):
        command = pformat(GWindow_removeFromRegion, id=id(gw), obj_id=id(gobj), region=region)
        self.put_pipe(command)

### SECTION: GObject

    def gobject_set_location(self, gobj, x, y):
        command = GObject_setLocation.format(id=id(gobj), x=x, y=y)
        self.put_pipe(command)

    def gobject_set_filled(self, gobj, flag):
        command = pformat(GObject_setFilled, id=id(gobj), flag=flag)
        self.put_pipe(command)

    def gobject_remove(self, gobj):
        command = pformat(GObject_remove, id=id(gobj))
        self.put_pipe(command)

    def gobject_set_color(self, gobj, color):
        command = pformat(GObject_setColor, id=id(gobj), color=color)
        self.put_pipe(command)

    def gobject_set_fill_color(self, gobj, color):
        command = pformat(GObject_setFillColor, id=id(gobj), color=color)
        self.put_pipe(command)

    def gobject_send_forward(self, gobj):
        command = pformat(GObject_sendForward, id=id(gobj))
        self.put_pipe(command)

    def gobject_send_to_front(self, gobj):
        command = pformat(GObject_sendToFront, id=id(gobj))
        self.put_pipe(command)

    def gobject_send_backward(self, gobj):
        command = pformat(GObject_sendBackward, id=id(gobj))
        self.put_pipe(command)

    def gobject_send_to_back(self, gobj):
        command = pformat(GObject_sendToBack, id=id(gobj))
        self.put_pipe(command)

    def gobject_set_size(self, gobj, width, height):
        command = pformat(GObject_setSize, id=id(gobj), width=width, height=height)
        self.put_pipe(command)

    def gobject_get_bounds(self, gobj):
        command = pformat(GObject_getBounds, id=id(gobj))
        self.put_pipe(command)
        result = self.get_result()
        if (not result.startsWith("GRectangle(")): raise Exception(result)
        return self.scanRectangle(result)

    def gobject_set_line_width(self, gobj, line_width):
        command = pformat(GObject_setLineWidth, id=id(gobj), line_width = line_width)
        self.put_pipe(command)

    def gobject_contains(self, gobj, x, y):
        command = pformat(GObject_contains, id=id(gobj), x=x, y=y)
        self.put_pipe(command)
        return (self.get_result() == "true")

    def gobject_scale(self, gobj, sx, sy):
        command = pformat(GObject_scale, id=id(gobj), sx=sx, sy=sy)
        self.put_pipe(command)

    def gobject_rotate(self, gobj, theta):
        command = pformat(GObject_rotate, id=id(gobj), theta=theta)
        self.put_pipe(command)
### END SECTION: GObject

### SECTION: GRect
    def grect_constructor(self, gobj, width, height):
        command = pformat(GRect_constructor, id=id(gobj), width=width, height=height)
        self.put_pipe(command)
### END SECTION: GRect

### SECTION: GRoundRect
    def groundrect_constructor(self, gobj, width, height, corner):
        command = pformat(GRoundRect_constructor, id=id(gobj), width=width, height=height, corner=corner)
        self.put_pipe(command)
### END SECTION: GRoundRect

### SECTION: GCompound
    def gcompound_constructor(self, gobj):
        command = pformat(GCompound_constructor, id=id(gobj))
        self.put_pipe(command)

    def gcompound_add(self, compound, gobj):
        command = pformat(GCompound_add, compound_id=id(compound), gobj_id=id(gobj))
        self.put_pipe(command)
        self.get_status()
### END SECTION: GCompound

### SECTION: G3DRect
    def g3drect_constructor(self, gobj, width, height, raised):
        command = pformat(G3DRect_constructor, id=id(gobj), width=width, height=height, raised=raised)
        self.put_pipe(command)

    def g3drect_set_raised(self, gobj, raised):
        command = pformat(G3DRect_setRaised, id=id(gobj), raised=raised)
        self.put_pipe(command)
### END SECTION: G3DRect

### SECTION: GOval
    def goval_constructor(self, gobj, width, height):
        command = pformat(GOval_constructor, id=id(gobj), width=width, height=height)
        self.put_pipe(command)
### END SECTION: GOval

### SECTION: GArc
    def garc_constructor(self, gobj, width, height, start, sweep):
        command = pformat(GArc_constructor, id=id(gobj), width=width, height=height, start=start, sweep=sweep)
        self.put_pipe(command)

    def garc_set_start_angle(self, gobj, angle):
        command = pformat(GArc_setStartAngle, id=id(gobj), angle=angle)
        self.put_pipe(command)

    def garc_set_sweep_angle(self, gobj, angle):
        command = pformat(GArc_setSweepAngle, id=id(gobj), angle=angle)
        self.put_pipe(command)

    # TODO WTF is this method
    def garc_set_frame_rectangle(self, gobj, x, y, width, height):
        command = pformat(GArc_setFrameRectangle, id=id(gobj), x=x, y=y, width=width, height=height)
        self.put_pipe(command)
### END SECTION: GArc

### SECTION: GLine
    def gline_constructor(self, gobj, x1, y1, x2, y2):
        command = pformat(GLine_constructor, id=id(gobj), x1=x1, y1=y1, x2=x2, y2=y2)
        self.put_pipe(command)

    def gline_set_start_point(self, gobj, x, y):
        command = pformat(GLine_setStartPoint, id=id(gobj), x=x, y=y)
        self.put_pipe(command)

    def gline_set_end_point(self, gobj, x, y):
        command = pformat(GLine_setEndPoint, id=id(gobj), x=x, y=y)
        self.put_pipe(command)
### END SECTION: GLine

### SECTION: GImage
    def gimage_constructor(self, gobj,  filename):
        if(filename[0] != "/" and filename[1:3] != ":\\"):
            filename = os.getcwd() + os.sep + filename
        for i in range(len(filename)):
            if(filename[i] == "\\"):
                filename = filename[:i] + "/" + filename[i+1:]

        command = pformat(GImage_constructor, id=id(gobj), filename=filename)
        self.put_pipe(command)
        result = self.get_result()

        # TODO(sredmond): Don't return the dimension any more.
        if (not result.startswith("GDimension(")): raise Exception(result)
        return self.scanDimension(result)
### END SECTION: GImage

### SECTION: GLabel
    def glabel_constructor(self, gobj, label):
        command = pformat(GLabel_constructor, id=id(gobj), label=label)
        self.put_pipe(command)

    def glabel_set_font(self, gobj, font):
        command = pformat(GLabel_setFont, id=id(gobj), font=font)
        self.put_pipe(command)


    def glabel_set_label(self, gobj, str):
        command = pformat(GLabel_setLabel, id=id(gobj), label=strlib.quote_string(str))
        self.put_pipe(command);

    def glabel_get_font_ascent(self, gobj):
        command = pformat(GLabel_getFontAscent, id=id(gobj))
        self.put_pipe(command)
        return float(self.get_result())

    def glabel_get_font_descent(self, gobj):
        command = pformat(GLabel_getFontDescent, id=id(gobj))
        self.put_pipe(command)
        return float(self.get_result())

    def glabel_get_size(self, gobj):
        command = pformat(GLabel_getSize, id=id(gobj))
        self.put_pipe(command)
        # SO BROKEN
        return self.scanDimension(self.get_result())
### END SECTION: GLabel

### SECTION: GPolygon
    def gpolygon_constructor(self, gobj):
        command = pformat(GPolygon_constructor, id=id(gobj))
        self.put_pipe(command)

    def gpolygon_add_vertex(self, gobj, x, y):
        command = pformat(GPolygon_addVertex, id=id(gobj), x=x, y=y)
        self.put_pipe(command)
### END SECTION: GPolygon

### Section: GTimer
    def gtimer_constructor(self, timer, millis):
        JavaBackend.TIMER_TABLE[id(timer)] = timer # TODO: why?
        command = pformat(GTimer_constructor, id=id(timer), millis=millis)
        self.put_pipe(command)

    def gtimer_delete(self, timer):
        del JavaBackend.TIMER_TABLE[id(timer)]  # TODO: why?
        command = pformat(GTimer_delete, id=id(timer))
        self.put_pipe(command)

    def gtimer_start(self, timer):
        command = pformat(GTimer_start, id=id(timer))
        self.put_pipe(command)

    def gtimer_pause(self, millis):
        # TODO(sredmond): Does this method pause all active timers instead of just one? That seems wrong.
        command = pformat(GTimer_pause, millis=millis)
        self.put_pipe(command)
        self.get_status()  # TODO: wtf

    def gtimer_stop(self, timer):
        command = pformat(GTimer_stop, id=id(timer))
        self.put_pipe(command)
### End Section: GTimer

### Section: GBufferedImage
    def gbufferedimage_constructor(self, gobj, x, y, width, height):
        JavaBackend.SOURCE_TABLE[id(gobj)] = gobj
        command = pformat(GBufferedImage_constructor, id=id(gobj), x=int(x), y=int(y), width=int(width), height=int(height))
        self.put_pipe(command)

    def gbufferedimage_fill(self, gobj, rgb):
        command = pformat(GBufferedImage_fill, id=id(gobj), rgb=rgb)
        self.put_pipe(command)

    def gbufferedimage_fill_region(self, gobj, x, y, width, height, rgb):
        command = pformat(GBufferedImage_fillRegion, id=id(gobj), x=int(x), y=int(y), width=int(width), height=int(height), rgb=rgb)
        self.put_pipe(command)

    def gbufferedimage_load(self, gobj, filename):
        command = pformat(GBufferedImage_load, id=id(gobj), filename=filename)
        self.put_pipe(command)
        return self.get_result()

    def gbufferedimage_resize(self, gobj, width, height, retain):
        command = pformat(GBufferedImage_resize, id=id(gobj), width=int(width), height=int(height), retain=retain)
        self.put_pipe(command)

    def gbufferedimage_save(self, gobj, filename):
        command = pformat(GBufferedImage_save, id=id(gobj), filename=filename)
        self.put_pipe(command)
        self.get_status()  # ???

    def gbufferedimage_set_rgb(self, gobj, x, y, rgb):
        command = pformat(GBufferedImage_setRGB, id=id(gobj), x=int(x), y=int(y), rgb=rgb)
        self.put_pipe(command)

    def gbufferedimage_update_all_pixels(self, gobj, base64):
        command = pformat(GBufferedImage_updateAllPixels, id=id(gobj), base64=base64)
        self.put_pipe(command)
### End Section: GBufferedImage

### Section: Sound

    def create_sound(self, sound, filename):
        # if(filename[0] != "/" and filename[1:3] != ":\\"):
        #   filename = os.getcwd() + os.sep + filename
        # for i in range(len(filename)):
        #   if(filename[i] == "\\"):
        #       filename = filename[:i] + "/" + filename[i+1:]

        command = pformat(Sound_create, id=id(sound), filename=filename)
        self.put_pipe(command)
        # print(self.get_result())

    def delete_sound(self, sound):
        command = pformat(Sound_delete, id=id(sound))
        self.put_pipe(command)

    def play_sound(self, sound):
        command = pformat(Sound_play, id=id(sound))
        self.put_pipe(command)

### END SECTION: Sound

### SECTION: JBEConsole

    def clearConsole(self):
        command = pformat(JBEConsole_clear)
        self.put_pipe(command)

    def setConsoleFont(self, font):
        command = pformat(JBEConsole_setFont, font=font)
        self.put_pipe(command)

    def setConsoleSize(self, width, height):
        command = pformat(JBEConsole_setSize, width=width, height=height)
        self.put_pipe(command)

### END SECTION: JBEConsole

### SECTION: GInteractor

    def setActionCommand(self, gobj, cmd):
        command = pformat(GInteractor_setActionCommand, id=id(gobj), cmd=cmd)
        self.put_pipe(command)

    def getSize(self, gobj):
        command = pformat(GInteractor_getSize, id=id(gobj))
        self.put_pipe(command)
        return self.scanDimension(self.get_result())

    def gbutton_constructor(self, gobj, label):
        JavaBackend.SOURCE_TABLE[id(gobj)] = gobj
        command = pformat(GButton_constructor, id=id(gobj), label=label)
        self.put_pipe(command)

    def gcheckbox_constructor(self, gobj, label):
        JavaBackend.SOURCE_TABLE[id(gobj)] = gobj
        command = pformat(GCheckBox_constructor, id=id(gobj), label=label)
        self.put_pipe(command)

    def gcheckbox_is_selected(self, gobj):
        command = pformat(GCheckBox_isSelected, id=id(gobj))
        self.put_pipe(command)
        result = self.get_result().strip()
        return result == "true"

    def gcheckbox_set_selected(self, gobj, state):
        command = pformat(GCheckBox_setSelected, id=id(gobj), state=state)
        self.put_pipe(command)

    def gslider_constructor(self, gobj, min, max, value):
        JavaBackend.SOURCE_TABLE[id(gobj)] = gobj
        command = pformat(GSlider_constructor, id=id(gobj), min=min, max=max, value=value)
        self.put_pipe(command)

    def gslider_get_value(self, gobj):
        command = pformat(GSlider_getValue, id=id(gobj))
        self.put_pipe(command)
        return int(self.get_result())

    def gslider_set_value(self, gobj, value):
        command = pformat(GSlider_setValue, id=id(gobj), value=value)
        self.put_pipe(command)

    def createGTextField(self, gobj, num_chars):
        JavaBackend.SOURCE_TABLE[id(gobj)] = gobj
        command = pformat(GTextField_constructor, id=id(gobj), num_chars=num_chars)
        self.put_pipe(command)

    def getText(self, gobj):
        command = pformat(GTextField_getText, id=id(gobj))
        self.put_pipe(command)
        return self.get_result()

    def setText(self, gobj, str):
        command = pformat(GTextField_setText, id=id(gobj), text=strlib.quote_string(str))
        self.put_pipe(command)

    def createGChooser(self, gobj):
        JavaBackend.SOURCE_TABLE[id(gobj)] = gobj
        command = pformat(GChooser_constructor, id=id(gobj))
        self.put_pipe(command)

    def addItem(self, gobj, item):
        command = pformat(GChooser_addItem, id=id(gobj), item=strlib.quote_string(item))
        self.put_pipe(command)

    def getSelectedItem(self, gobj):
        command = pformat(GChooser_getSelectedItem, id=id(gobj))
        self.put_pipe(command)
        return self.get_result()

    def setSelectedItem(self, gobj, item):
        command = pformat(GChooser_setSelectedItem, id=id(gobj), item=strlib.quote_string(item))
        self.put_pipe(command)

### END SECTION: GInteractor

    def file_open_file_dialog(self, title, mode, path):
        # TODO: BUGFIX for trailing slashes
        command = pformat(File_openFileDialog, title=title, mode=mode, path=path)
        self.put_pipe(command)
        return self.get_result()

    def gfilechooser_show_open_dialog(self, current_dir, file_filter):
        command = pformat(GFileChooser_showOpenDialog,
            current_dir=current_dir,
            file_filter=file_filter
        )
        self.put_pipe(command)
        return self.get_result()

    def gfilechooser_show_save_dialog(self, current_dir, file_filter):
        command = pformat(GFileChooser_showOpenDialog,
            current_dir=current_dir,
            file_filter=file_filter
        )
        self.put_pipe(command)
        return self.get_result()


    def goptionpane_show_confirm_dialog(self, message, title, confirm_type):
        command = pformat(GOptionPane_showConfirmDialog,
            message=message,
            title=title,
            type=confirm_type.value
        )
        self.put_pipe(command)
        result = self.get_result()
        return int(result)

    def goptionpane_show_input_dialog(self, message, title):
        command = pformat(GOptionPane_showInputDialog,
            message=message,
            title=title
        )
        self.put_pipe(command)
        result = self.get_result()
        return strlib.url_decode(result)

    def goptionpane_show_message_dialog(self, message, title, message_type):
        command = pformat(GOptionPane_showMessageDialog,
            message=message,
            title=title,
            type=message_type.value
        )
        self.put_pipe(command)
        self.get_result()  # Wait for dialog to close

    def goptionpane_show_option_dialog(self, message, title, options, initially_selected):
        command = pformat(GOptionPane_showOptionDialog,
            message=message,
            title=title,
            options=', '.join(map(strlib.quote_string, map(strlib.url_encode, map(str, options)))),
            initial=initially_selected
        )
        self.put_pipe(command)
        result = self.get_result()
        return int(result)

    def goptionpane_show_text_file_dialog(self, message, title, rows, cols):
        command = pformat(GOptionPane_showTextFileDialog,
            message=strlib.quote_string(strlib.url_encode(message)),
            title=strlib.quote_string(strlib.url_encode(title)),
            rows=rows,
            cols=cols
        )
        self.put_pipe(command)
        self.get_result() # Wait for dialog to close

    def note_play(self, note, repeat):
        note = str(note) + boolalpha(repeat)
        command = pformat(Note_play,
            note=note
        )
        self.put_pipe(command)
        self.get_result()  # Wait for playing to be done

    ##############################
    # Section: Event Interaction
    # ----------------------------
    # This section implements interaction with the JBE console to process Events

    def getNextEvent(self, mask):
        if not JavaBackend.EVENT_QUEUE:

            command = pformat(GEvent_getNextEvent, mask=mask.value)
            self.put_pipe(command)
            self.get_result(consume_acks=True, stop_on_event=True)  # Will add to EVENT_QUEUE?
            if not JavaBackend.EVENT_QUEUE:
            # TODO: hotfix for lecture 9.1
                return gevents.GEvent()
                return None
        return JavaBackend.EVENT_QUEUE.popleft()

    def waitForEvent(self, mask):
        while not JavaBackend.EVENT_QUEUE:
            command = pformat(GEvent_waitForEvent, mask=mask.value)
            self.put_pipe(command)
            self.get_result()
        return JavaBackend.EVENT_QUEUE.popleft()

    def parseEvent(self, line):
        try:
            # TODO(sredmond): This is a broken way to parse tokens.
            # Breaks when an event parameter has a space in it.
            tokens = re.findall(r"[-\w\.\(]+", line)
            if(tokens[0] == "mousePressed("):
                return self.parseMouseEvent(tokens[1:], gevents.EventType.MOUSE_PRESSED)
            elif(tokens[0] == "mouseReleased("):
                return self.parseMouseEvent(tokens[1:], gevents.EventType.MOUSE_RELEASED)
            elif(tokens[0] == "mouseClicked("):
                return self.parseMouseEvent(tokens[1:], gevents.EventType.MOUSE_CLICKED)
            elif(tokens[0] == "mouseMoved("):
                return self.parseMouseEvent(tokens[1:], gevents.EventType.MOUSE_MOVED)
            elif(tokens[0] == "mouseDragged("):
                return self.parseMouseEvent(tokens[1:], gevents.EventType.MOUSE_DRAGGED)
            elif(tokens[0] == "keyPressed("):
                return self.parseKeyEvent(tokens[1:], gevents.EventType.KEY_PRESSED)
            elif(tokens[0] == "keyReleased("):
                return self.parseMouseEvent(tokens[1:], gevents.EventType.KEY_RELEASED)
            elif(tokens[0] == "keyTyped("):
                return self.parseKeyEvent(tokens[1:], gevents.EventType.KEY_TYPED)
            elif(tokens[0] == "actionPerformed("):
                return self.parseActionEvent(tokens[1:], gevents.EventType.ACTION_PERFORMED)
            elif(tokens[0] == "timerTicked("):
                return self.parseTimerEvent(tokens[1:], gevents.EventType.TIMER_TICKED)
            elif(tokens[0] == "windowClosed("):
                return self.parseWindowEvent(tokens[1:], gevents.EventType.WINDOW_CLOSED)
            elif(tokens[0] == "windowResized("):
                return self.parseWindowEvent(tokens[1:], gevents.EventType.RESIZED)
            elif(tokens[0] == "lastWindowClosed("):
                print("Exited normally")
                sys.exit(0)
            else:
                dummy = 1
                # ignore for now
            return gevents.GEvent()
        except Exception as inst:
            print("EXCEPTION")
            print("type:")
            print(type(inst))
            print("exception data:")
            print(inst)
            print("line:")
            print(line)
            raise
            return gevents.GEvent()

    def parseMouseEvent(self, tokens, type):
        from campy.graphics import gwindow
        id = int(tokens[0])
        tokens = tokens[1:]

        time = float(tokens[0])
        tokens = tokens[1:]

        modifiers = int(tokens[0])
        tokens = tokens[1:]

        x = float(tokens[0])
        tokens = tokens[1:]

        y = float(tokens[0])
        tokens = tokens[1:]
        print(JavaBackend.WINDOW_TABLE)

        e = gevents.GMouseEvent(type, \
                                JavaBackend.WINDOW_TABLE[id], \
                                x, \
                                y)
        # Manually set the internals of the GEvent.
        e._time = time
        e._modifiers = modifiers
        return e

    def parseKeyEvent(self, tokens, type):
        from campy.graphics import gwindow
        id = int(tokens[0])
        tokens = tokens[1:]

        time = float(tokens[0])
        tokens = tokens[1:]

        modifiers = int(tokens[0])
        tokens = tokens[1:]

        keyChar = int(tokens[0])
        tokens = tokens[1:]

        keyCode = int(tokens[0])
        tokens = tokens[1:]

        e = gevents.GKeyEvent(type, \
                                gwindow.GWindow(gwd = JavaBackend.WINDOW_TABLE[id]), \
                                keyChar, \
                                keyCode)
        # Manually set the internals of the GEvent.
        e._time = time
        e._modifiers = modifiers
        return e

    def parseTimerEvent(self, tokens, type):
        id = int(tokens[0])
        tokens = tokens[1:]

        time = float(tokens[0])
        tokens = tokens[1:]
        e = gevents.GTimerEvent(type, JavaBackend.TIMER_TABLE[id])

        # Manually set the internals of the GEvent.
        e._time = time
        return e

    def parseWindowEvent(self, tokens, type):
        from campy.graphics import gwindow
        id = tokens[0]
        tokens = tokens[1:]

        time = float(tokens[0])
        tokens = tokens[1:]

        e = gevents.GWindowEvent(type, gwindow.GWindow(JavaBackend.WINDOW_TABLE[id]))
        # Manually set the internals of the GEvent.
        e._time = time
        return e

    def parseActionEvent(self, tokens, type):
        id = int(tokens[0])
        tokens = tokens[1:]

        action = tokens[0]
        tokens = tokens[1:]

        time = float(tokens[0])
        tokens = tokens[1:]

        e = gevents.GActionEvent(type, JavaBackend.SOURCE_TABLE[id], action)

        # Manually set the internals of the GEvent.
        e._time = time
        return e

    def scanDimension(self, str):
        tokens = re.findall(r"[-:\w\.]+", str)
        #skip "GDimension"
        tokens = tokens[1:]
        width = float(tokens[0])
        tokens = tokens[1:]
        height = float(tokens[0])
        return gtypes.GDimension(width, height)

    def scanRectangle(self, str):
        tokens = re.findall(r"[-:\w\.]+", str)
        #skip "GRectangle"
        tokens = tokens[1:]
        x = float(tokens[0])
        tokens = tokens[1:]
        y = float(tokens[0])
        tokens = tokens[1:]
        width = float(tokens[0])
        tokens = tokens[1:]
        height = float(tokens[0])
        return gtypes.GRectangle(x, y, width, height)

    ##############################
    # Section: Console Interaction
    # ----------------------------
    # This section implements interaction with the JBE console for the Console class

    def get_line_console(self):
        self.put_pipe(pformat(JBEConsole_getLine))
        result = self.get_result(consume_acks=True, caller='get_line_console')
        self.echo_console(result + '\n')  # TODO: wrong for multiple inputs on one line?
        return result

    def put_console(self, line, stderr=False):
        # BUGFIX: strings that end with '\' don't print because of back-end error;
        # kludge fix by appending an "invisible" space after it
        if line.endswith('\\'):
            line += ' '
        self.put_pipe(pformat(JBEConsole_print,
            line=line,
            stderr=stderr
        ))
        self.echo_console(line, stderr)

    def echo_console(self, line, stderr=False):
        if True: # getConsoleEcho()
            needs_flush = '\n' in line
            if needs_flush:
                sys.stdout.flush()
            (sys.stdout if not stderr else sys.stderr).write(line)
            if needs_flush:
                sys.stdout.flush()
                sys.stderr.flush()

    def end_line_console(self, stderr):
        self.put_pipe(pformat(JBEConsole_println))
        self.echo_console('\n', stderr)


    ################################
    # Section: Backend Communication
    # ------------------------------
    # The following section implements utility functions to communicate with the
    # Java backend process.

    def put_pipe(self, command):
        self.BACKEND.write(command)

    def get_pipe(self):
        return self.BACKEND.read()

    def get_status(self):
        return self.BACKEND.get_status()

    def get_result(self):
        return self.BACKEND.get_result()

    # def put_pipe(self, command):
    #     # print(command)
    #     cmd = command + '\n'
    #     # out = JavaBackend.BACKEND.communicate(input=command+"\n", timeout=1)[0]
    #     if DEBUG_PIPE:
    #         print(cmd)
    #     JavaBackend.BACKEND.stdin.write(cmd)
    #     JavaBackend.BACKEND.stdin.flush()

    # def get_pipe(self):
    #     return JavaBackend.Q.get()
    #     # return JavaBackend.BACKEND.stdout.readline()

    # def get_status(self):
    #     result = self.get_result()
    #     if result != 'ok':
    #         error(result)

    # # TODO: check for whitespace returned at start or finish
    # def get_result(self, consume_acks=True, stop_on_event=False, caller=''):
    #     while True:
    #         if DEBUG_PIPE:
    #             print('getResult(): calling getPipe()...', file=sys.stderr, flush=True)
    #         line = self.get_pipe()
    #         if DEBUG_PIPE:
    #             print(line)

    #         is_result = line.startswith('result:')
    #         is_result_long = line.startswith('result_long:')
    #         is_event = line.startswith('event:')
    #         is_ack = line.startswith('result:___jbe___ack___')
    #         has_acm_exception = 'acm.util.ErrorException' in line
    #         has_exception = 'xception' in line
    #         has_error = 'Unexpected error' in line

    #         if is_result_long:
    #             # Read a long result (sent across multiple lines)
    #             result = ''
    #             next_line = self.get_pipe()
    #             while next_line != 'result_long:end':
    #                 if not line.startswith('result:___jbe___ack___'):
    #                     result += line
    #                     if DEBUG_PIPE:
    #                         print('getResult(): appended line (length so far: {})'.format(len(result)), file=sys.stderr, flush=True)
    #                 next_line = self.get_pipe()
    #             if DEBUG_PIPE:
    #                 print('getResult(): returning long strings "{}...{}" (length {})'.format(result[:10], result[-10:], len(result)), file=sys.stderr, flush=True)
    #             return result
    #         elif ((is_result or is_event) and has_acm_exception) or (not is_result and not is_event and (has_exception or has_error)):
    #             # Read an error message from the back-end
    #             if is_result:
    #                 line = line[7:]  # Prune 'result:'
    #             elif is_event:
    #                 line = line[6:]  # Prune 'event:'
    #             result = 'ERROR emitted from Stanford Java back-end process\n{}'.format(line)
    #             error(result)  # TODO: import error

    #         elif is_result:
    #             # Read a regular result
    #             if not is_ack or not consume_acks:
    #                 result = line[7:]  # Prune 'result:'
    #                 if DEBUG_PIPE:
    #                     print('getResult(): returning regular result (length {}) {}'.format(len(result), repr(result)), file=sys.stderr, flush=True)
    #                 return result.strip()
    #             else:
    #                 # Just an acknowledgement of some previous event: not a real result.
    #                 if DEBUG_PIPE:
    #                     print('getResult(): saw ACK (length {}) "{}"'.format(len(line), line), file=sys.stderr, flush=True)
    #         elif is_event:
    #             # Read a Java-originated event; enqueue it to process here.
    #             event = self.parseEvent(line[6:].strip())
    #             JavaBackend.EVENT_QUEUE.append(event)
    #             if stop_on_event or (event.event_class == gevents.EventClassType.WINDOW_EVENT and event.event_type == gevents.EventType.CONSOLE_CLOSED and caller == 'get_line_console'):
    #                 return ''
    #         else:
    #             if '\tat ' in line or '   at ' in line:
    #                 # a line from a back-end Java exception stack trace;
    #                 # shouldn't really be happening, but back end isn't perfect.
    #                 # echo it here to STDERR so Python user can see it to help diagnose the issue
    #                 print(line, file=sys.stderr, flush=True)


    # def startupMain(self):
    #     spl_location = pathlib.Path(__file__).parent / 'spl.jar'
    #     # TODO = actually communicate with the jar
    #     args = shlex.split('java -jar {}'.format(spl_location))
    #     import sys
    #     backend = subprocess.Popen(args, \
    #                                shell=False, \
    #                                stdin=subprocess.PIPE, \
    #                                stdout=subprocess.PIPE, \
    #                                stderr=sys.stdout, \
    #                                universal_newlines=True)

    #     JavaBackend.BACKEND = backend
