"""Top-level Exceptions and Errors.

Provides a generic function to raise an error from a message.

All exceptions (that are not builtin exceptions like ValueError, IndexError)
raised in this library inherit from :class:`CampyException`, the root of all
exceptions in this library.
"""
# TODO(sredmond): Should this be called ErrorException for consistency with ACM?
class CampyException(Exception):
    """Root of all exceptions in the :mod:`campy` module.

    This allows for consistent exception reporting in the module.
    """


class InterruptedIOError(CampyException):
    """A blocking I/O call is interrupted by closing the program."""


def error(message):
    """Generic function to raise an error.

    Signals an error condition in a program by throwing an
    :class:`CampyException`: with the specified message.

    :param str message: error message
    :raises: An :class:`CampyException` with the supplied error message.

    Usage::

        if 'Red Leicester' not in cheeses:
            error("I'm afraid we're fresh out of Red Leicester, sir.")

    You can check whether a code block raises a :class:`CampyException` with::

        try:
            do_something_that_might_raise_a_campy_exception()
        except CampyException:
            recover_from_an_error()

    If the supplied message is an instance or a subclass of :class:`Exception`,
    the :class:`CampyException` is raised from the supplied Exception so that
    traceback information is maintained.
    """
    if isinstance(message, Exception) or issubclass(message, Exception):
        raise CampyException(message) from message
    else:
        raise CampyException(message)


__all__ = ['CampyException', 'InterruptedIOError', 'error']
