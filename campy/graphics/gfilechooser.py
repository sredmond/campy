"""A :class:`GFileChooser` pops up a graphical dialog boxes to select a file.

These dialog boxes come in two flavors:

- Open Dialog: Select a file to open.
- Save Dialog: Select a file to save.
"""
import campy.private.platform as _platform

# TODO(sredmond): If this class only has static methods, then they should just
# be module-level functions.
class GFileChooser:
    # Constants for dialog types, taken from Java's JFileChooser
    SAVE_DIALOG = 1
    OPEN_DIALOG = 1

    @staticmethod
    def show_open_dialog(current_dir="", file_filter=""):
        return _platform.Platform().gfilechooser_show_open_dialog(current_dir, file_filter)

    @staticmethod
    def show_save_dialog(current_dir="", file_filter=""):
        return _platform.Platform().gfilechooser_show_save_dialog(current_dir, file_filter)
