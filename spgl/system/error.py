"""
File: error.py
--------------
Implementation of the error function.

TODO: Make naming consistent with PEP8? (i.e. Error and InterruptedIOError instead?)
"""
class ErrorException(Exception):
    """Allows errors to be reported in a consistent way."""
    # def __init__(self, message=''):
    #     # if isinstance(msg, Exception):
    #     #     msg = "{cls}: {msg}".format(cls=msg.__class__, msg=str(msg))
    #     super().__init__(self, message)

class InterruptedIOException(Exception):
    """Thrown when a blocking I/O call is interrupted by closing the program."""
    pass


def error(message):
    """Generic function to raise an error.

    Signals an error condition in a program by throwing an
    <code>ErrorException</code> with the specified message.

    :param str message: error message
    :raises: An :class:`ErrorException` with the supplied error message.
    """
    raise ErrorException(message)
