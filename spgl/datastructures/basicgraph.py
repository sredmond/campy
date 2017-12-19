# TODO(sredmond): Implement hash.

class Vertex():
    """Canonical Vertex (Node) structure used by :class:`BasicGraph`.

    """
    # TODO(sredmond): Investigate whether VertexGen in the C++ library is meaningful.
    def __init__(self, name):
        self.name = name
        self.reset_data()

    ## TODO Copy constructor

    def reset_data(self):
        self.arcs = set()  # {Edge}
        self.visited = False
        self.previous = None
        self.cost = 0.0
        self._color = 0  # UNCOLORED

    @property
    def color(self):
        """Return the color of this vertex."""
        return self._m_color

    @color.setter
    def color(self, c):
        self._color = c
        # self.notify_observers()  ## TODO Add observables

    # Convenient aliases
    @property
    def edges(self):
        return self.arcs

    @property
    def weight(self):
        return self.cost

    def __repr__(self):
        return "Vertex(name={}, cost={}, visited={}, previous={}, neighbors={{}})".format(
            self.name,
            self.cost,
            self.visited,
            self.previous.name if self.previous else 'None',
            ', '.join(edge.finish.name for edge in self.edges)
        )

    ## TODO equality override

# Node = Vertex  # Should we allow class-level aliasing like Marty?

class Edge():
    def __init__(self, start=None, finish=None, cost=0.0):
        self.start = start
        self.finish = finish
        self.cost = cost
        self.reset_data()

    def reset_data(self):
        self.visited = False

    # Convenient aliases
    @property
    def end(self):
        return self.finish

    @end.setter
    def end(self, value):
        self.finish = value

    @end.deleter
    def end(self):
        del self.end

    @property
    def weight(self):
        return self.cost

    def __repr__(self):
        return "Edge(start={}, finish={}, cost={}, visited={})".format(
            self.start.name if self.start else 'None',
            self.finish.name if self.finish else 'None',
            self.cost,
            self.visited
        )

# Arc = Edge  # Should we alias this too?

class BasicGraph():
    def __init__(self):
        self._reset_enabled = True
