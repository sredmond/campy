"""Tests for the :mod:`campy.graphics.gtimer` module."""
from campy.graphics.gtimer import GTimer

from campy.graphics.gevents import EventType

# Find a way to test this timer.

def test_create_timer():
    assert False
    timer = GTimer(1000)
    timer.start()
    count = 0
    while count < 10:
        event = _platform.Platform().getNextEvent(EventType.TIMER_TICKED)
        if event.event_type == EventType.TIMER_TICKED:
            print('Received a TICK')
            count += 1
            if count == 5:
                print('Pausing for 5s')
                timer.pause(5000)
    timer.stop()
