"""A general interval timer that fires :class:GTimerEvent`s."""
# NOTE(sredmond): Although the Stanford C++ libraries use GTimerData to manage
# reference counts, Python will automatically garbage collect correctly for us.
# Overriding the __del__ method allows us to offer Python some instruction for
# when a GTimer is cleaned up, but __del__ isn't guaranteed to be called
# immediately or at all, so we risk stranding memory.
import campy.private.platform as _platform


class GTimer:
    """An interval timer that generates :class:GTimerEvent`s at a fixed rate."""

    def __init__(self, milliseconds):
        """Create a :class:`GTimer` that can generate :class:`GTimerEvent`s.

        Once started, the timer will generate a :class:`GTimerEvent` each time
        the given number of milliseconds has elapsed.

        Note that no events are generated until the client calls :meth:`start()`
        on the timer.

        For more, see the documentation for :class:`GTimerEvent`.

        :param milliseconds: The timer interval (in milliseconds).
        """
        self.milliseconds = milliseconds
        _platform.Platform().gtimer_constructor(self)

    def __del__(self):
        """Delete the backend resources associated with this :class:`GTimer`.

        This method is called by Python only when there are no references to
        this object. However, it is not guaranteed to be called immediately or
        even eventually (depending on the Python implementation). Thus, it's
        best to think of this as a friendly suggestion to the Python
        interpreter that cleaning up a :class:`GTimer` involves informing the
        backend that it should free up any resources associated with the timer
        as well.
        """
        # TODO(sredmond): Investigate race condition when GTimer is deleted
        # after the platform is deleted.
        _platform.Platform().gtimer_delete(self)

    def start(self):
        """Start this timer.

        A timer will generate :class:`GTimerEvent`s until it is stopped.

        To achieve the effect of a one-shot timer, the best approach is to
        call :meth:`stop()` on this timer after processing one event.
        """
        _platform.Platform().gtimer_start(self)

    def pause(self, milliseconds):
        """Pause this timer for some time before automatically resuming.

        :param milliseconds: How long to pause this timer for (in milliseconds).
        """
        _platform.Platform().gtimer_pause(self, millis)

    def stop(self):
        """Stop this timer from generating events until it is restarted."""
        _platform.Platform().gtimer_stop(self)

    def __repr__(self):
        return 'GTimer(ms={})'.format(self.milliseconds)
