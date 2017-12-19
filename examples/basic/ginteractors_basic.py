#!/usr/bin/env python3 -tt
"""
Illustrates basic use of GInteractors.
"""

from spgl.graphics.gwindow import *
from spgl.graphics.gtypes import *
from spgl.gui.ginteractors import *

INTRO = """Welcome to a basic test of GInteractors.

Press ENTER to begin.
"""
CONTINUE = "> "

input(INTRO)

window = GWindow()

slider = GSlider()
window.add(slider)

input(CONTINUE)

slider2 = GSlider()
window.add(slider2)

input(CONTINUE)
window.clear()

button = GButton("I am a button label")
window.add(button)
input(CONTINUE)

button = GButton("I am a button label")
window.add(button)

input(CONTINUE)
window.clear()

textbox = GTextField()
textbox.setText("this is text in a textfield")
window.add(textbox)
input(CONTINUE)

chooser = GChooser()
chooser.setSize(100,200)
chooser.addItem('small')
chooser.addItem('large')
window.add(chooser)
input(CONTINUE)

window.close()
