import math

from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import *

def draw_sierpinski_triangle(window, x, y, size, order):
    height = size * math.sqrt(3) / 2
    if order == 0:
        window.add(GLine(x, y, x+size, y))  # Horizontal segment.
        window.add(GLine(x, y, x+size/2, y+height))  # Left inclined segment.
        window.add(GLine(x+size/2, y+height, x+size, y))  # Right inclined segment.
    else:
        draw_sierpinski_triangle(window, x, y, size/2, order-1)
        draw_sierpinski_triangle(window, x+size/2, y, size/2, order-1)
        draw_sierpinski_triangle(window, x+size/4, y+height/2, size/2, order-1)

if __name__ == '__main__':
    size = 1080
    order = 5

    gw = GWindow(width=size, height=size)
    draw_sierpinski_triangle(gw, 0, 0, size, order)
