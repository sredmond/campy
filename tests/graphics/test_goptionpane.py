"""Tests for the :mod:`campy.graphics.goptionpane` module."""
from campy.graphics.goptionpane import GOptionPane, ConfirmType, MessageType

# TODO(sredmond): Find a way to unit test these modules.

def test_confirm_dialog():
    assert False
    print(GOptionPane.show_confirm_dialog("Do you really wanna?"))
    print(GOptionPane.show_confirm_dialog("Do you really wanna?", confirm_type=ConfirmType.OK_CANCEL))
    print(GOptionPane.show_confirm_dialog("Do you really wanna?", confirm_type=ConfirmType.YES_NO_CANCEL))
    print(GOptionPane.show_confirm_dialog("Do you really wanna?", title="Look at me!"))


def test_input_dialog():
    assert False
    print(GOptionPane.show_input_dialog("Do you want to build a snowman?"))
    print(GOptionPane.show_input_dialog("Do you want to build a snowman?", title="Hey there"))


def test_message_dialog():
    assert False
    GOptionPane.show_message_dialog("Basic Message Dialog!")
    GOptionPane.show_message_dialog("Dialog w/ Title!", title="I'm a title!")
    GOptionPane.show_message_dialog("Error Message1", message_type=MessageType.ERROR)
    GOptionPane.show_message_dialog("Info Message!", message_type=MessageType.INFORMATION)
    GOptionPane.show_message_dialog("Question Message!", message_type=MessageType.QUESTION)  # TODO this doesn't show the right icon
    GOptionPane.show_message_dialog("Warning Message!", message_type=MessageType.WARNING)


def test_option_dialog():
    assert False
    print(GOptionPane.show_option_dialog("Basic Options Dialog!", ["aah", "boo", "cow"]))
    print(GOptionPane.show_option_dialog("options w/ title!", ["aah", "boo", "cow"], title="hi im a title"))
    print(GOptionPane.show_option_dialog("No options!", []))
    print(GOptionPane.show_option_dialog("Non-str options!", [1,2,3,4]))
    print(GOptionPane.show_option_dialog("default-selected!", ["car", "boat", "plane"], initially_selected="plane"))
    print(GOptionPane.show_option_dialog("default-selected w/ bad initial!", ["car", "boat", "plane"], initially_selected="derp"))


def test_text_file_dialog():
    assert False
    GOptionPane.show_text_file_dialog("Text File Dialog")
    GOptionPane.show_text_file_dialog("Text File Dialog w/ title", title="im a title")
    GOptionPane.show_text_file_dialog("Text File Dialog w/ title and rows", title="im a title", rows=10)
    GOptionPane.show_text_file_dialog("Text File Dialog w/ title and cols", title="im a title", cols=10)
    GOptionPane.show_text_file_dialog("Text File Dialog w/ title and rows and cols", title="im a title", rows=5, cols=10)
