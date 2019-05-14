#!/usr/bin/env python
"""CS106A Assignment 2 Example: Illusion

This program draws four filled 270 degree arcs on a white background to create
the illusion of a rectangle in negative space.
"""
from campy.graphics.gcolor import GColor
from campy.graphics.gobjects import GArc
from campy.graphics.gtypes import GPoint
from campy.graphics.gwindow import GWindow

# Width of the rectangle (in pixels).
RECTANGLE_WIDTH = 350

# Height of the rectangle (in pixels).
RECTANGLE_HEIGHT = 270

# Radius of each constructed arc. For the illusion to look interesting, this
# should be no more than half the minimum of the rectangle's height and width.
ARC_RADIUS = 50

if __name__ == '__main__':
    window = GWindow(title='Illusion')
    center = GPoint(window.width / 2, window.height / 2)
    corners = (
        GPoint(center.x - RECTANGLE_WIDTH / 2, center.y - RECTANGLE_HEIGHT / 2),  # Upper-left
        GPoint(center.x - RECTANGLE_WIDTH / 2, center.y + RECTANGLE_HEIGHT / 2),  # Lower-left
        GPoint(center.x + RECTANGLE_WIDTH / 2, center.y + RECTANGLE_HEIGHT / 2),  # Lower-right
        GPoint(center.x + RECTANGLE_WIDTH / 2, center.y - RECTANGLE_HEIGHT / 2),  # Upper-right
    )

    for corner, start in zip(corners, range(0, 360, 90)):
        arc = GArc(ARC_RADIUS * 2, ARC_RADIUS * 2, start=start, sweep=270, x=corner.x - ARC_RADIUS, y=corner.y - ARC_RADIUS)
        arc.filled = True
        window.add(arc)
        # Alternatively, don't set the arc's location at initialization and instead set it here.
        # window.add(arc, corner.x - ARC_RADIUS, corner.y - ARC_RADIUS)
