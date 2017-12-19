from spgl.graphics.gobjects import GLabel, GRect
from spgl.graphics.gwindow import GWindow

TILE_WIDTH = 100
TILE_HEIGHT = 50
TILE_SPACE = 20
LABEL_TEXT = 'CS106A'

def create_centered_label(x, y, text=LABEL_TEXT):
    label = GLabel(text)

    label.location = (x - label.width / 2, y + label.ascent / 2)

    return label

def draw_centered_tile(window, x, y, width=TILE_WIDTH, height=TILE_HEIGHT):
    tile = GRect(x=x-width/2, y=y-height/2, width=width, height=height)
    window.add(tile)
    window.add(create_centered_label(x, y))

def draw_centered_tiles(window):
    x, y = window.width / 2, window.height / 2
    x_offset = (TILE_WIDTH + TILE_SPACE) / 2
    y_offset = (TILE_HEIGHT + TILE_SPACE) / 2
    draw_centered_tile(window, x - x_offset, y - y_offset)
    draw_centered_tile(window, x - x_offset, y + y_offset)
    draw_centered_tile(window, x + x_offset, y - y_offset)
    draw_centered_tile(window, x + x_offset, y + y_offset)

if __name__ == '__main__':
    window = GWindow()
    draw_centered_tiles(window)
