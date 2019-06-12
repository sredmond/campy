"""Breakout!"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect

from campy.gui.events.mouse import onmousemoved
from campy.gui.events.timer import pause

# Radius of the ball (in pixels).
BALL_RADIUS = 10

# Width of the paddle (in pixels).
PADDLE_WIDTH = 125

# Height of the paddle (in pixels).
PADDLE_HEIGHT = 15

# Vertical offset of the paddle from the window bottom (in pixels).
PADDLE_OFFSET = 50

# Color names to cycle through for brick rows.
COLORS = ('RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE')

# Space between bricks (in pixels).
# This space is used for horizontal and vertical spacing.
BRICK_SPACING = 5

# Height of a brick (in pixels).
BRICK_WIDTH = 40

# Height of a brick (in pixels).
BRICK_HEIGHT = 15

# Number of rows of bricks.
BRICK_ROWS = 10

# Number of columns of bricks.
BRICK_COLS = 10

# Vertical offset of the topmost brick from the window top (in pixels).
BRICK_OFFSET = 50


# Create a graphical window, with some extra space.
window_width = BRICK_COLS * (BRICK_WIDTH + BRICK_SPACING) - BRICK_SPACING
window_height = BRICK_OFFSET + 3 * (BRICK_ROWS * (BRICK_HEIGHT + BRICK_SPACING) - BRICK_SPACING)
window = GWindow(width=window_width, height=window_height, title='Breakout')


# Center a filled ball in the graphical window.
ball = GOval(2 * BALL_RADIUS, 2 * BALL_RADIUS, x=window.width/2, y=window.height/2)
ball.filled = True
window.add(ball)


# Default initial velocity for the ball.
vx = 2.7
vy = 3.0


# Create a paddle.
paddle = GRect(PADDLE_WIDTH, PADDLE_HEIGHT, x=window.width/2, y=window.height-PADDLE_OFFSET)
paddle.filled = True
window.add(paddle)

# TODO(sredmond): Add a hotkey to reset the game.

def make_bricks(window):
    for row in range(BRICK_ROWS):
        row_color = COLORS[(row // 2) % len(COLORS)]
        for col in range(BRICK_COLS):
            brick = GRect(BRICK_WIDTH, BRICK_HEIGHT,
                          x=col * (BRICK_WIDTH + BRICK_SPACING), y=BRICK_OFFSET + row * (BRICK_HEIGHT + BRICK_SPACING))
            brick.filled = True
            brick.fill_color = row_color
            window.add(brick)


def get_colliding_object(window, ball):
    upper_left  = window.get_object_at(ball.x,              ball.y)
    upper_right = window.get_object_at(ball.x + ball.width, ball.y)
    lower_left  = window.get_object_at(ball.x,              ball.y + ball.height)
    lower_right = window.get_object_at(ball.x + ball.width, ball.y + ball.height)
    # TODO(sredmond): Be careful about not returning the paddle here.
    return upper_left or upper_right or lower_left or lower_right


@onmousemoved
def move_paddle(event):
    if event.x - paddle.width / 2 < 0:  # Flush left.
        paddle.x = 0
    elif event.x + paddle.width / 2 > window.width:  # Flush right.
        paddle.x = window.width - paddle.width
    else:  # Center paddle on mouse.
        paddle.x = event.x - paddle.width / 2


if __name__ == '__main__':
    make_bricks(window)

    while True:
        ball.move(vx, vy)
        pause(1000 / 60)  # 60 frames per second.

        # Check for wall collisions.
        if ball.x < 0 or ball.x + ball.width > window.width:
            vx = -vx  # Bounce horizontally.
        if ball.y < 0:
            vy = -vy  # Bounce vertically off of top of screen.
        if ball.y + ball.height > window.height:  # Passed the bottom of the screen. Game over!
            print('Game over!')
            break

        # Check for object collisions.
        colliding_object = get_colliding_object(window, ball)
        # Bounce off of the paddle.
        if colliding_object == paddle and vy > 0:
            vy = -vy
        # Bounce off of a brick.
        elif colliding_object != paddle and colliding_object is not None:
            vy = -vy
            window.remove(colliding_object)
