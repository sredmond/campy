"""
This file defines the <code>GFileChooser</code> class which supports
popping up graphical dialog boxes to select file names.

@author sredmond
"""
import campy.private.platform as _platform

class GFileChooser():
    # Constants for dialog types, taken from Java's JFileChooser
    SAVE_DIALOG = 1
    OPEN_DIALOG = 1

    @staticmethod
    def show_open_dialog(current_dir="", file_filter=""):
        return _platform.Platform().gfilechooser_show_open_dialog(current_dir, file_filter)

    @staticmethod
    def show_save_dialog(current_dir="", file_filter=""):
        return _platform.Platform().gfilechooser_show_save_dialog(current_dir, file_filter)
