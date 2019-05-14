#!/usr/bin/env python
"""CS106A Assignment 2 Example: Tiles

This program displays four centered tiles, each containing centered text.
"""
from campy.graphics.gobjects import GLabel, GRect
from campy.graphics.gwindow import GWindow


# Width of each tile (in pixels).
TILE_WIDTH = 100

# Height of each tile (in pixels).
TILE_HEIGHT = 50

# Amount of space between each of the tiles (in pixels).
# Used for both horizontal space and vertical space between tiles.
TILE_SPACE = 20

# The label for each of the tiles.
LABEL_TEXT = 'CS106A'


def create_centered_label(x, y):
    # Center the label, noting that a label's location is its lower-left corner.
    label = GLabel(LABEL_TEXT)
    label.location = (x - label.width / 2, y + label.ascent / 2)
    return label


def create_centered_rect(x, y):
    return GRect(TILE_WIDTH, TILE_HEIGHT, x=x-TILE_WIDTH/2, y=y-TILE_HEIGHT/2)


def draw_centered_tile(window, x, y):
    # A tile has a rectangle and a label.
    window.add(create_centered_rect(x, y))
    window.add(create_centered_label(x, y))


def draw_centered_tiles(window):
    x, y = window.width / 2, window.height / 2
    x_offset = (TILE_WIDTH + TILE_SPACE) / 2
    y_offset = (TILE_HEIGHT + TILE_SPACE) / 2

    # Draw the four centered tiles.
    draw_centered_tile(window, x - x_offset, y - y_offset)  # Upper-left.
    draw_centered_tile(window, x - x_offset, y + y_offset)  # Lower-left.
    draw_centered_tile(window, x + x_offset, y - y_offset)  # Upper-right.
    draw_centered_tile(window, x + x_offset, y + y_offset)  # Lower-right.


if __name__ == '__main__':
    window = GWindow(title='Tiles')
    draw_centered_tiles(window)
