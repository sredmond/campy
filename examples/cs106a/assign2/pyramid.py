#!/usr/bin/env python3
"""Draw a graphical pyramid on screen."""
# TODO(sredmond): Rethink star-imports - they pollute the global namespace and
# are generally a bad style point (awkward imports of _underscore identifiers).
from campy.graphics.gwindow import *
from campy.graphics.gobjects import *
from campy.graphics.gtimer import *

window = GWindow(width=1280, height=800)
window.title = 'Pyramid'

MAX_WIDTH = window.width
MAX_HEIGHT = window.height
NUM_BRICKS_IN_BASE = 12

BRICK_WIDTH = MAX_WIDTH // NUM_BRICKS_IN_BASE
BRICK_HEIGHT = MAX_HEIGHT // NUM_BRICKS_IN_BASE

DEFAULT_COLORS = ('red', 'green', 'blue', 'yellow', 'orange')
def get_color(row_num, colors=DEFAULT_COLORS):
    return colors[row_num % len(colors)]

def make_brick(x, y, color):
    brick = GRect(BRICK_WIDTH, BRICK_HEIGHT, x, y)
    brick.filled = True
    brick.fill_color = color
    return brick

def make_pyramid():
    start_y = MAX_HEIGHT - BRICK_HEIGHT
    for brick_row in range(NUM_BRICKS_IN_BASE):
        row_color = get_color(brick_row)
        row_y = start_y - brick_row * BRICK_HEIGHT
        num_bricks_in_row = NUM_BRICKS_IN_BASE - brick_row
        start_x = (MAX_WIDTH - num_bricks_in_row * BRICK_WIDTH) // 2
        for brick_num in range(num_bricks_in_row):
            x = start_x + brick_num * BRICK_WIDTH
            brick = make_brick(x, row_y, row_color)
            window.add(brick)

if __name__ == '__main__':
    make_pyramid()
