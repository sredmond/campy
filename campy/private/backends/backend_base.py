"""Common abstract base classes for various backends.

There are three different types of backends.

- GraphicsBackendBase: Everything graphical - windows, canvas objects, labels, interactors.
- AudioBackendBase: Everything auditory - creating and playing sounds.
- ConsoleBackendBase: Everything textual - fonts and lines.

The Tk backend is a graphical backend only. The Java backend is all three.

Other implementations of `ConsoleBackendBase` have been spun out into their own
library `popup-console`.

These abstract base classes are provided for backend developers to see which
methods their backend will need to support. It is considered under development
and can change at any time.
"""
import abc

class GraphicsBackendBase(abc.ABC):
    """Interface for graphical backends."""
    # TODO(sredmond): Decorate all of these classes with @abc.abstractmethod.
    # For now, the interlaced decorators make the interface too hard to read.

    # GWindow lifecycle.
    def gwindow_constructor(self, gwindow, width, height, top_compound, visible=True): pass
    def gwindow_close(self, gwindow): pass
    def gwindow_delete(self, gwindow): pass
    def gwindow_set_exit_on_close(self, gwindow, exit_on_close): pass
    def gwindow_exit_graphics(self): pass

    # GWindow drawing.
    def gwindow_clear(self, gwindow): pass
    def gwindow_clear_canvas(self, gwindow): pass
    def gwindow_repaint(self, gwindow): pass
    def gwindow_draw(self, gwindow, gobject): pass

    # GWindow attributes.
    def gwindow_request_focus(self, gwindow): pass
    def gwindow_set_visible(self, gwindow, flag): pass
    def gwindow_set_window_title(self, gwindow, title): pass
    def gwindow_get_width(self): pass
    def gwindow_get_height(self): pass

    # GWindow geometry.
    def gwindow_add_to_region(self, gwindow, gobject, region): pass
    def gwindow_remove_from_region(self, gwindow, gobject, region): pass
    def gwindow_set_region_alignment(self, gwindow, region, align): pass

    # Shared GObject operations.
    def gobject_set_location(self, gobject, x, y): pass
    def gobject_set_filled(self, gobject, flag): pass
    def gobject_remove(self, gobject): pass
    def gobject_set_color(self, gobject, color): pass
    def gobject_set_fill_color(self, gobject, color): pass
    def gobject_send_forward(self, gobject): pass
    def gobject_send_to_front(self, gobject): pass
    def gobject_send_backward(self, gobject): pass
    def gobject_send_to_back(self, gobject): pass
    def gobject_set_size(self, gobject, width, height): pass
    def gobject_get_size(self, gobject): pass
    def gobject_get_bounds(self, gobject): pass
    def gobject_set_line_width(self, gobject, line_width): pass
    def gobject_contains(self, gobject, x, y): pass
    def gobject_set_visible(self, gobject, flag): pass
    def gobject_scale(self, gobject, sx, sy): pass
    def gobject_rotate(self, gobject, theta): pass

    # Rectangular regions
    def grect_constructor(self, grect): pass
    def groundrect_constructor(self, gobject, width, height, corner): pass
    def g3drect_constructor(self, gobject, width, height, raised): pass
    def g3drect_set_raised(self, gobject, raised): pass

    # Elliptical regions
    def goval_constructor(self, gobject): pass
    def garc_constructor(self, gobject, width, height, start, sweep): pass
    def garc_set_start_angle(self, gobject, angle): pass
    def garc_set_sweep_angle(self, gobject, angle): pass
    def garc_set_frame_rectangle(self, gobject, x, y, width, height): pass

    # GLines
    def gline_constructor(self, gobject, x1, y1, x2, y2): pass
    def gline_set_start_point(self, gobject, x, y): pass
    def gline_set_end_point(self, gobject, x, y): pass

    # Compounds
    def gcompound_constructor(self, gobject): pass
    def gcompound_add(self, compound, gobject): pass

    # Labels
    def glabel_constructor(self, gobject, label): pass
    def glabel_set_font(self, gobject, font): pass
    def glabel_set_label(self, gobject, str): pass
    def glabel_get_font_ascent(self, gobject): pass
    def glabel_get_font_descent(self, gobject): pass
    def glabel_get_size(self, gobject): pass

    # Polygons
    def gpolygon_constructor(self, gobject): pass
    def gpolygon_add_vertex(self, gobject, x, y): pass

    # Timers
    def gtimer_constructor(self, timer, millis): pass
    def gtimer_delete(self, timer): pass
    def gtimer_start(self, timer): pass
    def gtimer_pause(self, millis): pass
    def gtimer_stop(self, timer): pass

    # Images
    def gimage_constructor(self, gobject,  filename): pass

    def gbufferedimage_constructor(self, gobject, x, y, width, height): pass
    def gbufferedimage_fill(self, gobject, rgb): pass
    def gbufferedimage_fill_region(self, gobject, x, y, width, height, rgb): pass
    def gbufferedimage_load(self, gobject, filename): pass
    def gbufferedimage_resize(self, gobject, width, height, retain): pass
    def gbufferedimage_save(self, gobject, filename): pass
    def gbufferedimage_set_rgb(self, gobject, x, y, rgb): pass
    def gbufferedimage_update_all_pixels(self, gobject, base64): pass

    # Events
    def set_action_command(self, gobject, cmd): pass
    def get_next_event(self, mask): pass
    def wait_for_event(self, mask): pass

    # Interactors
    def gbutton_constructor(self, gobject, label): pass
    def gcheckbox_constructor(self, gobject, label): pass
    def gcheckbox_is_selected(self, gobject): pass
    def gcheckbox_set_selected(self, gobject, state): pass
    def gslider_constructor(self, gobject, min, max, value): pass
    def gslider_get_value(self, gobject): pass
    def gslider_set_value(self, gobject, value): pass
    def gtextfield_constructor(self, gobject, num_chars): pass
    def gtextfield_get_text(self, gobject): pass
    def gtextfield_set_text(self, gobject, str): pass
    def gchooser_constructor(self, gobject): pass
    def gchooser_add_item(self, gobject, item): pass
    def gchooser_get_selected_item(self, gobject): pass
    def gchooser_set_selected_item(self, gobject, item): pass

    # Dialogs
    def file_open_file_dialog(self, title, mode, path): pass
    def gfilechooser_show_open_dialog(self, current_dir, file_filter): pass
    def gfilechooser_show_save_dialog(self, current_dir, file_filter): pass
    def goptionpane_show_confirm_dialog(self, message, title, confirm_type): pass
    def goptionpane_show_input_dialog(self, message, title): pass
    def goptionpane_show_message_dialog(self, message, title, message_type): pass
    def goptionpane_show_option_dialog(self, message, title, options, initially_selected): pass
    def goptionpane_show_text_file_dialog(self, message, title, rows, cols): pass


class ConsoleBackendBase(abc.ABC):
    """Interface for console backends."""

    @abc.abstractmethod
    def clear_console(self): pass
    @abc.abstractmethod
    def set_console_font(self, font): pass
    @abc.abstractmethod
    def set_console_size(self, console_size): pass
    @abc.abstractmethod
    def get_console_line(self): pass
    @abc.abstractmethod
    def put_console(self, line, stderr=False): pass
    @abc.abstractmethod
    def echo_console(self): pass
    @abc.abstractmethod
    def end_line_console(self): pass


class AudioBackendBase(abc.ABC):
    """Interface for audio backends."""

    # Sounds
    @abc.abstractmethod
    def create_sound(self, sound, *args): pass
    @abc.abstractmethod
    def delete_sound(self, sound, *args): pass
    @abc.abstractmethod
    def play_sound(self, sound, *args): pass

    # Notes
    @abc.abstractmethod
    def play_note(self, note, repeat): pass
