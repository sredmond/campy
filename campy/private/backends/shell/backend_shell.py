"""A normal shell console can provide (some of) a console backend."""
from campy.private.backend_base import ConsoleBackendBase

import logging
import sys


# Module-level logger.
logger = logging.getLogger(__name__)


class ShellConsoleBackend(ConsoleBackendBase):
    """A naive implementation of a ConsoleBackend around a shell console."""

    def get_console_line(self):
        """Read a line of input from the user."""
        return input()

    def put_console(self, line, stderr=False):
        """Print a line of output to the console."""
        outfile = sys.stdout if not stderr else sys.stderr
        print(line, file=outfile)

    #########################
    # Unimplemented Methods #
    #########################
    def clear_console(self):
        logger.debug('clear_console has no effect on a ShellConsoleBackend.')

    def set_console_font(self, font):
        logger.debug('set_console_font has no effect on a ShellConsoleBackend.')

    def set_console_size(self, console_size):
        logger.debug('set_console_size has no effect on a ShellConsoleBackend.')

    def echo_console(self):
        logger.debug('echo_console has no effect on a ShellConsoleBackend.')

    def end_line_console(self):
        logger.debug('end_line_console has no effect on a ShellConsoleBackend.')
