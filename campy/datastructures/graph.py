def error(str):
    print(str)


class Graph():
    def __init__(self, NodeType, ArcType, src=None):
        self._NodeType = NodeType
        self._ArcType = ArcType
        self.nodes = set()
        self.arcs = set()
        self.node_map = dict()
        # self.comparator = None  # TODO
        if src:
            self._deep_copy(src)

    def add_arc_by_nodes(self, n1, n2, named=False):
        if named:
            n1 = self._get_node_by_name(n1, member='add_arc')
            n2 = self._get_node_by_name(n1, member='add_arc')
        self._verify_existing_node(n1)
        self._verify_existing_node(n2)
        arc = self._ArcType()
        arc.start = n1
        arc.finish = n2

    def add_arc(self, arc):
        self._verify_not_none(arc)
        if not self._node_exists(arc.start):
            self.add_node(arc.start)
        if not self._node_exists(arc.end):
            self.add_node(arc.end)
        arc.start.arcs.add(arc)
        self.arcs.add(arc)
        return arc

    def add_node(self, node_info, named=False):
        if named:
            node = self._get_node_by_name(node_info, member='add_node')
            if not node:
                node = self._NodeType()
                node.arcs = set()
                node.name = node_info
        else:
            node = node_info
        self._verify_not_none(node, 'add_node')
        if node.name in self.node_map:
            error("Graph::add_node: node {} already exists".format(node.name))

        self.nodes.add(node)
        self.node_map[node.name] = node
        return node

    def clear(self):
        self.nodes = set()
        self.arcs = set()
        self.node_map = dict()

    def get_arc_set(self, node_info, named=False):
        if named:
            node = self._get_node_by_name(node_info)
        else:
            node = node_info
        self._verify_existing_node(node, member='get_arc_set')
        return node.arcs

    def get_neighbors(self, node_info, named=False):
        if named:
            node = self._get_node_by_name(node_info)
        else:
            node = node_info
        self._verify_existing_node(node, member='get_neighbors')
        return {arc.finish for arc in node.arcs}

    def is_connected(self, n1, n2, named=False):
        if named:
            n1 = self._get_node_by_name(n1, member='add_arc')
            n2 = self._get_node_by_name(n1, member='add_arc')
        # TODO error checking here
        for arc in n1.arcs:
            if arc.finish == n2:
                return True
        return False

    def is_empty(self):
        return len(self.nodes) == 0

    def remove_arc_by_nodes(self, n1, n2, named=False):
        if named:
            n1 = self._get_node_by_name(n1)
            n2 = self._get_node_by_name(n1)
            return self.remove_arc_by_nodes(n1, n2, named=False)
        if not self._node_exists(n1) or not self._node_exists(n2):
            return
        to_remove = []
        for arc in self.arcs:
            if arc.start == n1 and arc.finish == n2:
                to_remove.append(arc)

        for arc in to_remove:
            self.remove_arc(arc)

    def remove_arc(self, arc):
        arc.start.arcs.discard(arc)
        self.arcs.discard(arc)

    def remove_node(self, node, named=False):
        if named:
            node = self._get_node_by_name(node)
            self.remove_node(node, named=True)
        if not self._node_exists(node):
            return

        to_remove = []
        for arc in self.arcs:
            if arc.start == node or arc.end == node:
                to_remove.append(arc)
        for arc in to_remove:
            self.remove_arc(arc)

        self.nodes.discard(node)
        del self.node_map[node.name]

    def scan_arc_data(self):
        pass

    def scan_node_data(self):
        pass

    def scan_graph_entry(self, stream):
        pass

    def write_arc_data(self, ostream):
        pass

    def write_node_data(self, ostream):
        pass

    @property
    def size(self):
        pass

    # Implementation details, not useful to client
    def _deep_copy(self):
        pass

    def _get_node_by_name(self, name, member=''):
        node = self.node_map.get(name)
        if not node:
            error('Graph::{}: no node named {}'.format(member, name))
        return node

    def _graph_compare(self, other):
        pass

    def _arc_exists(self, arc):
        return arc in self.arcs

    def _node_exists(self, node):
        return node and self.node_map.get(node.name) == node

    def _verify_existing_node(self, node, member=''):
        self._verify_not_none(node, member)
        if not self._node_exists(node):
            error('Graph::{}: node not found in graph'.format(member))

    def _verify_not_none(self, value, member=''):
        if value is None:
            error('Graph::{}: parameter cannot be None'.format(member))

    def _scan_node(self, scanner):
        pass

    def __repr__(self):
        return "Graph"  # TODO obviously

    def __eq__(self, other):
        return False  # TODO, obviously

    # Iterating?
