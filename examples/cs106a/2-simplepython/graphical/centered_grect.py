#!/usr/bin/env python
"""CS106A Assignment 2 Example: Centered Rectangle (Warmup)

This program draws a blue, filled rectangle with a width of 350 pixels and a
height of 270 pixels in the center of the screen.
"""
from campy.graphics.gcolor import GColor
from campy.graphics.gobjects import GRect
from campy.graphics.gtypes import GPoint
from campy.graphics.gwindow import GWindow

# Width of the rectangle (in pixels).
RECTANGLE_WIDTH = 350

# Height of the rectangle (in pixels).
RECTANGLE_HEIGHT = 270

# Color of the rectangle.
RECTANGLE_COLOR = GColor.BLUE

if __name__ == '__main__':
    window = GWindow(title='Centered Rectangle')
    center = GPoint(window.width / 2, window.height / 2)

    rect = GRect(RECTANGLE_WIDTH, RECTANGLE_HEIGHT, x=center.x - RECTANGLE_WIDTH / 2, y=center.y - RECTANGLE_HEIGHT / 2)
    rect.filled = True
    rect.fill_color = RECTANGLE_COLOR

    window.add(rect)
    # Alternatively, don't set the rect's location at initialization and instead set it here.
    # window.add(rect, center.x - rect.width / 2, center.y - rect.height / 2)
