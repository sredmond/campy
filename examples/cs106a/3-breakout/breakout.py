#!/usr/bin/env python
"""Breakout! A graphical game of epic proportions.

Partial Python implementation of a game of Breakout, a brick-breaking game
popularized by Eric Roberts' CS106A course at Stanford.
"""
# TODO(sredmond): Avoid import-star.
from campy.graphics.gwindow import *
from campy.graphics.gobjects import *
from campy.graphics.gevents import *
from campy.graphics.gtimer import *
from campy.util.randomgenerator import *

import time

window = GWindow()
window.title = 'Breakout'

ball = GOval(20, 20, x=window.width / 2, y=window.height / 2, )
ball.filled = True
window.add(ball)
vx = 2.7
vy = 3.0

paddle = GRect(125, 15, x=window.width / 2, y=window.height - 50)
paddle.filled = True
window.add(paddle)

spacer = 5
brick_width = (window.width -  9 * spacer) / 10

for i in range(10):
	for j in range(10):
		brick = GRect(brick_width, 15, x=j * (brick_width + spacer), y=50 + i * (15 + spacer))
		brick.filled = True
		if i < 2:
			brick.fill_color = "RED"
		elif i < 4:
			brick.fill_color = "ORANGE"
		elif i < 6:
			brick.fill_color = "YELLOW"
		elif i < 8:
			brick.fill_color = "GREEN"
		elif i<10:
			brick.fill_color = "BLUE"
		window.add(brick)

timer = GTimer(milliseconds=15)

import sys
timer.start()
while True:
	e = get_next_event ()
	if(e.getEventType() == EventType.MOUSE_MOVED):
		newX = e.getX()
		if(newX - paddle.getWidth()/2 > 0 and \
			newX + paddle.getWidth()/2 < window.getWidth()):
			paddle.setLocation(x = newX - paddle.getWidth()/2, y = paddle.getY())
		elif(newX - paddle.getWidth()/2 < 0):
			paddle.setLocation(x = 0, y = paddle.getY())
		elif(newX + paddle.getWidth()/2 > window.getWidth()):
			paddle.setLocation(x = window.getWidth() - paddle.getWidth(), \
								y = paddle.getY())
	elif(e.getEventType() == EventType.TIMER_TICKED):
		ball.move(vx, vy)

		# check for wall collisions
		if(ball.getX() + ball.getWidth() > window.getWidth() or \
			ball.getX() < 0):
			vx = -vx
		if(ball.getY() + ball.getHeight() > window.getHeight() or \
			ball.getY() < 0):
			vy = -vy

		obj1 = window.getObjectAt(ball.getX()-1, ball.getY()-1)
		obj2 = window.getObjectAt(ball.getX() + ball.getWidth() + 1, ball.getY()-1)
		obj3 = window.getObjectAt(ball.getX()-1, ball.getY() + ball.getHeight()+1)
		obj4 = window.getObjectAt(ball.getX() + ball.getWidth() + 1,  ball.getY() + ball.getHeight()+1)
		# check for paddle collisions
		if(window.getObjectAt(ball.getX(), ball.getY()) == paddle or \
			window.getObjectAt(ball.getX() + ball.getWidth(), ball.getY()) == paddle or \
			window.getObjectAt(ball.getX(), ball.getY() + ball.getHeight()) == paddle or \
			window.getObjectAt(ball.getX() + ball.getWidth(), ball.getY() + ball.getHeight()) == paddle):
			if(vy > 0):
				vy = -vy
		elif(obj1 != None and obj1 != paddle):
			vy = -vy
			window.remove(obj1)
		elif(obj2 != None and obj2 != paddle):
			vy = -vy
			window.remove(obj2)
		elif(obj3 != None and obj3 != paddle):
			vy = -vy
			window.remove(obj3)
		elif(obj4 != None and obj4 != paddle):
			vy = -vy
			window.remove(obj4)
	elif(e.getEventType() == EventType.KEY_TYPED):
		initRandomSeed()
		window.remove(ball)
		ball = GOval(20,20, window.getWidth()/2, window.getHeight()/2)
		ball.setFilled(True)
		window.add(ball)
		vx = randomReal(2,4)
		if(randomChance(.5)): vx = -vx
		vy = 3.0


