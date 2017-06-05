"""
File: gtimer.py
---------------
This file defines the <code>GTimer</code> class, which implements a
general interval timer.

A <code>GTimer</code> fires GTimerEvents on the EventQueue.
"""

# Implementation Note:
# While Stanford's CPP lib (as of 05/17) uses a GTimerData struct to manage reference counting,
# Python already handles reference counting and deletion for us.
# By implementing a __del__ method, we can specify what to do when the object is truly destroyed.
# TODO: Make sure that, when deletion on interpreter exit executes, that platform still exists.

# TODO: handle copy.copy() and copy.deepcopy() by supporting pickled methods

import spgl.private.platform as _platform

class GTimer:
    """
    Implements a simple interval timer that generates a
    <code>GTimerEvent</code> with a specified frequency.
    """

    def __init__(self, milliseconds):
        """
        Creates a GTimer object that generates a GTimerEvent
        each time the specified number of milliseconds has elapsed.

        No events are generated until the client calls start on the timer.
        For more details on using timers, see the documentation for the GTimerEvent class.

        :type milliseconds: int
        :param milliseconds: interval for timer event
        """
        _platform.Platform().gtimer_constructor(self, milliseconds)

    def __del__(self):
        """Deletes the Java resources associated with this timer.

        This method is called when there are no more references to this object
        (Python keeps track), and is not guaranteed to be called if the object
        exists when the interpreter exits.

        TODO: Make sure module symbols from _platform haven't been cleaned up already.
        """
        print("In del")
        _platform.Platform().gtimer_delete(self)

    def start(self):
        """Starts the timer.

        A timer continues to generate timer events until it
        is stopped; to achieve the effect of a one-shot timer, the simplest
        approach is to call the <code>stop</code> method inside the event
        handler.
        """
        _platform.Platform().gtimer_start(self)

    def pause(self, millis):
        """Pauses (all?) timers for <code>millis</code> milliseconds before automatically resuming."""
        _platform.Platform().gtimer_pause(millis)

    def stop(self):
        """Stops the timer so that it stops generating events until it is restarted."""
        _platform.Platform().gtimer_stop(self)

    """
    Equality, inequality, and copying are all handled for us
    """

def _test():
    import spgl.graphics.gevents as gevents
    print('Creating timer...')
    timer = GTimer(1000)
    print('Starting timer...')
    timer.start()
    print('Started!')
    count = 0
    while count < 10:
        print('Waiting for event')
        event = _platform.Platform().getNextEvent(gevents.EventType.TIMER_TICKED)
        if event.getEventType() == gevents.EventType.TIMER_TICKED:
            print('Received a TICK')
            count += 1
            if count == 5:
                print('Pausing for 5s')
                timer.pause(4000)
    timer.stop()
    # del timer


if __name__ == '__main__':
    _test()
