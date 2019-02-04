#!/usr/bin/env python3
"""Demonstrate the use of a GWindow for non-interactive drawing."""
from campy.graphics.gwindow import GWindow

window = GWindow()
window.draw_line(0, 0, window.width, window.height)
window.draw_line(window.width, 0, 0, window.height)

midx, midy = window.width // 2, window.height // 2
pt = window.draw_polar_line(midx, midy, 100, 60)
pt = window.draw_polar_line(pt.x, pt.y, 100, -60)
window.draw_polar_line(pt.x, pt.y, 100, 180)

window.draw_oval(0, 0, 100, 100)
window.fill_oval(25, 25, 50, 50)

window.draw_rect(0, 0, 100, 100)
window.fill_rect(25, 25, 50, 50)

