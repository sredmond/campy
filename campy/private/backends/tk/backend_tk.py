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
import atexit
import logging
import tkinter
import threading
import sys

from campy.private.backends.backend_base import GraphicsBackendBase

# Module-level logger.
logging.basicConfig()
logger = logging.getLogger(__name__)

class TkCanvas(tkinter.Canvas):
    pass

class TkBackend(GraphicsBackendBase):
    CANVAS_OBJECTS = {}
    def __init__(self):
        self.root = tkinter.Tk()

        self.root.wm_attributes("-transparent", True)

        # TODO(sredmond): I don't think this is cross-platform.
        self.root.wm_attributes("-topmost", True)

        # _set_menubar(self.root)

        # TODO(sredmond): Try running mainloop in a different thread.
        # atexit.register(threading.Thread(target=self.root.mainloop).run)
        atexit.register(self.root.mainloop)

        # self.root.protocol("WM_DELETE_WINDOW", sys.exit)

        # self.root.iconbitmap('icon.ico')
        # self.root.withdraw()
        self.root.title("root.title")

    def gwindow_constructor(self, gw, width, height, top_compound, visible=True):
        self.canvas = tkinter.Canvas(self.root, width=width, height=height, bd=0, highlightthickness=0)
        self.canvas.pack()

        self.root.update_idletasks()
        self.root.update()

        # self.root.update_idletasks()
        # self.root.update()

    def gwindow_delete(self, gw):
        pass

    def gwindow_draw(self, gw, gobj):
        import campy.graphics.gobjects as _gobjects
        if isinstance(gobj, _gobjects.GLine):
            self._draw_gline(gobj)
        elif isinstance(gobj, _gobjects.GOval):
            self._draw_goval(gobj)
        elif isinstance(gobj, _gobjects.GRect):
            self._draw_grect(gobj)
        else:
            print('Unknown object type.')

    def grect_constructor(self, gobj, width, height):
        # self.canvas.create_rectangle(0, 0, width, height, fill='red')
        pass

    # Begin: GObject
    # def gobject_set_location(self, gobj, x, y):
    #     tkid = CANVAS_OBJECTS[id(gobj)]
    #     self.canvas.


    def gobject_set_filled(self, gobj, flag):
        tkid = self.CANVAS_OBJECTS[id(gobj)]

    def gobject_set_color(self, gobj, color): pass

    def gobject_set_fill_color(self, gobj, color): pass

    def gobject_remove(self, gobj): pass

    def gobject_send_forward(self, gobj): pass
    def gobject_send_to_front(self, gobj): pass
    def gobject_send_backward(self, gobj): pass
    def gobject_send_to_back(self, gobj): pass
    def gobject_set_size(self, gobj, width, height): pass
    def gobject_get_bounds(self, gobj): pass
    def gobject_set_line_width(self, gobj, line_width): pass
    def gobject_contains(self, gobj, x, y): pass
    def gobject_scale(self, gobj, sx, sy): pass
    def gobject_rotate(self, gobj, theta): pass
    # End: GObject

    def _gobject_set_properties(self, gobj):
        tkid = self.CANVAS_OBJECTS[id(gobj)]
        self.canvas.itemconfig()

    def _draw_gline(self, line, **options):
        # TODO(sredmond): Once updating the line attributes, return to line.x1
        # TODO(sredmond): Respect the options (e.g. color) attributes of the supplied line.
        return self.canvas.create_line(line.x0, line.y0, line.x0 + line.dx, line.y0 + line.dy)

    def _draw_goval(self, oval, **options):
        x, y, width, height = oval.x, oval.y, oval.width, oval.height
        # TODO(sredmond): Respect the options (e.g. color, filled) attributes of the supplied line.
        return self.canvas.create_oval(x, y, x + width, y + height)

    def _draw_grect(self, rect, **options):
        x, y, width, height = rect.x, rect.y, rect.width, rect.height
        # TODO(sredmond): Respect the options (e.g. color, filled) attributes of the supplied line.
        return self.canvas.create_rectangle(x, y, x + width, y + height)


def _set_menubar(root):
    """Create a menu bar."""
    menubar = tkinter.Menu(root)
    filemenu = tkinter.Menu(menubar, tearoff=0)
    # filemenu.add_command(label="Save As...", command=self.save_as_dialog)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    helpmenu = tkinter.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...", command=lambda: print('About me'))
    menubar.add_cascade(label="Help", menu=helpmenu)
    root.config(menu=menubar)

# _instance = TkBackend()
