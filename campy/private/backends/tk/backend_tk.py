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
from campy.private.backends.tk.menu import setup_menubar

import atexit
import logging
import tkinter as tk
import tkinter.font as tkfont
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmessagebox
import tkinter.simpledialog as tksimpledialog
import threading
import sys

# Module-level logger.
logger = logging.getLogger(__name__)

# class TkCanvas(tkinter.Canvas):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.objects = {}  # Mapping from GObjects to tkids.
#         # Who cleans this up when Python deletes and object?

#     def set_location(self, obj, x, y):
#         tkid = self.objects[id(obj)]
#         coords = self.coords(tkid)
#         # TODO(sredmond): pgl has an additional term here.
#         self.move(tkid, x - coords[0], y - coords[1])

#     def add_rect(self, rect, x0, y0, x1, y1):
#         # **options??
#         self.objects[id(rect)] = self.create_rectangle(x0, y0, x1, y1)

#     def add_oval(self, oval, x0, y0, x1, y1):
#         self.objects[id(oval)] = self.create_oval(x0, y0, x1, y1)

#     def add_arc(self, arc, x0, y0, x1, y1, start, extent):
#         self.objects[id(arc)] = self.create_arc(x0, y0, x1, y1, start=start, extent=extent)

#     def add_label(self, label):
#         # TODO(sredmond): Make GLabels get added by upper-left coordiante.
#         print('adding label')
#         self.objects[id(label)] = self.create_text(label._x, label._y, text=label.label, anchor=tkinter.SW)



# class TkBackend(GraphicsBackendBase):
#     def __init__(self):
#         self.root = tkinter.Tk()

#         self.root.wm_attributes("-transparent", True)

#         # # TODO(sredmond): I don't think this is cross-platform.
#         # self.root.wm_attributes("-topmost", True)
#         self.root.lift()

#         # _set_menubar(self.root)

#         # TODO(sredmond): Try running mainloop in a different thread.
#         # atexit.register(threading.Thread(target=self.root.mainloop).run)
#         atexit.register(self.root.mainloop)

#         # self.root.protocol("WM_DELETE_WINDOW", sys.exit)

#         # self.root.iconbitmap('icon.ico')
#         # self.root.withdraw()
#          self.root.title("root.title")

#     def gwindow_constructor(self, gw, width, height, top_compound, visible=True):
#         self.canvas = TkCanvas(self.root, width=width, height=height, bd=0, highlightthickness=0)
#         self.canvas.pack(expand=True, fill='both')

#         self.root.update_idletasks()
#         self.root.update()

#         # self.root.update_idletasks()
#         # self.root.update()

#         # TODO(sredmond): Don't just use the default canvas here.
#         top_compound.canvas = self.canvas

#     def gwindow_delete(self, gw):
#         pass

#     def gwindow_draw(self, gw, gobj):
#         import campy.graphics.gobjects as _gobjects
#         if isinstance(gobj, _gobjects.GLine):
#             self._draw_gline(gobj)
#         elif isinstance(gobj, _gobjects.GOval):
#             self._draw_goval(gobj)
#         elif isinstance(gobj, _gobjects.GRect):
#             self._draw_grect(gobj)
#         else:
#             print('Unknown object type.')

# ####################
# # SECTION: Objects #
# ####################

#     def grect_constructor(self, rect, width, height):
#         self.canvas.add_rect(rect, rect.x, rect.y, rect.x + rect.width, rect.y + rect.height)

#     def goval_constructor(self, oval, width, height):
#         self.canvas.add_oval(oval, oval.x, oval.y, oval.x + oval.width, oval.y + oval.height)

#     def garc_constructor(self, arc, width, height, start, sweep):
#         self.canvas.add_arc(arc, arc.x, arc.y, arc.x + width, arc.y + height, start, sweep)

#     # Begin: GObject
#     def gobject_set_location(self, gobj, x, y):
#         self.canvas.set_location(gobj, x, y)


#     def gobject_set_filled(self, gobj, flag):
#         if flag:
#             self.canvas.fill(gobj, gobj.fill_color.hex)
#         else:
#             self.canvas.unfill(gobj)

#     def gobject_set_color(self, gobj, color): pass

#     def gobject_set_fill_color(self, gobj, color):
#         if gobj.filled:
#             self.canvas.fill(gobj, color.hex)

#     def gobject_remove(self, gobj): pass

#     def gobject_send_forward(self, gobj): pass
#     def gobject_send_to_front(self, gobj): pass
#     def gobject_send_backward(self, gobj): pass
#     def gobject_send_to_back(self, gobj): pass
#     def gobject_set_size(self, gobj, width, height): pass
#     def gobject_get_bounds(self, gobj): pass
#     def gobject_set_line_width(self, gobj, line_width): pass
#     def gobject_contains(self, gobj, x, y): pass
#     def gobject_scale(self, gobj, sx, sy): pass
#     def gobject_rotate(self, gobj, theta): pass
#     # End: GObject

#     def _gobject_set_properties(self, gobj):
#         tkid = self.CANVAS_OBJECTS[id(gobj)]
#         self.canvas.itemconfig()

#     def _draw_gline(self, line, **options):
#         # TODO(sredmond): Once updating the line attributes, return to line.x1
#         # TODO(sredmond): Respect the options (e.g. color) attributes of the supplied line.
#         return self.canvas.create_line(line._x0, line._y0, line._x1, line._y1)

#     def _draw_goval(self, oval, **options):
#         x, y, width, height = oval.x, oval.y, oval.width, oval.height
#         # TODO(sredmond): Respect the options (e.g. color, filled) attributes of the supplied line.
#         return self.canvas.create_oval(x, y, x + width, y + height)

#     def _draw_grect(self, rect, **options):
#         x, y, width, height = rect.x, rect.y, rect.width, rect.height
#         # TODO(sredmond): Respect the options (e.g. color, filled) attributes of the supplied line.
#         return self.canvas.create_rectangle(x, y, x + width, y + height)

#     # GLabel
#     def glabel_constructor(self, gobj, label):
#         # self.canvas.add_label(gobj)
#         pass

#     def glabel_set_font(self, gobj, font): pass

#     def glabel_set_label(self, gobj, str): pass

#     def glabel_get_font_ascent(self, gobj):
#         return 10  # placeholder

#     def glabel_get_font_descent(self, gobj):
#         return 3  # placeholder

#     def glabel_get_size(self, gobj): pass

#     # GCompound
#     def gcompound_constructor(self, gobj):
#         """Construct a new GCompound.

#         Python is handling all of our objects, so don't do anything.
#         """
#         pass  # Intentionally empty.


#     def gcompound_add(self, compound, gobj):
#         # TODO(sredmond): This is just a stopgap.
#         from campy.graphics.gobjects import GLabel
#         if isinstance(gobj, GLabel):
#             self.canvas.add_label(gobj)

# ########################
# # SECTION: Interactors #
# ########################
#     def gbutton_constructor(self, button):
#         label = button.label
#         button._tkobj = tkinter.Button(self.root, text=button.label, command=lambda: self.click_button(button))
#         button._tkobj.pack()


#     # TODO(sredmond): This should really be a static method.
#     # @staticmethod
#     def click_button(self, button):
#         if not button.disabled:
#             button.click()

# ####################
# # END: Interactors #
# ####################

# ##########################
# # SECTION: File Choosing #
# ##########################


# ######################
# # END: File Choosing #
# ######################



# def convert_font(font_description):
#     # TODO(sredmond): Don't write bad code anymore!
#     pieces = font_description.split('-')
#     return pieces

class TkWindow:
    def __init__(self, root, width, height, parent):
        self._parent = parent

        self._master = tk.Toplevel(root)
        self._closed = False
        self._master.protocol("WM_DELETE_WINDOW", self._close)
        self._master.resizable(width=False, height=False)  # Disable resizing by default.

        # TODO(sredmond): On macOS, multiple backends might race to set the process-level menu bar.
        setup_menubar(self._master)

        self._frame = tk.Frame(self._master)

        self.canvas = tk.Canvas(self._frame, width=width, height=height, highlightthickness=0, bd=0)
        self.canvas.pack()

        # Raise the master to be the top window.
        self._master.wm_attributes("-topmost", 1)  # TODO(sredmond): Is this really necessary?
        self._master.lift()
        self._master.focus_force()

        self._frame.pack()
        self._frame.update()
        self._master.update()


    def _close(self):
        if self._closed: return

        self._closed = True
        self._master.destroy()
        self._parent._remove_tkwin(self)  # Tell the parent that we have closed.
        # TODO(sredmond): Consider autoflushing like Zelle.

    def _clear(self):
        self._frame.destroy()

        self._frame = tk.Frame(self._master)
        self.canvas = tk.Canvas(self._frame, width=width, height=height, highlightthickness=0, bd=0)
        self.canvas.pack()

    def _clear_canvas(self):
        self.canvas.destroy()

        self.canvas = tk.Canvas(self._frame, width=width, height=height, highlightthickness=0, bd=0)
        self.canvas.pack()

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
        print('in remove tkwin')
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
        self._windows.append(gwindow._tkwin)

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
        gwindow._tkwin._clear()

    def gwindow_clear_canvas(self, gwindow):
        self._update_active_window(gwindow._tkwin)
        gwindow._tkwin._clear_canvas()

    def gwindow_repaint(self, gwindow): pass

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
    def gwindow_add_to_region(self, gwindow, gobject, region): pass
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
            self.itemconfig(tkid, fill='')
            if isinstance(object, GArc):
                self.itemconfig(tkid, style=tkinter.ARC)

        win._master.update_idletasks()

    def gobject_remove(self, gobject):
        if not hasattr(gobject, '_tkid'): return
        tkid = gobject._tkid
        win = gobject._tkwin

        win.canvas.delete(tkid)

        win._master.update_idletasks()

    def gobject_set_color(self, gobject, color):
        if not hasattr(gobject, '_tkid'): return
        tkid = gobject._tkid
        win = gobject._tkwin

        win.canvas.itemconfig(tkid, outline=color.hex)

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
            fill=glabel.color.hex, anchor=tk.NW,
            state=tk.NORMAL if glabel.visible else tk.HIDDEN)

        win._master.update_idletasks()

    def glabel_set_font(self, glabel, font): pass
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
        print(coords)
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

    ###############
    # Interactors #
    ###############
    def gbutton_constructor(self, gbutton):
        if hasattr(gbutton, '_tkwin'):
            return

        win = self._windows[-1]
        gbutton._tkwin = win

        # TODO(sredmond): Wrap up a GActionEvent on the Tk side to supply.
        gbutton._tkobj = tk.Button(win._master, text=gbutton.label, command=gbutton.click,
            state=tk.NORMAL if not gbutton.disabled else tk.DISABLED)
        gbutton._tkobj.pack()

        win._master.update_idletasks()

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

