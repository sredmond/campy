from spgl.graphics.gobjects import GCompound, GLine, GLabel

from namesurferconstants import *

COLORS = ['#000000', '#FF0000', '#0000FF', '#FF00FF']

def label_for(name, rank, color):
    if rank > 0:
        label = GLabel('{} {}'.format(name, rank))
    else:
        label = GLabel('{} *'.format(name))
    label.setColor(color)
    return label

class NameSurferGraph(GCompound):

    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.draw_background()
        self._entries = []

    def _x_for_decade(self, n):
        return self.width * (n / NDECADES)

    def _y_for_rank(self, r):
        if r == 0:
            return self.height - GRAPH_MARGIN_SIZE
        else:
            return GRAPH_MARGIN_SIZE + (r / MAX_RANK) * (self.height - 2 * GRAPH_MARGIN_SIZE)

    def draw_entry(self, entry, color):
        for i, (rank_l, rank_r) in enumerate(zip(entry.ranks, entry.ranks[1:])):
            label = label_for(entry.name, rank_l, color)
            decade_x = self._x_for_decade(i)
            y_l = self._y_for_rank(rank_l)
            self.add(label, x=decade_x, y=y_l)

            y_r = self._y_for_rank(rank_r)
            line = GLine(decade_x, y_l, self._x_for_decade(i+1), y_r)
            line.setColor(color)
            self.add(line)
        # Add the final label.
        final_rank = entry.ranks[-1]
        label = label_for(entry.name, final_rank, color)
        final_rank_y = self._y_for_rank(final_rank)
        final_rank_x = self._x_for_decade(NDECADES - 1)
        self.add(label, x=final_rank_x, y=final_rank_y)

    def add_entry(self, entry):
        self._entries.append(entry)
        self.draw_entry(entry, COLORS[len(self._entries) % len(COLORS)])

    def draw_background(self):
        # Draw horizontal lines.
        self.add(GLine(0, GRAPH_MARGIN_SIZE, self.width, GRAPH_MARGIN_SIZE))
        self.add(GLine(0, self.height - GRAPH_MARGIN_SIZE, self.width, self.height-GRAPH_MARGIN_SIZE))

        for n in range(NDECADES):
            decade_x = self._x_for_decade(n)
            # Draw vertical lines.
            self.add(GLine(decade_x, 0, decade_x, self.height))
            # Draw labels.
            self.add(GLabel(str(START_DECADE + 10 * n)), x=decade_x, y=self.height) # TODO(sredmond): Should auto-convert to string.

    def clear(self):
        super().removeAll()
        self._entries = []
        self.draw_background()
