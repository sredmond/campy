"""Common base class for all backends.

A backend provides several utilities

"""

class GraphicsBackendBase:
    # GWindow Lifecycle
    def gwindow_constructor(self, gw, width, height, top_compound, visible=True): pass
    def gwindow_close(self, gw): pass
    def gwindow_delete(self, gw): pass
    def gwindow_set_exit_on_close(self, gw, exit_on_close): pass
    def gwindow_exit_graphics(self): pass

    def gwindow_clear(self, gw): pass
    def gwindow_clear_canvas(self, gw, exit_on_close): pass
    def gwindow_add_to_region(self, gw, gobj, region): pass
    def gwindow_request_focus(self, gw): pass
    def gwindow_repaint(self, gw): pass
    def gwindow_set_visible(self, flag, gobj = None, gw = None): pass
    def gwindow_set_window_title(self, gw, title): pass
    def gwindow_get_screen_width(self): pass
    def gwindow_get_screen_height(self): pass
    def gwindow_draw(self, gw, gobj): pass
    def gwindow_set_region_alignment(self, gw, region, align): pass
    def gwindow_remove_from_region(self, gw, gobj, region): pass

    def gobject_set_location(self, gobj, x, y): pass
    def gobject_set_filled(self, gobj, flag): pass
    def gobject_remove(self, gobj): pass
    def gobject_set_color(self, gobj, color): pass
    def gobject_set_fill_color(self, gobj, color): pass
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

    # Rectangular regions
    def grect_constructor(self, gobj, width, height): pass
    def groundrect_constructor(self, gobj, width, height, corner): pass
    def g3drect_constructor(self, gobj, width, height, raised): pass
    def g3drect_set_raised(self, gobj, raised): pass

    # Elliptical regions
    def goval_constructor(self, gobj, width, height): pass
    def garc_constructor(self, gobj, width, height, start, sweep): pass
    def garc_set_start_angle(self, gobj, angle): pass
    def garc_set_sweep_angle(self, gobj, angle): pass
    def garc_set_frame_rectangle(self, gobj, x, y, width, height): pass

    # GLines
    def gline_constructor(self, gobj, x1, y1, x2, y2): pass
    def gline_set_start_point(self, gobj, x, y): pass
    def gline_set_end_point(self, gobj, x, y): pass

    # Compounds
    def gcompound_constructor(self, gobj): pass
    def gcompound_add(self, compound, gobj): pass

    def gimage_constructor(self, gobj,  filename): pass
    def glabel_constructor(self, gobj, label): pass
    def glabel_set_font(self, gobj, font): pass
    def glabel_set_label(self, gobj, str): pass
    def glabel_get_font_ascent(self, gobj): pass
    def glabel_get_font_descent(self, gobj): pass
    def glabel_get_size(self, gobj): pass
    def gpolygon_constructor(self, gobj): pass
    def gpolygon_add_vertex(self, gobj, x, y): pass
    def gtimer_constructor(self, timer, millis): pass
    def gtimer_delete(self, timer): pass
    def gtimer_start(self, timer): pass
    def gtimer_pause(self, millis): pass
    def gtimer_stop(self, timer): pass
    def gbufferedimage_constructor(self, gobj, x, y, width, height): pass
    def gbufferedimage_fill(self, gobj, rgb): pass
    def gbufferedimage_fill_region(self, gobj, x, y, width, height, rgb): pass
    def gbufferedimage_load(self, gobj, filename): pass
    def gbufferedimage_resize(self, gobj, width, height, retain): pass
    def gbufferedimage_save(self, gobj, filename): pass
    def gbufferedimage_set_rgb(self, gobj, x, y, rgb): pass
    def gbufferedimage_update_all_pixels(self, gobj, base64): pass

    def setActionCommand(self, gobj, cmd): pass
    def getSize(self, gobj): pass
    def gbutton_constructor(self, gobj, label): pass
    def gcheckbox_constructor(self, gobj, label): pass
    def gcheckbox_is_selected(self, gobj): pass
    def gcheckbox_set_selected(self, gobj, state): pass
    def gslider_constructor(self, gobj, min, max, value): pass
    def gslider_get_value(self, gobj): pass
    def gslider_set_value(self, gobj, value): pass
    def createGTextField(self, gobj, num_chars): pass
    def getText(self, gobj): pass
    def setText(self, gobj, str): pass
    def createGChooser(self, gobj): pass
    def addItem(self, gobj, item): pass
    def getSelectedItem(self, gobj): pass
    def setSelectedItem(self, gobj, item): pass
    def file_open_file_dialog(self, title, mode, path): pass
    def gfilechooser_show_open_dialog(self, current_dir, file_filter): pass
    def gfilechooser_show_save_dialog(self, current_dir, file_filter): pass
    def goptionpane_show_confirm_dialog(self, message, title, confirm_type): pass
    def goptionpane_show_input_dialog(self, message, title): pass
    def goptionpane_show_message_dialog(self, message, title, message_type): pass
    def goptionpane_show_option_dialog(self, message, title, options, initially_selected): pass
    def goptionpane_show_text_file_dialog(self, message, title, rows, cols): pass

    def getNextEvent(self, mask): pass
    def waitForEvent(self, mask): pass

    def parseEvent(self, line): pass
    def parseMouseEvent(self, tokens, type): pass
    def parseKeyEvent(self, tokens, type): pass
    def parseTimerEvent(self, tokens, type): pass
    def parseWindowEvent(self, tokens, type): pass
    def parseActionEvent(self, tokens, type): pass

    def startupMain(self): pass

class ConsoleBackendBase:
    def clear_console(self):
        pass

    def set_console_font(self, font):
        pass

    def set_console_size(self, console_size):
        pass

    def get_console_line(self):
        pass

    def put_console(self, line, stderr=False):
        pass

    def echo_console(self):
        pass

    def end_line_console(self):
        pass

class SoundBackendBase:
    """A `SoundBackendBase` provides a common API for loading and playing sounds."""

    def create_sound(self, sound, *args):
        pass

    def delete_sound(self, sound, *args):
        pass

    def play_sound(self, sound, *args):
        pass

    def note_play(self, note, repeat):
        pass
