#!/usr/bin/env python3

from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GLine, GOval
from campy.gui.events.window import onwindowclosed
from campy.graphics.goptionpane import GOptionPane, ConfirmResult

def main():
    window = GWindow(400, 400)

    # Awkward! We need a window before we can do anything.
    @onwindowclosed
    def prompt_exit():
        result = GOptionPane.show_confirm_dialog("Are you sure you want to quit?")
        if result == ConfirmResult.YES:
            return False
        return True

if __name__ == '__main__':
    main()
