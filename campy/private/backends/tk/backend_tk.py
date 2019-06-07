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
# It is discouraged to instantiate multiple instances of Tk graphics
from campy.private.backends.backend_base import GraphicsBackendBase

import atexit
import logging
import tkinter
import tkinter.font as tkfont
from tkinter import filedialog
import threading
import sys

# Module-level logger.
logger = logging.getLogger(__name__)

class TkCanvas(tkinter.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.objects = {}  # Mapping from GObjects to tkids.
        # Who cleans this up when Python deletes and object?

    def set_location(self, obj, x, y):
        tkid = self.objects[id(obj)]
        coords = self.coords(tkid)
        # TODO(sredmond): pgl has an additional term here.
        self.move(tkid, x - coords[0], y - coords[1])

    def add_rect(self, rect, x0, y0, x1, y1):
        # **options??
        self.objects[id(rect)] = self.create_rectangle(x0, y0, x1, y1)

    def add_oval(self, oval, x0, y0, x1, y1):
        self.objects[id(oval)] = self.create_oval(x0, y0, x1, y1)

    def add_arc(self, arc, x0, y0, x1, y1, start, extent):
        self.objects[id(arc)] = self.create_arc(x0, y0, x1, y1, start=start, extent=extent)

    def add_label(self, label):
        # TODO(sredmond): Make GLabels get added by upper-left coordiante.
        print('adding label')
        self.objects[id(label)] = self.create_text(label._x, label._y, text=label.label, anchor=tkinter.SW)

    def fill(self, object, fill_color):
        from campy.graphics.gobjects import GArc
        tkid = self.objects[id(object)]
        self.itemconfig(tkid, fill=fill_color)
        if isinstance(object, GArc):
            self.itemconfig(tkid, style=tkinter.PIESLICE)

    def unfill(self, object):
        from campy.graphics.gobjects import GArc
        tkid = self.objects[id(object)]
        self.itemconfig(tkid, fill='')
        if isinstance(object, GArc):
            self.itemconfig(tkid, style=tkinter.ARC)


class TkBackend(GraphicsBackendBase):
    def __init__(self):
        self.root = tkinter.Tk()

        self.root.wm_attributes("-transparent", True)

        # # TODO(sredmond): I don't think this is cross-platform.
        # self.root.wm_attributes("-topmost", True)
        self.root.lift()

        # _set_menubar(self.root)

        # TODO(sredmond): Try running mainloop in a different thread.
        # atexit.register(threading.Thread(target=self.root.mainloop).run)
        atexit.register(self.root.mainloop)

        # self.root.protocol("WM_DELETE_WINDOW", sys.exit)

        # self.root.iconbitmap('icon.ico')
        # self.root.withdraw()
         self.root.title("root.title")

    def gwindow_constructor(self, gw, width, height, top_compound, visible=True):
        self.canvas = TkCanvas(self.root, width=width, height=height, bd=0, highlightthickness=0)
        self.canvas.pack(expand=True, fill='both')

        self.root.update_idletasks()
        self.root.update()

        # self.root.update_idletasks()
        # self.root.update()

        # TODO(sredmond): Don't just use the default canvas here.
        top_compound.canvas = self.canvas

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

####################
# SECTION: Objects #
####################

    def grect_constructor(self, rect, width, height):
        self.canvas.add_rect(rect, rect.x, rect.y, rect.x + rect.width, rect.y + rect.height)

    def goval_constructor(self, oval, width, height):
        self.canvas.add_oval(oval, oval.x, oval.y, oval.x + oval.width, oval.y + oval.height)

    def garc_constructor(self, arc, width, height, start, sweep):
        self.canvas.add_arc(arc, arc.x, arc.y, arc.x + width, arc.y + height, start, sweep)

    # Begin: GObject
    def gobject_set_location(self, gobj, x, y):
        self.canvas.set_location(gobj, x, y)


    def gobject_set_filled(self, gobj, flag):
        if flag:
            self.canvas.fill(gobj, gobj.fill_color.hex)
        else:
            self.canvas.unfill(gobj)

    def gobject_set_color(self, gobj, color): pass

    def gobject_set_fill_color(self, gobj, color):
        if gobj.filled:
            self.canvas.fill(gobj, color.hex)

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
        return self.canvas.create_line(line._x0, line._y0, line._x1, line._y1)

    def _draw_goval(self, oval, **options):
        x, y, width, height = oval.x, oval.y, oval.width, oval.height
        # TODO(sredmond): Respect the options (e.g. color, filled) attributes of the supplied line.
        return self.canvas.create_oval(x, y, x + width, y + height)

    def _draw_grect(self, rect, **options):
        x, y, width, height = rect.x, rect.y, rect.width, rect.height
        # TODO(sredmond): Respect the options (e.g. color, filled) attributes of the supplied line.
        return self.canvas.create_rectangle(x, y, x + width, y + height)

    # GLabel
    def glabel_constructor(self, gobj, label):
        # self.canvas.add_label(gobj)
        pass

    def glabel_set_font(self, gobj, font): pass

    def glabel_set_label(self, gobj, str): pass

    def glabel_get_font_ascent(self, gobj):
        return 10  # placeholder

    def glabel_get_font_descent(self, gobj):
        return 3  # placeholder

    def glabel_get_size(self, gobj): pass

    # GCompound
    def gcompound_constructor(self, gobj):
        """Construct a new GCompound.

        Python is handling all of our objects, so don't do anything.
        """
        pass  # Intentionally empty.


    def gcompound_add(self, compound, gobj):
        # TODO(sredmond): This is just a stopgap.
        from campy.graphics.gobjects import GLabel
        if isinstance(gobj, GLabel):
            self.canvas.add_label(gobj)

########################
# SECTION: Interactors #
########################
    def gbutton_constructor(self, button):
        label = button.label
        button._tkobj = tkinter.Button(self.root, text=button.label, command=lambda: self.click_button(button))
        button._tkobj.pack()


    # TODO(sredmond): This should really be a static method.
    # @staticmethod
    def click_button(self, button):
        if not button.disabled:
            button.click()

####################
# END: Interactors #
####################

##########################
# SECTION: File Choosing #
##########################

    def gfilechooser_show_open_dialog(self, current_dir, file_filter):
        logger.info('Ignoring file_filter argument to gfilechooser_show_open_dialog.')
        return filedialog.askopenfilename(initialdir=current_dir, title='Select File to Open')

    def gfilechooser_show_save_dialog(self, current_dir, file_filter):
        logger.info('Ignoring file_filter argument to gfilechooser_show_save_dialog.')
        return filedialog.asksaveasfilename(initialdir=current_dir, title='Select File to Save')

######################
# END: File Choosing #
######################



def convert_font(font_description):
    # TODO(sredmond): Don't write bad code anymore!
    pieces = font_description.split('-')
    return pieces
