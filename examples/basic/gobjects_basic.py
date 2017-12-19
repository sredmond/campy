#!/usr/bin/env python3 -tt
"""
File: gobjects.py
-------------------------
This example program illustrates the use of the Python graphics library.
"""

from spgl.graphics.gwindow import *
from spgl.graphics.gtypes import *
from spgl.graphics.gobjects import *
# from spgl.graphics.gsounds import *
# from spgl.graphics.filelib import *

INTRO = """Welcome to a basic test of GObjects.

Press ENTER to begin.
"""
CONTINUE = "> "

input(INTRO)

window = GWindow()

# rect = GRect(45,54,10,10)
# window.add(rect)
# input(CONTINUE)

# rect.setFilled(True)
# input(CONTINUE)

# rect.move(100,100)
# input(CONTINUE)

# rect.setLocation(x=0,y=0)
# input(CONTINUE)

# rect.setColor(color = "RED")
# input(CONTINUE)

# rect.setColor(rgb = 0x00ff00)
# input(CONTINUE)

# rect.setVisible(False)
# input(CONTINUE)

# rect.setVisible(True)
# input(CONTINUE)

# window.repaint()
# input(CONTINUE)

# window.clear()
# input(CONTINUE)

# window.add(rect)
# rect2 = GRect(10, 10)
# gcomp = GCompound()
# gcomp.add(rect)
# gcomp.add(rect2)
# window.add(gcomp, 50, 50)
# input(CONTINUE)

# gcomp.remove(rect2)
# input(CONTINUE)

# gcomp.add(rect2)
# input(CONTINUE)

# gcomp.sendForward(rect)
# input(CONTINUE)

# gcomp.sendBackward(rect)
# input(CONTINUE)

# gcomp.sendToFront(rect)
# input(CONTINUE)

# gcomp.sendToBack(rect)
# input(CONTINUE)

# gcomp.removeAll()
# input(CONTINUE)

roundrect = GRoundRect(30, 30, 50, 50)
window.add(roundrect)
input(CONTINUE)

window.remove(roundrect)
rect3d = G3DRect(30, 30, 50, 50, True)
rect3d.setFilled(True)
window.add(rect3d)
input(CONTINUE)

rect3d.setRaised(False)
input(CONTINUE)

window.remove(rect3d)
oval = GOval(20, 40, 50, 50)
window.add(oval)
input(CONTINUE)

oval.setSize(40, 20)
input(CONTINUE)

oval.setFilled(True)
oval.setFillColor(rgb = 0x30c290)
input(CONTINUE)

window.remove(oval)
arc = GArc(50, 20, 30, 225, 50, 50)
window.add(arc)
input(CONTINUE)

arc.setStartAngle(0)
input(CONTINUE)

arc.setSweepAngle(90)
input(CONTINUE)

arc.setFilled(True)
arc.setFillColor(rgb = 0xffff00)
input(CONTINUE)

window.remove(arc)
line = GLine(0,0,50,50)
window.add(line)
input(CONTINUE)

line.setStartPoint(150,150)
input(CONTINUE)

line.setEndPoint(0,0)
input(CONTINUE)

# TODO(sredmond): Investigate return type of GImage
# window.remove(line)
# image = GImage("../res/images/python.jpg")
# window.add(image)

# input(CONTINUE)

# image.scale(sf = 3)

# input(CONTINUE)
# window.remove(image)

# label = GLabel("This is the Python client with a quote \\\"", 50, 50)
# window.add(label)

# input(CONTINUE)

# label.setFont("Arial-30")

# input(CONTINUE)

# label.setLabel("Changing the label now")

# input(CONTINUE)
# window.remove(label)

poly = GPolygon()
poly.addVertex(50, 50)
poly.addVertex(75, 25)
poly.addEdge(-20,100)
poly.addPolarEdge(15, 190)
window.add(poly)

input(CONTINUE)

poly.setFilled(True)
poly.setFillColor(rgb = 0xa01090)

input(CONTINUE)

window.remove(poly)

input(CONTINUE)

s = Sound("../res/sounds/fireball.wav")

input(CONTINUE)

s.play()

input(CONTINUE)

file = open_file_dialog(title = "Open", mode = "load", path=__file__)

input(CONTINUE)

window.remove(rect)

input(CONTINUE)

window.requestFocus()

input("Completed, press enter to close program")

window.close()
