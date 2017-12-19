"""Draw a red-and-white target.

"""
from spgl.graphics.gwindow import GWindow, pause
from spgl.graphics.gobjects import GOval

DEFAULT_OUTER_RADIUS = 72  # pixels == 1 inch
DEFAULT_NUM_CIRCLES = 3
DEFAULT_COLORS = ['red', 'white']

def draw_centered_circle(window, x, y, radius, color):
    circle = GOval(x=x-radius, y=y-radius, width=2 * radius, height=2 * radius)

    circle.filled = True
    circle.fill_color = color

    window.add(circle)


def draw_target(window, outer_radius=DEFAULT_OUTER_RADIUS,
                num_circles=DEFAULT_NUM_CIRCLES, colors=DEFAULT_COLORS):
    center_x, center_y = window.width / 2, window.height / 2
    for circle_id in range(num_circles):
        radius = outer_radius * (num_circles - circle_id) / num_circles
        color = colors[circle_id % len(colors)]
        draw_centered_circle(window, center_x, center_y, radius, color)


if __name__ == '__main__':
    window = GWindow(width=1080, height=1080)
    draw_target(window)
    pause(1000)
    draw_target(window, outer_radius=min(window.height, window.width), num_circles=100)
