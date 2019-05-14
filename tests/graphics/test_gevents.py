"""Tests for the :mod:`campy.graphics.gevents` module."""
from campy.graphics.gevents import GEvent, GMouseEvent, EventType, EventClassType


def test_create_empty_event():
    event = GEvent()
    assert event.event_class == EventClassType.NULL_EVENT
    assert event.event_type is None


def test_mouse_clicked_event():
    event = GMouseEvent(EventType.MOUSE_CLICKED, x=100, y=50)
    assert event.event_class == EventClassType.MOUSE_EVENT
    assert event.event_type == EventType.MOUSE_CLICKED
    assert event.x == 100
    assert event.y == 50
