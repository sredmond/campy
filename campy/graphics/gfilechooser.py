"""Show graphical dialog boxes that ask the user to select a file.

These dialog boxes come in two flavors:

- Open: Select a file to open.
- Save: Select a file to save.

In each case, the filename is returned, or None if the user closed the dialog.
"""
# TODO(sredmond): Reconsider having the empty string returned as a sentinel.
# TODO(sredmond): Add support for additional parameters to the dialogs.
# e.g. defaultextension, title)
import campy.private.platform as _platform

import os


# The current user's home directory, used as the default initial directory.
HOME = os.path.expanduser('~')


def show_open_dialog(directory=HOME):
    """Show the user a dialog asking for a file to open.

    :param directory: The initial directory displayed in the dialog.
    :type directory: pathlib.Path or str
    :return: The filename of the user-selected file, or None if the dialog was cancelled.
    """
    return _platform.Platform().gfilechooser_show_open_dialog(str(directory), file_filter='')


def show_save_dialog(directory=HOME):
    """Show the user a dialog asking for a file to save.

    :param directory: The initial directory displayed in the dialog.
    :type directory: pathlib.Path or str
    :return: The filename of the user-selected file, or None if the dialog was cancelled.
    """
    return _platform.Platform().gfilechooser_show_save_dialog(str(directory), file_filter='')
