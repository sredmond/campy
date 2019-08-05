# Two modes:
#   (1) interactive: Everything runs in one thread. Long-running event handlers block the update.
#   (2) separated: non-main thread for all non-mainloop code.
"""
We match the Tk hierarchy of classes onto the ACM hierarchy as follows:
Each application (i.e. instance of TkBackend) has exactly one Tk root (i.e. one tkinter.Tk()).

This top widget takes care of everything.

After instantiation of the first instance of a TkBackend, the tkinter._default_root will be set.

Except in extreme circumstances, there should only ever be one instance of TkBackend.

Each GWindow is associated to a single Canvas. GWindows beyond the first will open a new Toplevel window.

## EXIT BEHAVIOR
(A) At program termination, Tk object is not destroyed, and "program" isn't done until Tk window is closed.
(B) At program termination, Tk object is destroyed and program is finished.
"""
# TODO(sredmond): For all methods that implicitly operate on the most recent
# GWindow, allow the client to pass an optional GWindow on which to operate.
# It is discouraged to instantiate multiple instances of Tk graphics
from campy.private.backends.backend_base import GraphicsBackendBase
from campy.private.backends.tk.menu import setup_menubar

import atexit
import functools
import logging
import pathlib
import tkinter as tk
import tkinter.font as tkfont
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmessagebox
import tkinter.simpledialog as tksimpledialog
import threading
import sys

# TODO(sredmond): What magic is this?
try:
    from _tkinter import DONT_WAIT
except ImportError:
    DONT_WAIT = 2

# Load the PIL PhotoImage class if possible, otherwise use tkinter's.
try:
    from PIL.ImageTk import PhotoImage
except ImportError:
    from tkinter import PhotoImage


# Module-level logger.
logger = logging.getLogger(__name__)

class TkWindow:
    """The Tk equivalent to a :class:`GWindow`."""
    def __init__(self, root, width, height, parent):
        self._parent = parent

        self._master = tk.Toplevel(root)
        self._closed = False
        self._master.protocol("WM_DELETE_WINDOW", self._close)
        self._master.resizable(width=False, height=False)  # Disable resizing by default.

        # Raise the master to be the top window.
        self._master.wm_attributes("-topmost", 1)  # TODO(sredmond): Is this really necessary?
        self._master.lift()
        self._master.focus_force()

        # TODO(sredmond): On macOS, multiple backends might race to set the process-level menu bar.
        setup_menubar(self._master)

        self._frame = tk.Frame(self._master)  #, bd=2, bg='red'

        self._canvas = tk.Canvas(self._frame, width=width, height=height, highlightthickness=0, bd=0)
        self._canvas.pack(fill=tk.BOTH, expand=True)

        self._frame.pack(fill=tk.BOTH, expand=True)
        self._frame.update()

        self._master.update()

        # Empty side regions for interaction. Their ordering and layout depends
        # on order of construction, so start them off empty.
        self._top = None
        self._bottom = None
        self._left = None
        self._right = None

    @property
    def canvas(self):
        return self._canvas

    @property
    def top(self):
        """Get the top bar for interactors, creating it if needed."""
        if not self._top:
            self._top = tk.Frame(self._master)
            self._top.pack(fill=tk.X, side=tk.TOP)
            self._frame.pack_forget()
            self._frame.pack(fill=tk.BOTH, expand=True)
        return self._top

    @property
    def bottom(self):
        """Get the bottom bar for interactors, creating it if needed."""
        if not self._bottom:
            self._bottom = tk.Frame(self._master)
            self._bottom.pack(fill=tk.X, side=tk.BOTTOM)
            self._frame.pack_forget()
            self._frame.pack(fill=tk.BOTH, expand=True)
        return self._bottom

    @property
    def left(self):
        """Get the left bar for interactors, creating it if needed."""
        if not self._left:
            self._left = tk.Frame(self._master)
            self._left.pack(fill=tk.Y, side=tk.LEFT)
            self._frame.pack_forget()
            self._frame.pack(fill=tk.BOTH, expand=True)
        return self._left

    @property
    def right(self):
        """Get the right bar for interactors, creating it if needed."""
        if not self._right:
            self._right = tk.Frame(self._master)
            self._right.pack(fill=tk.Y, side=tk.LEFT)
            self._frame.pack_forget()
            self._frame.pack(fill=tk.BOTH, expand=True)
        return self._right

    def clear(self):
        # Delete all canvas elements and all interactors, but leave the canvas and interactor regions in place."""
        self.clear_canvas()
        if self._top:
            for child in self._top.children:
                child.destroy()
        if self._bottom:
            for child in self._bottom.children:
                child.destroy()
        if self._left:
            for child in self._left.children:
                child.destroy()
        if self._right:
            for child in self._right.children:
                child.destroy()

    def clear_canvas(self):
        # Delete all canvas elements, but leave the canvas (and all interactor regions) in place.
        self.canvas.delete('all')

    def _close(self):
        if self._closed: return
        self._closed = True

        self._master.destroy()
        # TODO(sredmond): Consider autoflushing like Zelle.
        self._parent._remove_tkwin(self)  # Tell the parent that we have closed.


class TkBackend(GraphicsBackendBase):
    def __init__(self):
        self._root = tk.Tk()  # A wrapper around a new Tcl interpreter.
        self._root.withdraw()  # Removes the window from the screen (without destroying it).

        atexit.register(self._root.mainloop)  # TODO(sredmond): For debugging only.
        self._windows = []  # TODO(sredmond): Use winfo_children().

    def _update_active_window(self, window):
        # Optimization: Don't mess with the windows when there's only one.
        if len(self._windows) == 1: return

        window._master.lift()

        # Move the window to top of the stack.
        self._windows.remove(window)
        self._windows.append(window)

    def _remove_tkwin(self, window):
        if not window._closed:
            window._close()

        try:
            self._windows.remove(window)
        except ValueError:
            pass

        if not self._windows:
            self._shutdown()

    def _shutdown(self):
        self._root.destroy()

    ######################
    # GWindow lifecycle. #
    ######################
    def gwindow_constructor(self, gwindow, width, height, top_compound, visible=True):
        gwindow._tkwin = TkWindow(self._root, width, height, parent=self)
        gwindow._tkwin._gwindow = gwindow  # Circular reference so a TkWindow knows its originating GWindow.

        self._windows.append(gwindow._tkwin)

        # HACK: Get nice titles built in.
        self.gwindow_set_window_title(gwindow, gwindow.title)

    def gwindow_close(self, gwindow):
        self._remove_tkwin(gwindow._tkwin)

    def gwindow_delete(self, gwindow):
        self._remove_tkwin(gwindow._tkwin)

    def gwindow_exit_graphics(self):
        self._remove_tkwin(gwindow._tkwin)

    def gwindow_set_exit_on_close(self, gwindow, exit_on_close): pass

    ####################
    # GWindow drawing. #
    ####################
    def gwindow_clear(self, gwindow):
        self._update_active_window(gwindow._tkwin)
        gwindow._tkwin.clear()

    def gwindow_clear_canvas(self, gwindow):
        self._update_active_window(gwindow._tkwin)
        gwindow._tkwin.clear_canvas()

    def gwindow_repaint(self, gwindow):
        # Update any unresolved tasks.
        gwindow._tkwin._master.update_idletasks()

    def gwindow_draw(self, gwindow, gobject): pass

    ####################
    # GWindow drawing. #
    ####################
    def gwindow_request_focus(self, gwindow):
        self._update_active_window(gwindow._tkwin)
        gwindow._tkwin._master.focus_force()

    def gwindow_set_visible(self, gwindow, flag):
        self._update_active_window(gwindow._tkwin)
        if flag:  # Show the window.
            gwindow._tkwin._master.deiconify()
        else:  # Show the window.
            gwindow._tkwin._master.withdraw()

    def gwindow_set_window_title(self, gwindow, title):
        self._update_active_window(gwindow._tkwin)
        gwindow._tkwin._master.title(title)

    def gwindow_get_width(self):
        self._update_active_window(gwindow._tkwin)
        return gwindow._tkwin._master.geometry()[0]

    def gwindow_get_height(self):
        self._update_active_window(gwindow._tkwin)
        return gwindow._tkwin._master.geometry()[1]

    ######################
    # GWindow alignment. #
    ######################
    def gwindow_add_to_region(self, gwindow, gobject, region):
        from campy.graphics.gwindow import Region
        if region == Region.NORTH:
            self._ginteractor_add(gobject, gwindow._tkwin.top)
        if region == Region.EAST:
            self._ginteractor_add(gobject, gwindow._tkwin.right)
        if region == Region.SOUTH:
            self._ginteractor_add(gobject, gwindow._tkwin.bottom)
        if region == Region.WEST:
            self._ginteractor_add(gobject, gwindow._tkwin.left)

    def gwindow_remove_from_region(self, gwindow, gobject, region): pass
    def gwindow_set_region_alignment(self, gwindow, region, align): pass

    ##############################
    # Shared GObject operations. #
    ##############################
    def gobject_set_location(self, gobject, x, y):
        if not hasattr(gobject, '_tkid'): return

        tkid = gobject._tkid
        win = gobject._tkwin

        coords = win.canvas.coords(tkid)
        win.canvas.move(tkid, x - coords[0], y - coords[1])
        win._master.update_idletasks()

    def gobject_set_filled(self, gobject, flag):
        from campy.graphics.gobjects import GArc
        if not hasattr(gobject, '_tkid'): return

        tkid = gobject._tkid
        win = gobject._tkwin
        if flag:
            win.canvas.itemconfig(tkid, fill=gobject.fill_color.hex)
            if isinstance(object, GArc):
                win.canvas.itemconfig(tkid, style=tk.PIESLICE)
        else:
            win.canvas.itemconfig(tkid, fill='')
            if isinstance(object, GArc):
                self.itemconfig(tkid, style=tkinter.ARC)

        win._master.update_idletasks()

    def gobject_remove(self, gobject):
        if not hasattr(gobject, '_tkid'): return
        tkid = gobject._tkid
        win = gobject._tkwin

        win.canvas.delete(tkid)
        delattr(gobject, '_tkid')
        delattr(gobject, '_tkwin')

        win._master.update_idletasks()

    def gobject_set_color(self, gobject, color):
        if not hasattr(gobject, '_tkid'): return
        tkid = gobject._tkid
        win = gobject._tkwin

        # Awkward import.
        from campy.graphics.gobjects import GLabel, GLine
        if not isinstance(gobject, GLabel) and not isinstance(gobject, GLine):
            win.canvas.itemconfig(tkid, outline=color.hex)
        else:
            # GLabels and GLines are special because their "color" is actually a fill color.
            win.canvas.itemconfig(tkid, fill=color.hex)

        win._master.update_idletasks()

    def gobject_set_fill_color(self, gobject, color):
        if not hasattr(gobject, '_tkid'): return
        tkid = gobject._tkid
        win = gobject._tkwin

        win.canvas.itemconfig(tkid, fill=color.hex)

        win._master.update_idletasks()

    def gobject_send_forward(self, gobject): pass
    def gobject_send_to_front(self, gobject):
        if not hasattr(gobject, '_tkid'): return
        tkid = gobject._tkid
        win = gobject._tkwin

        win.canvas.tag_raise(tkid)

        win._master.update_idletasks()

    def gobject_send_backward(self, gobject): pass
    def gobject_send_to_back(self, gobject):
        if not hasattr(gobject, '_tkid'): return
        tkid = gobject._tkid
        win = gobject._tkwin

        win.canvas.tag_lower(tkid)

        win._master.update_idletasks()

    def gobject_set_size(self, gobject, width, height): pass
    def gobject_get_size(self, gobject):
        if not hasattr(gobject, '_tkid'): return
        tkid = gobject._tkid
        win = gobject._tkwin

        x0, y0, x1, y1 = win.canvas.bbox(tkid)
        return x1 - x0, y1 - y0

    def gobject_get_bounds(self, gobject): pass
    def gobject_set_line_width(self, gobject, line_width): pass
    def gobject_contains(self, gobject, x, y): pass
    def gobject_set_visible(self, gobject, flag):
        if not hasattr(gobject, '_tkid'): return
        tkid = gobject._tkid
        win = gobject._tkwin

        if not flag:
            win.canvas.itemconfig(tkid, state=tk.HIDDEN)
        else:
            win.canvas.itemconfig(tkid, state=tk.NORMAL)

    def gobject_scale(self, gobject, sx, sy): pass
    def gobject_rotate(self, gobject, theta): pass

    ########################
    # Rectangular regions. #
    ########################
    def grect_constructor(self, grect):
        if hasattr(grect, '_tkwin'):
            return

        win = self._windows[-1]
        grect._tkwin = win

        grect._tkid = win.canvas.create_rectangle(
            grect.x, grect.y, grect.x + grect.width, grect.y + grect.height,
            outline=grect.color.hex, fill=grect.fill_color.hex if grect.filled else '',
            state=tk.NORMAL if grect.visible else tk.HIDDEN)
        win._master.update_idletasks()

    def groundrect_constructor(self, gobject, width, height, corner): pass
    def g3drect_constructor(self, gobject, width, height, raised): pass
    def g3drect_set_raised(self, gobject, raised): pass

    #######################
    # Elliptical regions. #
    #######################
    def goval_constructor(self, goval):
        if hasattr(goval, '_tkwin'):
            return

        win = self._windows[-1]
        goval._tkwin = win

        goval._tkid = win.canvas.create_oval(
            goval.x, goval.y, goval.x + goval.width, goval.y + goval.height,
            outline=goval.color.hex, fill=goval.fill_color.hex if goval.filled else '',
            state=tk.NORMAL if goval.visible else tk.HIDDEN)

        win._master.update_idletasks()

    def garc_constructor(self, garc):
        if hasattr(garc, '_tkwin'):
            return

        win = self._windows[-1]
        garc._tkwin = win

        garc._tkid = win.canvas.create_arc(
            garc.x, garc.y, garc.x + garc.width, garc.y + garc.height,
            start=garc.start, extent=garc.sweep,
            outline=garc.color.hex, fill=garc.fill_color.hex if garc.filled else '',
            style=tk.PIESLICE if garc.filled else tk.ARC,
            state=tk.NORMAL if garc.visible else tk.HIDDEN)

        win._master.update_idletasks()

    def garc_set_start_angle(self, garc, angle):
        if not hasattr(garc, '_tkid'): return
        tkid = garc._tkid
        win = garc._tkwin

        win.canvas.itemconfig(tkid, start=angle)

        win._master.update_idletasks()

    def garc_set_sweep_angle(self, garc, angle):
        if not hasattr(garc, '_tkid'): return
        tkid = garc._tkid
        win = garc._tkwin

        win.canvas.itemconfig(tkid, extent=angle)

        win._master.update_idletasks()

    def garc_set_frame_rectangle(self, garc, x, y, width, height): pass


    ##########
    # GLines #
    ##########
    def gline_constructor(self, gline):
        if hasattr(gline, '_tkwin'):
            return

        win = self._windows[-1]
        gline._tkwin = win

        gline._tkid = win.canvas.create_line(
            gline.start.x, gline.start.y, gline.end.x, gline.end.y,
            fill=gline.color.hex,
            state=tk.NORMAL if gline.visible else tk.HIDDEN)

        win._master.update_idletasks()

    def gline_set_start_point(self, gline, x, y):
        if not hasattr(gline, '_tkid'): return
        tkid = gline._tkid
        win = gline._tkwin

        win.canvas.coords(tkid, x, y, gline.end.x, gline.end.y,)

        win._master.update_idletasks()

    def gline_set_end_point(self, gline, x, y):
        if not hasattr(gline, '_tkid'): return
        tkid = gline._tkid
        win = gline._tkwin

        win.canvas.coords(tkid, gline.start.x, gline.start.y, x, y)

        win._master.update_idletasks()

    ##############
    # GCompounds #
    ##############
    def gcompound_constructor(self, gobject): pass
    def gcompound_add(self, compound, gobject): pass

    #########
    # Fonts #
    #########
    # See: https://www.astro.princeton.edu/~rhl/Tcl-Tk_docs/tk/font.n.html

    def gfont_default_attributes(self):
        # Resolves to the platform-specific default.
        font = tkfont.nametofont('TkDefaultFont')
        return font.config()

    def gfont_attributes_from_system_name(self, font_name):
        # Attempt to load the font with the given name.
        font = tkfont.nametofont(font_name)
        return font.config()

    def gfont_get_font_metrics(self, gfont):
        font = tkfont.Font(family=gfont.family, size=gfont.size,
                           weight=tkfont.BOLD if gfont.weight else tkfont.NORMAL,
                           slant=tkfont.ITALIC if gfont.slant else tkfont.ROMAN)
        if not hasattr(gfont, '_tkfont'):
            gfont._tkfont = font
        return font.metrics()

    def gfont_measure_text_width(self, gfont, text):
        if not hasattr(gfont, '_tkfont'):
            gfont._tkfont = tkfont.Font(family=gfont.family, size=gfont.size,
                            weight=tkfont.BOLD if gfont.weight else tkfont.NORMAL,
                            slant=tkfont.ITALIC if gfont.slant else tkfont.ROMAN)
        font = gfont._tkfont
        return font.measure(text)

    ##########
    # Labels #
    ##########
    def glabel_constructor(self, glabel):
        if hasattr(glabel, '_tkwin'):
            return

        win = self._windows[-1]
        glabel._tkwin = win

        # TODO(sredmond): Document that we're putting the anchor at the NW corner.
        # TODO(sredmond): Respect the font that's been set.
        glabel._tkid = win.canvas.create_text(
            glabel.x, glabel.y,
            text=glabel.text,
            fill=glabel.color.hex, anchor=tk.SW,
            state=tk.NORMAL if glabel.visible else tk.HIDDEN)

        self.glabel_set_font(glabel, glabel.font)

        win._master.update_idletasks()

    def glabel_set_font(self, glabel, gfont):
        if not hasattr(glabel, '_tkid'): return

        if not hasattr(gfont, '_tkfont'):
            gfont._tkfont = tkfont.Font(family=gfont.family, size=gfont.size,
                            weight=tkfont.BOLD if gfont.weight else tkfont.NORMAL,
                            slant=tkfont.ITALIC if gfont.slant else tkfont.ROMAN)
        font = gfont._tkfont
        tkid = glabel._tkid
        win = glabel._tkwin
        win.canvas.itemconfig(tkid, font=font)

    def glabel_set_label(self, glabel, text):
        if not hasattr(glabel, '_tkid'): return
        tkid = glabel._tkid
        win = glabel._tkwin

        win.canvas.itemconfig(tkid, text=text)

    def glabel_get_font_ascent(self, glabel): pass
    def glabel_get_font_descent(self, glabel): pass
    def glabel_get_size(self, glabel):
        # TODO(sredmond): This is currently broken.
        if not hasattr(glabel, '_tkid'): return 0, 0
        tkid = glabel._tkid
        win = glabel._tkwin

        x0, y0, x1, y1 = win.canvas.bbox(tkid)
        return x1 - x0, y1 - y0

    # Polygons
    def gpolygon_constructor(self, gpolygon):
        if hasattr(gpolygon, '_tkwin'):
            return

        win = self._windows[-1]
        gpolygon._tkwin = win

        coords = sum(((v.x + gpolygon.x, v.y + gpolygon.y) for v in gpolygon.vertices), ())
        gpolygon._tkid = win.canvas.create_polygon(coords,  # Not the fastest, but it'll do
            outline=gpolygon.color.hex, fill=gpolygon.fill_color.hex if gpolygon.filled else '',
            state=tk.NORMAL if gpolygon.visible else tk.HIDDEN)

        win._master.update_idletasks()

    def gpolygon_add_vertex(self, gpolygon, x, y):
        if not hasattr(gpolygon, '_tkid'): return
        tkid = gpolygon._tkid
        win = gpolygon._tkwin

        win.canvas.coords(tkid, x, y, gpolygon.end.x, gpolygon.end.y,)

        win._master.update_idletasks()

    ##########
    # Images #
    ##########
    def image_find(self, filename):
        # TODO(sredmond): Couple image file searching and image file loading.
        path = pathlib.Path(filename)
        if path.is_absolute():
            if path.is_file():
                return path
            return None


        # For relative paths, search for images in the following places.
        # (1) The actual relative path to the scripts current directory.
        # (1) An `images/` subfolder in the scripts current directory.
        # TODO(sredmond): Read in a path environmental variable for searching.
        if path.is_file():
            return path.resolve()  # We found it, even though it's relative!
        if (path.parent / 'images' / path.name).is_file():
            return (path.parent / 'images' / path.name).resolve()
        # TODO(sredmond): Also search through library-specific images.
        return None

    def image_load(self, filename):
        try:
            from PIL import Image
            logger.info('Loading image using PIL.')
            im = Image.open(filename)
            im = im.convert('RGB')  # This is an unfortunate conversion, in that it kills transparent images.
            return im, im.width, im.height
        except ImportError:
            im = tk.PhotoImage(file=gimage._path)
            return im, im.width(), im.height()

    def gimage_constructor(self, gimage):
        """Try to create some sort of Tk Photo Image."""
        if hasattr(gimage, '_tkwin'):
            return

        win = self._windows[-1]
        gimage._tkwin = win

        image = gimage._data  # Either a tk.PhotoImage or a PIL.Image
        # This is an awkward state, since ImageTk.PhotoImage isn't a subclass.
        if not isinstance(image, tk.PhotoImage):
            image = PhotoImage(image=image)

        gimage._tkid = win.canvas.create_image(
            gimage.x, gimage.y, anchor=tk.NW, image=image)

        # Keep a reference to the PhotoImage object so that the Python GC
        # doesn't destroy the data.
        gimage._tkim = image

        win._master.update_idletasks()

    def gimage_blank(self, gimage, width, height): pass
    def gimage_get_pixel(self, gimage, row, col):
        from campy.graphics.gcolor import Pixel
        try:
            # Using Tk.PhotoImage.
            value = gimage._data.get(col, row)
            return Pixel(*value.split(' '))  # TODO(sredmond): Make sure Tk always returns 'r g b' and not 'a' or a single channel.
        except AttributeError:  # No get method on ImageTk.PhotoImage.
            value = gimage._data.getpixel((col, row))  # Should be an (r, g, b) tuple
            return Pixel(*value)


    def gimage_set_pixel(self, gimage, row, col, rgb):
        try: # Default to using PIL
            gimage._data.putpixel((col, row), rgb)
            # Oh no... Look at this abuse of Python. This is the type of thing they warn you about in school.
            # TODO(sredmond): Move this into the hex method of colors.
            r, g, b = rgb
            hexcolor = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            gimage._tkim._PhotoImage__photo.put(hexcolor, (col, row))
        except AttributeError:  # No putpixel in Tk, so try to fall back.
            r, g, b = rgb
            hexcolor = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            gimage._tkim.put(hexcolor, (col, row))

    def gimage_preview(self, gimage): pass



    ##########
    # Events #
    ##########
    def set_action_command(self, gobject, cmd): pass
    def get_next_event(self, mask): pass
    def wait_for_event(self, mask): pass

    def event_add_keypress_handler(self, event, handler): pass
    def event_generate_keypress(self, event): pass

    @staticmethod
    def _wrap_mouse_event(event, window, event_type):
        from campy.gui.events.mouse import GMouseEvent
        # TODO(sredmond): As written, this joins the TkWindow, not the GWindow, to this event.
        return GMouseEvent(event_type=event_type, gwindow=window._gwindow, x=event.x, y=event.y)

    def event_add_mouse_handler(self, event, handler):
        from campy.gui.events.mouse import MouseEventType
        if not self._windows:
            logger.warning('Refusing to add a mouse listener before any windows are created.')
            return

        win = self._windows[-1]

        if event == MouseEventType.MOUSE_CLICKED:
            win._master.bind('<Button-1>', lambda cb_event: handler(self._wrap_mouse_event(cb_event, win, event)))
        elif event == MouseEventType.MOUSE_RELEASED:
            win._master.bind('<ButtonRelease-1>', lambda cb_event: handler(self._wrap_mouse_event(cb_event, win, event)))
        elif event == MouseEventType.MOUSE_MOVED:
            win._master.bind('<Motion>', lambda cb_event: handler(self._wrap_mouse_event(cb_event, win, event)))
        elif event == MouseEventType.MOUSE_DRAGGED:
            win._master.bind('<B1-Motion>', lambda cb_event: handler(self._wrap_mouse_event(cb_event, win, event)))
        else:
            logger.warning('Unrecognized event type: {}. Quietly passing.'.format(event))

    def event_generate_mouse(self, event): pass

    @staticmethod
    def _wrap_window_event(event, window):
        from campy.gui.events.window import GWindowEvent
        return GWindowEvent(window._gwindow, x=event.x, y=event.y, width=event.width, height=event.height)

    def event_add_window_changed_handler(self, handler):
        if not self._windows:
            logger.warning('Refusing to add a window listener before any windows are created.')
            return

        win = self._windows[-1]
        win._master.bind('<Configure>', lambda cb_event: handler(self._wrap_window_event(cb_event, win)))

    def event_set_window_closed_handler(self, handler):
        # TODO(sredmond): Don't allow this method to set a handler multiple times, or warn about replacing the old one.
        if not self._windows:
            logger.warning('Refusing to add a window listener before any windows are created.')
            return

        win = self._windows[-1]
        @functools.wraps(handler)
        def wrapper():
            result = handler()

            # Perform the default action when the handler returns a False value.
            if not result:
                win._close()

        # Unlike some of the other event methods, this callback is bound via protocol.
        win._master.protocol("WM_DELETE_WINDOW", wrapper)


    def event_pump_one(self):
        # Forcibly process queued tasks, but don't process newly queued ones.
        self._root.update_idletasks()
        self._root.dooneevent(DONT_WAIT)

    # TODO(sredmond): Rename these backend events for consistency.
    def timer_pause(self, event): pass
    def timer_schedule(self, function, delay_ms):
        self._root.after(delay_ms, function)


    ###############
    # Interactors #
    ###############
    def _ginteractor_add(self, gint, frame):
        from campy.gui.ginteractors import GButton
        if isinstance(gint, GButton):
            # TODO(sredmond): Wrap up a GActionEvent on the Tk side to supply.
            gint._tkobj = tk.Button(frame, text=gint.label, command=gint.click,
            state=tk.NORMAL if not gint.disabled else tk.DISABLED)
        gint._tkobj.pack()

        frame.update_idletasks()

    def gbutton_constructor(self, gbutton):
        if hasattr(gbutton, '_tkwin'):
            return

        win = self._windows[-1]
        gbutton._tkwin = win

    def gbutton_set_label(self, gbutton):
        if not hasattr(gbutton, '_tkobj'): return
        gbutton._tkobj.config(text=gbutton.label)

    def gbutton_set_disabled(self, gbutton):
        if not hasattr(gbutton, '_tkobj'): return
        gbutton._tkobj.config(state=tk.NORMAL if not gbutton.disabled else tk.DISABLED)

    def gcheckbox_constructor(self, gcheckbox):
        if hasattr(gcheckbox, '_tkwin'):
            return

        win = self._windows[-1]
        gcheckbox._tkwin = win

        # TODO(sredmond): Wrap up a GActionEvent on the Tk side to supply.
        var = tkinter.IntVar()
        gcheckbox._tkobj = tk.Checkbutton(win._master, text=gcheckbox.label, command=gcheckbutton.select,
            variable=var,
            state=tk.NORMAL if not gcheckbox.disabled else tk.DISABLED)
        gcheckbox._tkobj.var = var
        gcheckbox._tkobj.pack()

        win._master.update_idletasks()


    def gcheckbox_is_selected(self, gcheckbox):
        return bool(gcheckbox._tkobj.var.get())

    def gcheckbox_set_selected(self, gcheckbox, state):
        return gcheckbox._tkobj.var.set(1 if state else 0)

    def gslider_constructor(self, gslider, min, max, value): pass
    def gslider_get_value(self, gslider): pass
    def gslider_set_value(self, gslider, value): pass
    def gtextfield_constructor(self, gtextfield, num_chars): pass
    def gtextfield_get_text(self, gtextfield): pass
    def gtextfield_set_text(self, gtextfield, str): pass
    def gchooser_constructor(self, gchooser): pass
    def gchooser_add_item(self, gchooser, item): pass
    def gchooser_get_selected_item(self, gchooser): pass
    def gchooser_set_selected_item(self, gchooser, item): pass

    ###########
    # Dialogs #
    ###########
    # TODO(sredmond): Make these dialogs steal focus.
    def gfilechooser_show_open_dialog(self, current_dir, file_filter):
        logger.debug('Ignoring file_filter argument to gfilechooser_show_open_dialog.')
        parent = None
        if self._windows:
            parent=self._windows[-1]
        return tkfiledialog.askopenfilename(initialdir=current_dir, title='Select File to Open', parent=parent) or None

    def gfilechooser_show_save_dialog(self, current_dir, file_filter):
        logger.debug('Ignoring file_filter argument to gfilechooser_show_save_dialog.')
        parent = None
        if self._windows:
            parent=self._windows[-1]
        return tkfiledialog.asksaveasfilename(initialdir=current_dir, title='Select File to Save', parent=parent) or None

    def goptionpane_show_confirm_dialog(self, message, title, confirm_type):
        from campy.graphics.goptionpane import ConfirmType

        if confirm_type == ConfirmType.YES_NO:
            return tkmessagebox.askyesno(title, message)
        elif confirm_type == ConfirmType.YES_NO_CANCEL:
            return tkmessagebox.askyesnocancel(title, message)
        elif confirm_type == ConfirmType.OK_CANCEL:
            return tkmessagebox.askokcancel(title, message)
        else:
            logger.debug('Unrecognized confirm_type {!r}'.format(confirm_type))

    def goptionpane_show_input_dialog(self, message, title):
        return tksimpledialog.askstring(title, message, parent=self._root)

    def goptionpane_show_message_dialog(self, message, title, message_type):
        from campy.graphics.goptionpane import MessageType

        # TODO(sredmond): The icons aren't appearing correctly.
        if message_type == MessageType.ERROR:
            tkmessagebox.showerror(title, message, icon=tkmessagebox.ERROR)
        elif message_type == MessageType.INFORMATION:
            tkmessagebox.showinfo(title, message, icon=tkmessagebox.INFO)
        elif message_type == MessageType.WARNING:
            tkmessagebox.showwarning(title, message, icon=tkmessagebox.WARNING)
        elif message_type == MessageType.QUESTION:
            tkmessagebox.showinfo(title, message, icon=tkmessagebox.QUESTION)
        elif message_type == MessageType.PLAIN:
            tkmessagebox.showinfo(title, message)
        else:
            logger.debug('Unrecognized message_type {!r}'.format(message_type))

    def goptionpane_show_option_dialog(self, message, title, options, initially_selected): pass
    def goptionpane_show_text_file_dialog(self, message, title, rows, cols): pass

if __name__ == '__main__':
    # Quick tests.
    from campy.graphics.gwindow import GWindow
    from campy.graphics.gobjects import GRect, GPolygon
    from campy.graphics.gfilechooser import show_open_dialog, show_save_dialog
    from campy.graphics.goptionpane import *
    from campy.graphics.gtypes import *
    from campy.gui.interactors import *

    import math

    print('{!r}'.format(show_open_dialog()))
    print('{!r}'.format(show_save_dialog()))


    window = GWindow()
    rect = GRect(100, 200, x=50, y=60)
    window.add(rect)
    rect.location = 300, 300
    button = GButton('Button')
    window.add(button)

    # Add a polygon.
    edge_length = 75
    stop_sign = GPolygon()
    start = GPoint(-edge_length / 2, edge_length / 2 + edge_length / math.sqrt(2.0))
    stop_sign.add_vertex(start)
    for edge in range(8):
        stop_sign.add_polar_edge(edge_length, 45*edge)
    stop_sign.filled = True
    stop_sign.color = "BLACK"
    stop_sign.fill_color = "RED"
    window.add(stop_sign, window.width / 2, window.height / 2)

