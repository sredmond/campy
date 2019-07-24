"""Interact with the graphics libraries via window events.

There are only two types of window events to which a caller can subscribe:

- WindowClosed: The graphical window was closed.
- WindowResized: The graphical window was resized.
"""
import campy.private.platform as _platform

# Define decorators for all of the common types of events.
def onwindowclosed():
    pass

def onwindowresized():
    pass
