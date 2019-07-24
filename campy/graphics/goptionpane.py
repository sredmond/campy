"""
This file defines the <code>GOptionPane</code> class which supports
popping up graphical dialog boxes for user input.

This class is inspired by, extremely similar to, and implemented on
the back-end by, Java's JOptionPane class, so you may wish to consult
that class's documentation in the Java API Specification for more
information.
"""
import enum as _enum

import campy.private.platform as _platform
from campy.system.error import error as error

"""Constants for showConfirmDialog types, taken from Java's JOptionPane."""
@_enum.unique
class ConfirmType(_enum.Enum):
    """The three types of confirm dialogs: Yes/No, Yes/No/Cancel, or OK/Cancel."""
    YES_NO = 0
    YES_NO_CANCEL = 1
    OK_CANCEL = 2

@_enum.unique
class ConfirmResult(_enum.Enum):
    """The various results that can be returned from some option dialogs."""
    CANCEL = -1  # For yes/no/cancel
    NO = 0  # No is 'falsey'
    YES = 1  # Yes is 'truthy'
    OK = 2  # For ok/cancel dialogs

@_enum.unique
class MessageType(_enum.Enum):
    ERROR = 0
    INFORMATION = 1
    PLAIN = -1
    QUESTION = 3
    WARNING = 2

class GOptionPane:

    class InternalResult(_enum.Enum):
        """The results that can come back from showConfirmDialog.

        These are converted into Result enum values.
        """
        CANCEL_OPTION = 2
        CLOSED_OPTION = -1
        NO_OPTION = 1
        OK_OPTION = 0
        YES_OPTION = 0

    @classmethod
    def show_confirm_dialog(cls, message, title="", confirm_type=ConfirmType.YES_NO):
        if confirm_type not in ConfirmType:
            error("GOptionPane::show_confirm_dialog: Illegal dialog type.")

        if not title:
            title = "Select an option"

        result = cls.InternalResult(_platform.Platform().goptionpane_show_confirm_dialog(message, title, confirm_type))
        print("from platform: ", result)
        if result in [cls.InternalResult.OK_OPTION, cls.InternalResult.YES_OPTION]:
            # this is weird code because JOptionPane thinks of OK and Yes as the same,
            #and differentiates based on context of whether this is an OK/Cancel or Yes/No dialog
            return ConfirmResult.OK if confirm_type == ConfirmType.OK_CANCEL else ConfirmResult.YES
        elif result == cls.InternalResult.NO_OPTION:
            return ConfirmResult.NO
        else:
            return ConfirmResult.CANCEL

    @classmethod
    def show_input_dialog(cls, message, title=""):
        return _platform.Platform().goptionpane_show_input_dialog(message, title)

    @classmethod
    def show_message_dialog(cls, message, title="", message_type=MessageType.PLAIN):
        if message_type not in MessageType:
            error("GOptionPane::showMessageDialog: Illegal dialog type.");
        if not title:
            title = "Message"
        _platform.Platform().goptionpane_show_message_dialog(message, title, message_type)

    @classmethod
    def show_option_dialog(cls, message, options, title="", initially_selected=""):
        if not title:
            title = "Select an option"
        index = _platform.Platform().goptionpane_show_option_dialog(message, title, options, initially_selected)
        if cls.InternalResult(index) != cls.InternalResult.CLOSED_OPTION and 0 <= index < len(options):
            return options[index]
        return ""

    @classmethod
    def show_text_file_dialog(cls, message, title="", rows=-1, cols=-1):
        if not title:
            title = "Text file contents"
        _platform.Platform().goptionpane_show_text_file_dialog(message, title, rows, cols)



