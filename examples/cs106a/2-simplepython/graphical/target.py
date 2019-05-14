#!/usr/bin/env python
"""CS106A Assignment 2 Example: Target

This program draws an centered archery target with alternating concentric red and white circles.
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval

# Radius of the outermost circle (in pixels).
OUTER_RADIUS = 72  # 72 pixels is 1 inch on many displays.

# Radius of the innermost circle (in pixels).
INNER_RADIUS = 24  # 24 pixels is 1/3 inch on many displays.

###############
# Extensions! #
###############

# Color names to cycle between.
COLORS = ('RED', 'WHITE')

# The number of circles to draw.
NUM_CIRCLES = 3


def draw_centered_circle(window, x, y, radius, color):
    # A circle's width and height are twice the radius.
    circle = GOval(2 * radius, 2 * radius, x=x-radius, y=y-radius)
    circle.filled = True
    circle.fill_color = color
    window.add(circle)


def draw_target(window):
    center_x, center_y = window.width / 2, window.height / 2
    for circle_id in range(NUM_CIRCLES):
        # Linearly space between inner and outer radius.
        radius = INNER_RADIUS + (OUTER_RADIUS - INNER_RADIUS) * (NUM_CIRCLES - circle_id - 1) / (NUM_CIRCLES - 1)
        color = COLORS[circle_id % len(COLORS)]
        draw_centered_circle(window, center_x, center_y, radius, color)


if __name__ == '__main__':
    window = GWindow(width=OUTER_RADIUS * 3, height=OUTER_RADIUS * 3, title='Target')
    draw_target(window)
