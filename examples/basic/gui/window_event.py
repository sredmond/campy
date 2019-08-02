#!/usr/bin/env python3
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GLine, GOval
from campy.gui.events.window import onwindowresized

def main():
    window = GWindow(400, 400)

    # Awkward! We need a window before we can do anything.
    @onwindowresized
    def draw_x(event):
        event.window.clear()
        w, h = event.width, event.height
        x, y = event.x, event.y
        event.window.add(GLine(0, 0, w, h))
        event.window.add(GLine(w, 0, 0, h))

        event.window.add(GOval(200, 200, x=100-x, y=100-y))


if __name__ == '__main__':
    main()
