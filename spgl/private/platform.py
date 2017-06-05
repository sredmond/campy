'''
The platform module is resonsible for initalizing the connection to the java back end
as well as sending and receiving interprocess communcations. This module should not
be referenced by applications using the SPGL
'''
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

from spgl.graphics import gevents
from spgl.graphics import gtypes
from spgl.util import strlib

from spgl.system import error

from spgl.private.platformat import *
from spgl.private.platformatter import pformat

# Whether to print all pipe communications to stdout
DEBUG_PIPE = True

"""
Section: Java Backend Format Strings
------------------------------------
The following section lists format strings for the Java backend, and can/
should be updated as the text API to the Stanford Portable Library changes.
The strings are marked using keyword format syntax, which can be expanded by
keyword in Python
"""

def boolalpha(b):
    return "true" if b else "false"

class Platform:

    SOURCE_TABLE = None
    TIMER_TABLE = None
    WINDOW_TABLE = None
    BACKEND = None
    EVENT_QUEUE = None

    def __init__(self):
        if(Platform.BACKEND == None):
            print("Initializing...")
            self.startupMain()
            Platform.EVENT_QUEUE = collections.deque()  # TODO: make me threadsafe
            Platform.SOURCE_TABLE = {}
            Platform.TIMER_TABLE = {}
            Platform.WINDOW_TABLE = {}

    def createGCompound(self, gobj):
        self.put_pipe(pformat(GCompound_create, id=id(gobj)))

### Section: GWindow
    def gwindow_add_to_region(self, gw, gobj, region):
        command = pformat(GWindow_addToRegion, id=id(gw), gobj_id=id(gobj), region=region)
        self.put_pipe(command)

    def gwindow_constructor(self, gw, width, height, topCompound, visible=True):
        Platform.WINDOW_TABLE[id(gw)] = gw
        command = GWindow_constructor.format(id=id(gw), width=width, height=height, top_compound=id(top_compound), visible=visible)
        self.put_pipe(command)
        self.get_status()

    def gwindow_delete(self, gw):
        del Platform.WINDOW_TABLE[id(gw)]
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

    # TODO: from here

    def createGRect(self, gobj, width, height):
        command = GRect_create.format(id=gobj.ID, width=width, height=height)
        self.put_pipe(command)

    def setLocation(self, gobj, x, y):
        command = GObject_setLocation.format(id=gobj.ID, x=x, y=y)
        self.put_pipe(command)

    def setFilled(self, gobj, flag):
        command = GObject_setFilled.format(id=gobj.ID, flag=boolalpha(flag))
        self.put_pipe(command)

    def add(self, compound, gobj):
        command = GCompound_add.format(id=compound.ID, obj_id = gobj.ID)
        self.put_pipe(command)

    def remove(self, gobj):
        command = GObject_remove.format(id=gobj.ID)
        self.put_pipe(command)

    def setColor(self, gobj, color):
        command = GObject_setColor.format(id=gobj.ID, color=color)
        self.put_pipe(command)

    def setFillColor(self, gobj, color):
        command = GObject_setFillColor.format(id=gobj.ID, color=color)
        self.put_pipe(command)

    def close(self, gw):
        command = GWindow_close.format(id=gw.gwd.ID)
        self.put_pipe(command)

    def deleteGWindow(self, gw):
        command = GWindow_delete.format(id=gw.gwd.ID)
        self.put_pipe(command)

    def requestFocus(self, gw):
        command = GWindow_requestFocus.format(id=gw.gwd.ID)
        self.put_pipe(command)

    def clear(self, gw):
        command = GWindow_clear.format(id=gw.gwd.ID)
        self.put_pipe(command)

    def repaint(self, gw):
        command = GWindow_repaint.format(id=gw.gwd.ID)
        self.put_pipe(command)

    def setVisible(self, flag, gobj = None, gw = None):
        if(gw != None):
            command = GWindow_setVisible.format(id=gw.gwd.ID, flag=boolalpha(flag))
            self.put_pipe(command)
        elif(gobj != None):
            command = GObject_setVisible.format(id=gobj.ID, flag=boolalpha(flag))
            self.put_pipe(command)

    def createGRoundRect(self, gobj, width, height, corner):
        command = GRoundRect_create.format(id=gobj.ID, width=width, height=height, corner=corner)
        self.put_pipe(command)

    def createG3DRect(self, gobj, width, height, raised):
        command = G3DRect_create.format(id=gobj.ID, width=width, height=height, raised=boolalpha(raised))
        self.put_pipe(command)

    def setRaised(self, gobj, raised):
        command = G3DRect_setRaised.format(id=gobj.ID, raised=boolalpha(raised))
        self.put_pipe(command)

    def createGLabel(self, gobj, label):
        command = GLabel_create.format(id=gobj.ID, label=label)
        self.put_pipe(command)

    def createGLine(self, gobj, x1, y1, x2, y2):
        command = GLine_create.format(id=gobj.ID, x1=x1, y1=y1, x2=x2, y2=y2)
        self.put_pipe(command)

    def setStartPoint(self, gobj, x, y):
        command = GLine_setStartPoint.format(id=gobj.ID, x=x, y=y)
        self.put_pipe(command)

    def setEndPoint(self, gobj, x, y):
        command = GLine_setEndPoint.format(id=gobj.ID, x=x, y=y)
        self.put_pipe(command)

    def createGArc(self, gobj, width, height, start, sweep):
        command = GArc_create.format(id=gobj.ID, width=width, height=height, start=start, sweep=sweep)
        self.put_pipe(command)

    def setStartAngle(self, gobj, angle):
        command = GArc_setStartAngle.format(id=gobj.ID, angle=angle)
        self.put_pipe(command)

    def setSweepAngle(self, gobj, angle):
        command = GArc_setSweepAngle.format(id=gobj.ID, angle=angle)
        self.put_pipe(command)

    def createGImage(self, gobj,  filename):
        if(filename[0] != "/" and filename[1:3] != ":\\"):
            filename = os.getcwd() + os.sep + filename
        for i in range(len(filename)):
            if(filename[i] == "\\"):
                filename = filename[:i] + "/" + filename[i+1:]

        command = GImage_create.format(id=gobj.ID, filename=filename)
        self.put_pipe(command)
        result = self.get_result()

        if (not result.startswith("GDimension(")): raise Exception(result)
        return self.scanDimension(result)

    def createGPolygon(self, gobj):
        command = GPolygon_create.format(id=gobj.ID)
        self.put_pipe(command)

    def addVertex(self, gobj, x, y):
        command = GPolygon_addVertex.format(id=gobj.ID, x=x, y=y)
        self.put_pipe(command)

    def createGOval(self, gobj, width, height):
        command = GOval_create.format(id=gobj.ID, width=width, height=height)
        self.put_pipe(command)

    def setSize(self, gobj, width, height):
        command = GObject_setSize.format(id=gobj.ID, width=width, height=height)
        self.put_pipe(command)

    def getBounds(self, gobj):
        command = GObject_getBounds.format(id=gobj.ID)
        self.put_pipe(command)
        result = self.get_result()
        if (not result.startsWith("GRectangle(")): raise Exception(result)
        return self.scanRectangle(result)

    def setLineWidth(self, gobj, line_width):
        command = GObject_setLineWidth.format(id=gobj.ID, line_width = line_width)
        self.put_pipe(command)

    def contains(self, gobj, x, y):
        command = GObject_contains.format(id=gobj.ID, x=x, y=y)
        self.put_pipe(command)
        return (self.get_result() == "true")

    # TODO WTF is this method
    def setFrameRectangle(self, gobj, x, y, width, height):
        command = GArc_setFrameRectangle.format(id=gobj.ID, x=x, y=y, width=width, height=height)
        self.put_pipe(command)

    def setFont(self, gobj, font):
        command = GLabel_setFont.format(id=gobj.ID, font=font)
        self.put_pipe(command)

    def setLabel(self, gobj, str):
        command = GLabel_setLabel.format(id=gobj.ID, label=strlib.quote_string(str))
        self.put_pipe(command);

    def getFontAscent(self, gobj):
        command = GLabel_getFontAscent.format(id=gobj.ID)
        self.put_pipe(command)
        return float(self.get_result())

    def getFontDescent(self, gobj):
        command = GLabel_getFontDescent.format(id=gobj.ID)
        self.put_pipe(command)
        return float(self.get_result())

    def getGLabelSize(self, gobj):
        command = GLabel_getGLabelSize.format(id=gobj.ID)
        self.put_pipe(command)
        return self.scanDimension(self.get_result())

#### Section: GTimer

    def gtimer_constructor(self, timer, millis):
        Platform.TIMER_TABLE[id(timer)] = timer # TODO: why?
        command = pformat(GTimer_constructor, id=id(timer), millis=millis)
        self.put_pipe(command)

    def gtimer_delete(self, timer):
        del Platform.TIMER_TABLE[id(timer)]  # TODO: why?
        # print('Here')
        command = pformat(GTimer_delete, id=id(timer))
        # print('Here 2')
        self.put_pipe(command)

    def gtimer_start(self, timer):
        command = pformat(GTimer_start, id=id(timer))
        self.put_pipe(command)

    def gtimer_pause(self, millis):
        command = pformat(GTimer_pause, millis=millis)
        self.put_pipe(command)
        self.get_status()  # TODO: wtf

    def gtimer_stop(self, timer):
        command = pformat(GTimer_stop, id=id(timer))
        self.put_pipe(command)

#### End Section: GTimer

    def setWindowTitle(self, gw, title):
        command = GWindow_setTitle.format(id=gw.gwd.ID, title=strlib.quote_string(title))
        self.put_pipe(command)

    def getScreenWidth(self):
        command = GWindow_getScreenWidth.format()
        self.put_pipe(command)
        return float(self.get_result())

    def getScreenHeight(self):
        command = GWindow_getScreenHeight.format()
        self.put_pipe(command)
        return float(self.get_result())

    def exitGraphics(self):
        command = GWindow_exitGraphics.format()
        self.put_pipe(command)

    def draw(self, gw, gobj):
        command = GWindow_draw.format(id=gw.gwd.ID, obj_id=gobj.ID)
        self.put_pipe(command)

    def create_sound(self, sound, filename):
        # if(filename[0] != "/" and filename[1:3] != ":\\"):
        #   filename = os.getcwd() + os.sep + filename
        # for i in range(len(filename)):
        #   if(filename[i] == "\\"):
        #       filename = filename[:i] + "/" + filename[i+1:]

        command = Sound_create.format(id=id(sound), filename=filename)
        self.put_pipe(command)
        # print(self.get_result())

    def delete_sound(self, sound):
        command = Sound_delete.format(id=id(sound))
        self.put_pipe(command)

    def play_sound(self, sound):
        command = Sound_play.format(id=id(sound))
        self.put_pipe(command)

    def clearConsole(self):
        command = JBEConsole_clear.format()
        self.put_pipe(command)

    def setConsoleFont(self, font):
        command = JBEConsole_setFont.format(font=font)
        self.put_pipe(command)

    def setConsoleSize(self, width, height):
        command = JBEConsole_setSize.format(width=width, height=height)
        self.put_pipe(command)

    def scale(self, gobj, sx, sy):
        command = GObject_scale.format(id=gobj.ID, sx=sx, sy=sy)
        self.put_pipe(command)

    def rotate(self, gobj, theta):
        command = GObject_rotate.format(id=gobj.ID, theta=theta)
        self.put_pipe(command)

    def setActionCommand(self, gobj, cmd):
        command = GInteractor_setActionCommand.format(id=gobj.ID, cmd=strlib.quote_string(cmd))
        self.put_pipe(command)

    def getSize(self, gobj):
        command = GInteractor_getSize.format(id=gobj.ID)
        self.put_pipe(command)
        return self.scanDimension(self.get_result())

    def createGButton(self, gobj, label):
        Platform.SOURCE_TABLE[gobj.ID] = gobj
        command = GButton_create.format(id=gobj.ID, label=strlib.quote_string(label))
        self.put_pipe(command)

    def createGCheckBox(self, gobj, label):
        Platform.SOURCE_TABLE[gobj.ID] = gobj
        command = GCheckBox_create.format(id=gobj.ID, label=strlib.quote_string(label))
        self.put_pipe(command)

    def isSelected(self, gobj):
        command = GCheckBox_isSelected.format(id=gobj.ID)
        self.put_pipe(command)
        result = self.get_result().strip()
        return result == "true"

    def setSelected(self, gobj, state):
        command = GCheckBox_setSelected.format(id=gobj.ID, state=boolalpha(state))
        self.put_pipe(command)

    def createGSlider(self, gobj, min, max, value):
        Platform.SOURCE_TABLE[gobj.ID] = gobj
        command = GSlider_create.format(id=gobj.ID, min=min, max=max, value=value)
        self.put_pipe(command)

    def getValue(self, gobj):
        command = GSlider_getValue.format(id=gobj.ID)
        self.put_pipe(command)
        return int(self.get_result())

    def setValue(self, gobj, value):
        command = GSlider_setValue.format(id=gobj.ID, value=value)
        self.put_pipe(command)

    def createGTextField(self, gobj, num_chars):
        Platform.SOURCE_TABLE[gobj.ID] = gobj
        command = GTextField_create.format(id=gobj.ID, num_chars=num_chars)
        self.put_pipe(command)

    def getText(self, gobj):
        command = GTextField_getText.format(id=gobj.ID)
        self.put_pipe(command)
        return self.get_result()

    def setText(self, gobj, str):
        command = GTextField_setText.format(id=gobj.ID, text=strlib.quote_string(str))
        self.put_pipe(command)

    def createGChooser(self, gobj):
        Platform.SOURCE_TABLE[gobj.ID] = gobj
        command = GChooser_create.format(id=gobj.ID)
        self.put_pipe(command)

    def addItem(self, gobj, item):
        command = GChooser_addItem.format(id=gobj.ID, item=strlib.quote_string(item))
        self.put_pipe(command)

    def getSelectedItem(self, gobj):
        command = GChooser_getSelectedItem.format(id=gobj.ID)
        self.put_pipe(command)
        return self.get_result()

    def setSelectedItem(self, gobj, item):
        command = GChooser_setSelectedItem.format(id=gobj.ID, item=strlib.quote_string(item))
        self.put_pipe(command)

    def sendForward(self, gobj):
        command = GObject_sendForward.format(id=gobj.ID)
        self.put_pipe(command)

    def sendToFront(self, gobj):
        command = GObject_sendToFront.format(id=gobj.ID)
        self.put_pipe(command)

    def sendBackward(self, gobj):
        command = GObject_sendBackward.format(id=gobj.ID)
        self.put_pipe(command)

    def sendToBack(self, gobj):
        command = GObject_sendToBack.format(id=gobj.ID)
        self.put_pipe(command)

    def setRegionAlignment(self, gw, region, align):
        command = GWindow_setRegionAlignmnet.format(id=gw.gwd.ID, region=region, align=align)
        self.put_pipe(command)

    def addToRegion(self, gw, gobj, region):
        command = GWindow_addToRegion.format(id=gw.gwd.ID, obj_id=gobj.ID, region=region)
        self.put_pipe(command)

    def removeFromRegion(self, gw, gobj, region):
        command = GWindow_removeFromRegion.format(id=gw.gwd.ID, obj_id=gobj.ID, region=region)
        self.put_pipe(command)

    def file_open_file_dialog(self, title, mode, path):
        # TODO: BUGFIX for trailing slashes
        command = pformat(File_openFileDialog, title=title, mode=mode, path=path)
        self.put_pipe(command)
        return self.get_result()

    def gfilechooser_show_open_dialog(self, current_dir):
        command = GFileChooser_showOpenDialog.format(
            cwd=strlib.quote_string(current_dir)
        )
        self.put_pipe(command)
        return self.get_result()

    def gfilechooser_show_save_dialog(self, current_dir):
        command = GFileChooser_showOpenDialog.format(
            cwd=strlib.quote_string(current_dir)
        )
        self.put_pipe(command)
        return self.get_result()


    def goptionpane_show_confirm_dialog(self, message, title, confirm_type):
        command = GOptionPane_showConfirmDialog.format(
            msg=strlib.quote_string(strlib.url_encode(message)),
            title=strlib.quote_string(strlib.url_encode(title)),
            dialog_type=confirm_type.value
        )
        self.put_pipe(command)
        result = self.get_result()
        return int(result)

    def goptionpane_show_input_dialog(self, message, title):
        command = GOptionPane_showInputDialog.format(
            msg=strlib.quote_string(strlib.url_encode(message)),
            title=strlib.quote_string(strlib.url_encode(title)),
        )
        self.put_pipe(command)
        result = self.get_result()
        return strlib.url_decode(result)

    def goptionpane_show_message_dialog(self, message, title, message_type):
        command = GOptionPane_showMessageDialog.format(
            msg=strlib.quote_string(strlib.url_encode(message)),
            title=strlib.quote_string(strlib.url_encode(title)),
            dialog_type=message_type.value
        )
        self.put_pipe(command)
        self.get_result()  # Wait for dialog to close

    def goptionpane_show_option_dialog(self, message, title, options, initially_selected):
        command = GOptionPane_showOptionDialog.format(
            msg=strlib.quote_string(strlib.url_encode(message)),
            title=strlib.quote_string(strlib.url_encode(title)),
            options=', '.join(map(strlib.quote_string, map(strlib.url_encode, map(str, options)))),
            initial=strlib.quote_string(strlib.url_encode(initially_selected))
        )
        self.put_pipe(command)
        result = self.get_result()
        return int(result)

    def goptionpane_show_text_file_dialog(self, message, title, rows, cols):
        command = GOptionPane_showTextFileDialog.format(
            msg=strlib.quote_string(strlib.url_encode(message)),
            title=strlib.quote_string(strlib.url_encode(title)),
            rows=rows,
            cols=cols
        )
        self.put_pipe(command)
        self.get_result() # Wait for dialog to close

    def note_play(self, note, repeat):
        note = str(note) + boolalpha(repeat)
        command = Note_play.format(
            note=strlib.quote_string(strlib.url_encode(note))
        )
        self.put_pipe(command)
        self.get_result()  # Wait for playing to be done

    def getNextEvent(self, mask):
        if not Platform.EVENT_QUEUE:

            command = GEvent_getNextEvent.format(mask=mask.value)
            self.put_pipe(command)
            self.get_result(consume_acks=True, stop_on_event=True)  # Will add to EVENT_QUEUE?
            if not Platform.EVENT_QUEUE:
            # TODO: hotfix for lecture 9.1
                return gevents.GEvent()
                return None
        return Platform.EVENT_QUEUE.popleft()

    def waitForEvent(self, mask):
        while not Platform.EVENT_QUEUE:
            command = GEvent_waitForEvent.format(mask=mask.value)
            self.put_pipe(command)
            self.get_result()
        return Platform.EVENT_QUEUE.popleft()

    def parseEvent(self, line):
        try:
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
        from spgl.graphics import gwindow
        id = tokens[0]
        tokens = tokens[1:]

        time = float(tokens[0])
        tokens = tokens[1:]

        modifiers = int(tokens[0])
        tokens = tokens[1:]

        x = float(tokens[0])
        tokens = tokens[1:]

        y = float(tokens[0])
        tokens = tokens[1:]

        e = gevents.GMouseEvent(type, \
                                gwindow.GWindow(gwd = Platform.WINDOW_TABLE[id]), \
                                x, \
                                y)
        e.setEventTime(time)
        e.setModifiers(modifiers)
        return e

    def parseKeyEvent(self, tokens, type):
        from spgl.graphics import gwindow
        id = tokens[0]
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
                                gwindow.GWindow(gwd = Platform.WINDOW_TABLE[id]), \
                                keyChar, \
                                keyCode)
        e.setEventTime(time)
        e.setModifiers(modifiers)
        return e

    def parseTimerEvent(self, tokens, type):
        id = int(tokens[0])
        tokens = tokens[1:]

        time = float(tokens[0])
        tokens = tokens[1:]
        e = gevents.GTimerEvent(type, Platform.TIMER_TABLE[id])
        e.setEventTime(time)
        return e

    def parseWindowEvent(self, tokens, type):
        from spgl.graphics import gwindow
        id = tokens[0]
        tokens = tokens[1:]

        time = float(tokens[0])
        tokens = tokens[1:]

        e = gevents.GWindowEvent(type, gwindow.GWindow(Platform.WINDOW_TABLE[id]))
        e.setEventTime(time)
        return e

    def parseActionEvent(self, tokens, type):
        id = tokens[0]
        tokens = tokens[1:]

        action = tokens[0]
        tokens = tokens[1:]

        time = float(tokens[0])
        tokens = tokens[1:]

        e = gevents.GActionEvent(type, Platform.SOURCE_TABLE[id], action)
        e.setEventTime(time)
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
        self.put_pipe(JBEConsole_getLine)
        result = self.get_result(consume_acks=True, caller='get_line_console')
        self.echo_console(result + '\n')  # TODO: wrong for multiple inputs on one line?
        return result

    def put_console(self, line, stderr=False):
        # BUGFIX: strings that end with '\' don't print because of back-end error;
        # kludge fix by appending an "invisible" space after it
        if line.endswith('\\'):
            line += ' '
        self.put_pipe(JBEConsole_print.format(
            line=strlib.quote_string(line),
            stderr=boolalpha(stderr)
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
        self.put_pipe(JBEConsole_println)
        self.echo_console('\n', stderr)


    ################################
    # Section: Backend Communication
    # ------------------------------
    # The following section implements utility functions to communicate with the
    # Java backend process.

    def put_pipe(self, command):
        # print(command)
        cmd = command + '\n'
        # out = Platform.BACKEND.communicate(input=command+"\n", timeout=1)[0]
        if DEBUG_PIPE:
            print(cmd)
        Platform.BACKEND.stdin.write(cmd)
        Platform.BACKEND.stdin.flush()

    def get_pipe(self):
        return Platform.BACKEND.stdout.readline()

    def get_status(self):
        result = self.get_result()
        if result != 'ok':
            error(result)

    # TODO: check for whitespace returned at start or finish
    def get_result(self, consume_acks=True, stop_on_event=False, caller=''):
        while True:
            if DEBUG_PIPE:
                print('getResult(): calling getPipe()...', file=sys.stderr, flush=True)
            line = self.get_pipe()
            if DEBUG_PIPE:
                print(line)

            is_result = line.startswith('result:')
            is_result_long = line.startswith('result_long:')
            is_event = line.startswith('event:')
            is_ack = line.startswith('result:___jbe___ack___')
            has_acm_exception = 'acm.util.ErrorException' in line
            has_exception = 'xception' in line
            has_error = 'Unexpected error' in line

            if is_result_long:
                # Read a long result (sent across multiple lines)
                result = ''
                next_line = self.get_pipe()
                while next_line != 'result_long:end':
                    if not line.startswith('result:___jbe___ack___'):
                        result += line
                        if DEBUG_PIPE:
                            print('getResult(): appended line (length so far: {})'.format(len(result)), file=sys.stderr, flush=True)
                    next_line = self.get_pipe()
                if DEBUG_PIPE:
                    print('getResult(): returning long strings "{}...{}" (length {})'.format(result[:10], result[-10:], len(result)), file=sys.stderr, flush=True)
                return result
            elif ((is_result or is_event) and has_acm_exception) or (not is_result and not is_event and (has_exception or has_error)):
                # Read an error message from the back-end
                if is_result:
                    line = line[7:]  # Prune 'result:'
                elif is_event:
                    line = line[6:]  # Prune 'event:'
                result = 'ERROR emitted from Stanford Java back-end process\n{}'.format(line)
                error(result)  # TODO: import error

            elif is_result:
                # Read a regular result
                if not is_ack or not consume_acks:
                    result = line[7:]  # Prune 'result:'
                    if DEBUG_PIPE:
                        print('getResult(): returning regular result (length {}) "{}"'.format(len(result), result), file=sys.stderr, flush=True)
                    return result.strip()
                else:
                    # Just an acknowledgement of some previous event: not a real result.
                    if DEBUG_PIPE:
                        print('getResult(): saw ACK (length {}) "{}"'.format(len(line), line), file=sys.stderr, flush=True)
            elif is_event:
                # Read a Java-originated event; enqueue it to process here.
                event = self.parseEvent(line[6:].strip())
                Platform.EVENT_QUEUE.append(event)
                if stop_on_event or (event.eventClass == gevents.EventClassType.WINDOW_EVENT and event.eventType == gevents.EventType.CONSOLE_CLOSED and caller == 'get_line_console'):
                    return ''
            else:
                if '\tat ' in line or '   at ' in line:
                    # a line from a back-end Java exception stack trace;
                    # shouldn't really be happening, but back end isn't perfect.
                    # echo it here to STDERR so Python user can see it to help diagnose the issue
                    print(line, file=sys.stderr, flush=True)


    def startupMain(self):
        spl_location = pathlib.Path(__file__).parent / 'spl.jar'
        # TODO = actually communicate with the jar
        args = shlex.split('java -jar {}'.format(spl_location))
        import sys
        backend = subprocess.Popen(args, \
                                   shell=False, \
                                   stdin=subprocess.PIPE, \
                                   stdout=subprocess.PIPE, \
                                   stderr=sys.stdout, \
                                   universal_newlines=True)

        Platform.BACKEND = backend
