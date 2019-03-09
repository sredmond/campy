from campy.graphics.gobjects import GLabel, GRect, GLine
from campy.graphics.gwindow import GWindow
from campy.graphics.gevents import *

from campy.gui.ginteractors import GButton, GTextField

from namesurferdatabase import NameSurferDatabase
from namesurfergraph import NameSurferGraph
from namesurferconstants import *

if __name__ == '__main__':
    window = GWindow(width=APPLICATION_WIDTH, height=APPLICATION_HEIGHT)

    # Add interactors
    infield = GTextField(10)
    graph_button = GButton('Graph')
    clear_button = GButton('Clear!')

    window.addToRegion(GLabel('Name'), "NORTH")
    window.addToRegion(infield, "NORTH")
    window.addToRegion(graph_button, "NORTH")
    window.addToRegion(clear_button, "NORTH")

    # Construct NSDB and NSGraph
    db = NameSurferDatabase(NAMES_DATA_FILE)
    graph = NameSurferGraph(window.width, window.height - 40)
    window.add(graph)

    while True:
        event = get_next_event()
        if event.event_type == EventType.ACTION_PERFORMED:
            if event.source == graph_button:
                entry = db[infield.text]
                if not entry:
                    continue
                graph.add_entry(entry)
            if event.source == clear_button:
                graph.clear()
