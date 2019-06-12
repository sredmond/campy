"""Schedule time-delayed functions into the future.

To pause current execution, use the :meth:`pause` method.

The usual warnings about using time-based functions apply in this module.
Namely, the functions here are only as precise as the underlying system time
used by the backend.

For more details, see: https://docs.python.org/3/library/time.html
"""
import campy.private.platform as _platform

import functools
import time
import logging

# Module-level logger.
logger = logging.getLogger(__name__)


def pause(milliseconds, step=None, time_fn=time.time, sleep_fn=time.sleep):
    """Pause the current thread while pumping queued events.

    This method pauses for at least at long as the requested number of
    milliseconds.

    To pause for one second::

        window = GWindow()
        oval = GOval(200, 400)
        window.add(oval, 50, 50)
        pause(1000)
        rect = GRect(200, 400)
        window.add(rect, 50, 50)

    While the execution is paused, queued events are flushed through the
    backend until the desired time has passed. This rate can be controlled with
    the step argument, which forces true thread sleep between event queue
    flushes.

    :param milliseconds: The number of milliseconds to pause for.
    :param step: The number of milliseconds to step between events.
    :param time_fn: The time function to use, measured in seconds.
    :param sleep_fn: The sleep function to use, measured in seconds.
    """
    # TODO(sredmond): Consider hiding this all in a timer_pause backend method.
    logger.info('Pausing for {} milliseconds.'.format(milliseconds))
    events = 0  # Number of events processed - useful only for debugging.
    start = time_fn()
    # Loop until at least this much time has passed.
    while time_fn() - start < milliseconds / 1000:
        _platform.Platform().event_pump_one()
        events += 1
        if step:
            sleep_fn(step / 1000)
    end = time_fn()
    logger.info('Seconds Elapsed: {}'.format(end - start))
    logger.info('Events Handled: {}'.format(events))


def repeat_every(delay_ms, function=None, fargs=()):
    """Repeat a function periodically and infinitely.

    This will schedule a delay between function calls, so if the function itself
    takes a long time, the gap between function calls may be larger than the
    supplied argument.

    This function can be used either as a decorator or directly. If used as a
    decorator, the decorated function must be invoked to start the loop. If
    used directly, the looping function will be started immediately.)

    Invoked as a decorator::

        @repeat_every(1000)
        def update_time_elapsed(label):
            label.text = 'Current Time: {}'.format(time.ctime())

        window = GWindow()
        label = GLabel()
        window.add(label, window.width / 2, window.height / 2)
        update_time_elapsed(label)  # Start the infinite loop.

    Note that the new function is explicitly invoked to start the loop.

    Invoked directly:

        def update_time_elapsed(label):
            label.text = 'Current Time: {}'.format(time.ctime())

        repeat_every(1000, update_time_elapsed, fargs=(label,))  # No additional invoking.

    :param delay_ms: The number of milliseconds to delay between invocations.

    """
    # TODO(sredmond): This is a wonky API. Consider removing or restructuring.
    if not function:  # Used as a decorator-decorator
        def decorator(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                out = fn(*args, **kwargs)
                schedule(wrapper, delay_ms)  # Reschedule this wrapper.
                return out
            # Don't explicitly schedule the decorated function to start.
            return wrapper
        return decorator
    else:  # Invoked directly.
        def wrapper(*args, **kwargs):
            out = fn(*args, **kwargs)
            schedule(wrapper, delay_ms, fargs=fargs)  # Reschedule this wrapper.
            return out
        schedule(wrapper, delay_ms, fargs=fargs)


def schedule(function, delay_ms, fargs=()):
    """Schedule a function to execute in the future.

    Usage::

        window = GWindow()
        oval = GOval(200, 400)
        window.add(oval, 50, 50)

        def draw_box(window):
            rect = GRect(200, 400)
            window.add(rect, 50, 50)

        schedule(draw_box, 1000, fargs=(window, ))

    This instructs the backend to execute a callable after some time has passed.
    :param function: The callable to schedule.
    :param delay_ms: The number of milliseconds in the future to schedule.
    :param fargs: Additional arguments to be passed to the function.
    """
    curried = functools.partial(function, *fargs)
    # HACK(sredmond): Curried functions don't get __name__ set, but some backends rely on it.
    curried.__name__ = 'partial_{}'.format(function.__name__)
    _platform.Platform().timer_schedule(curried, delay_ms)

