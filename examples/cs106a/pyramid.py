from spgl.graphics.gwindow import *
from spgl.graphics.gobjects import *
from spgl.graphics.gevents import *
from spgl.gtimer import *
from spgl.grandom import *

window = GWindow(width=1280, height=800)
window.setWindowTitle("Pyramid")
# window.setSize(1280, 800)

MAX_WIDTH = window.getWidth()
MAX_HEIGHT = window.getHeight()
NUM_BRICKS_IN_BASE = 12
BRICK_WIDTH = MAX_WIDTH // NUM_BRICKS_IN_BASE
BRICK_HEIGHT = MAX_HEIGHT // NUM_BRICKS_IN_BASE
COLORS = ["red", "green", "blue", "yellow", "orange"]

def get_color(row_num):
    return COLORS[row_num % len(COLORS)]

start_y = MAX_HEIGHT - BRICK_WIDTH + 22
for brick_row in range(NUM_BRICKS_IN_BASE):
    row_y = start_y - brick_row * BRICK_HEIGHT
    num_bricks_in_row = NUM_BRICKS_IN_BASE - brick_row
    start_x = (MAX_WIDTH - num_bricks_in_row * BRICK_WIDTH) // 2
    for brick_index in range(num_bricks_in_row):
        x = start_x + brick_index * BRICK_WIDTH
        brick = GRect(BRICK_WIDTH, BRICK_HEIGHT, x, row_y)
        brick.setFilled(True)
        brick.setFillColor(color=get_color(brick_row))
        window.add(brick)
