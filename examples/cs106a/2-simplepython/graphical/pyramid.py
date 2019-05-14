#!/usr/bin/env python
"""CS106A Assignment 2 Example: Pyramid

This program draw a pyramid consisting of bricks arranged in horizontal rows.
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GRect

# Width of each brick (in pixels).
BRICK_WIDTH = 60

# Height of each brick (in pixels).
BRICK_HEIGHT = 24

# Number of bricks in the base.
BRICKS_IN_BASE = 14

###############
# Extensions! #
###############

# Color names to cycle between.
COLORS = ('RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'INDIGO', 'VIOLET')


def get_color(row_num):
    return COLORS[row_num % len(COLORS)]


def make_brick(x, y, color):
    brick = GRect(BRICK_WIDTH, BRICK_HEIGHT, x=x, y=y)
    brick.filled = True
    brick.fill_color = color
    return brick


def draw_row(window, bricks_in_row, start_x, row_y, row_color):
    for brick_num in range(bricks_in_row):
        # Slide to the right as we lay bricks in this row.
        x = start_x + brick_num * BRICK_WIDTH
        brick = make_brick(x, row_y, row_color)
        window.add(brick)


def draw_pyramid(window):
    # Align the bottom row to the bottom of the window.
    start_y = window.height - BRICK_HEIGHT
    for brick_row in range(BRICKS_IN_BASE):
        bricks_in_row = BRICKS_IN_BASE - brick_row
        # Center the row in the window.
        start_x = (window.width - bricks_in_row * BRICK_WIDTH) // 2
        row_y = start_y - brick_row * BRICK_HEIGHT
        row_color = get_color(brick_row)
        draw_row(window, bricks_in_row, start_x, row_y, row_color)


if __name__ == '__main__':
    # Leave some extra space in the window.
    window_width = BRICK_WIDTH * (BRICKS_IN_BASE + 1)
    window_height = BRICK_HEIGHT * (BRICKS_IN_BASE + 1)

    window = GWindow(width=window_width, height=window_height, title='Pyramid')
    draw_pyramid(window)
