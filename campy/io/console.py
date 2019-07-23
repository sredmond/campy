"""
File: console.py
----------------
This file redirects the <code>cin</code>, <code>cout</code>,
and <code>cerr</code> channels to use a console window.  This file
must be included in the source file that contains the <code>main</code>
method, although it may be included in other source files as well.
"""

import campy.private.platform as _platform
import enum as _enum

# Set this to True for autograding to avoid the startup of loading a graphical window.
__DONT_ENABLE_GRAPHICAL_CONSOLE = False

class Console:
    def __init__(self):
        self.console_clear_enabled = False
        self.console_echo = False
        self.console_event_on_close = False
        self.console_exit_program_on_close = False
        self.console_location_saved = False
        self.console_locked = False
        self.console_close_operation = ConsoleCloseOperation.CONSOLE_HIDE_ON_CLOSE

    def clear_console(self):
        msg = "==================== (console cleared) ===================="
        if self.console_clear_enabled:
            print(msg)
            _platform.getPlatform().jbeconsole_clear()
        else:
            print(msg)

    @property
    def console_print_exceptions(self):
        pass

    # @console_close_operation.setter
    # def console_close_operation(self, op):
    #     if self.console_locked: return
    #     self.console_close_operation = op
    #     print('TODO: jbeconsole_setCloseOperation')
    #     #_platform.getPlatform().jbeconsole_setCloseOperation(op)
    #     self.console_exit_program_on_close = op == ConsoleCloseOperation.CONSOLE_EXIT_ON_CLOSE

    # @console_echo.setter
    # def console_echo(self, echo):
    #     if self.console_locked: return
    #     self.console_echo = echo

    # @console_error_color.setter
    # def console_error_color(self, color): # TODO: annotate color w/ str
    #     if self.console_locked: return
    #     self.console_error_color = color
    #     print('TODO: jbeconsole_setConsoleColor')

    # @console_event_on_close.setter
    # def console_event_on_close(self, event_on_close):
    #     if self.console_locked: return
    #     self.console_event_on_close = event_on_close


class ConsoleCloseOperation(_enum.IntEnum):
    CONSOLE_DO_NOTHING_ON_CLOSE = 0
    CONSOLE_HIDE_ON_CLOSE = 1
    CONSOLE_DISPOSE_ON_CLOSE = 2
    CONSOLE_EXIT_ON_CLOSE = 3

# TODO: redirect stuff

_inst = Console()

