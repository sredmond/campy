#!/usr/bin/env python3 -tt
"""
File: examples/basic/interactors.py
-----------------------------------
Sample program demonstrating the use of interactors
"""
from campy.graphics.gwindow import *
from campy.graphics.gobjects import *
from campy.gui.ginteractors import *
from campy.graphics.gevents import *

window = GWindow(width=1000, height=600)
addInteract = GButton("Add")
removeInteract = GButton("Remove")
filledInteract = GCheckBox("Filled: ")
captionInteract = GTextField(20)
redInteract = GSlider(0,255,0)
greenInteract = GSlider(0,255,0)
blueInteract = GSlider(0,255,0)
sizeInteract = GChooser()
sizeInteract.addItem("Small")
sizeInteract.addItem("Medium")
sizeInteract.addItem("Large")

filledInteract.action_command = "fillChange"
captionInteract.action_command = "captionChange"
redInteract.action_command = "redChange"
greenInteract.action_command = "greenChange"
blueInteract.action_command = "blueChange"
sizeInteract.action_command = "sizeChange"
sizeInteract.selected_item = "Medium"

window.addToRegion(addInteract, "SOUTH")
window.addToRegion(removeInteract, "SOUTH")
window.addToRegion(filledInteract, "SOUTH")
window.addToRegion(captionInteract, "SOUTH")
window.addToRegion(redInteract, "SOUTH")
window.addToRegion(greenInteract, "SOUTH")
window.addToRegion(blueInteract, "SOUTH")
window.addToRegion(sizeInteract, "SOUTH")

objX = window.width/2-75
objY = window.height/2-75
obj = GOval(150,150, objX, objY)
window.add(obj)
cap = GLabel("")
capX = objX + obj.width  /2 - cap.width / 2
capY = objY + obj.height + 15 + cap.ascent
cap.location = (capX, capY)
window.add(cap)

red = "00"
green = "00"
blue = "00"

while(True):
	e = wait_for_event()
	if(e.event_type == EventType.ACTION_PERFORMED):
		if(e.source == addInteract):
			window.add(obj)
			window.add(cap)
		elif(e.source == removeInteract):
			window.remove(obj)
			window.remove(cap)
		elif(e.source == filledInteract):
			if(filledInteract.selected):
				print("filling")
				obj.filled = True
			else:
				print("unfilling")
				obj.filled = False
		elif(e.source == captionInteract):
			label = captionInteract.text
			cap.label = label
			capX = objX + obj.width / 2 - cap.width / 2
			capY = objY + obj.height + 15 + cap.ascent
			cap.location = (capX, capY)
			# TODO(sredmond): Continue modifying to attribute access from here on out
		elif(e.source == redInteract):
			red = str(hex(redInteract.getValue()))
			red = red[2:]
			if(red == "0"): red = "00"
			color = "#" + red + green + blue
			obj.setFillColor(color = color)
		elif(e.source == greenInteract):
			green = str(hex(greenInteract.getValue()))
			green = green[2:]
			if(green == "0"): green = "00"
			color = "#" + red + green + blue
			obj.setFillColor(color = color)
		elif(e.source == blueInteract):
			blue = str(hex(blueInteract.getValue()))
			blue = blue[2:]
			if(blue == "0"): blue = "00"
			color = "#" + red + green + blue
			obj.setFillColor(color = color)
		elif(e.source == sizeInteract):
			item = sizeInteract.getSelectedItem().strip()
			if(item == "Small"):
				obj.setSize(60, 60)
				objX = window.getWidth()/2-30
				objY = window.getHeight()/2-30
				obj.setLocation(x=objX, y=objY)
				capX = objX + obj.getWidth()/2 - cap.getWidth()/2
				capY = objY + obj.getHeight() + 15 + cap.getFontAscent()
				cap.setLocation(x=capX, y=capY)
			elif(item == "Medium"):
				obj.setSize(150, 150)
				objX = window.getWidth()/2-75
				objY = window.getHeight()/2-75
				obj.setLocation(x=objX, y=objY)
				capX = objX + obj.getWidth()/2 - cap.getWidth()/2
				capY = objY + obj.getHeight() + 15 + cap.getFontAscent()
				cap.setLocation(x=capX, y=capY)
			elif(item == "Large"):
				obj.setSize(400, 400)
				objX = window.getWidth()/2-200
				objY = window.getHeight()/2-200
				obj.setLocation(x=objX, y=objY)
				capX = objX + obj.getWidth()/2 - cap.getWidth()/2
				capY = objY + obj.getHeight() + 15 + cap.getFontAscent()
				cap.setLocation(x=capX, y=capY)
