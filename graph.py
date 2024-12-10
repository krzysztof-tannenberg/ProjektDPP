class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node_id, node_type, name):
        self.nodes[node_id] = {"type": node_type, "name": name}

    def add_edge(self, from_node, to_node, **kwargs):
        if from_node not in self.edges:
            self.edges[from_node] = {}
        self.edges[from_node][to_node] = kwargs

    def remove_node(self, node_id):
        self.nodes.pop(node_id, None)
        self.edges.pop(node_id, None)
        for edges in self.edges.values():
            edges[:] = [edge for edge in edges if edge["to"] != node_id]

    def remove_edge(self, from_node, to_node):
        if from_node in self.edges and to_node in self.edges[from_node]:
            del self.edges[from_node][to_node]

    def __str__(self):
        return f"Nodes: {self.nodes}\nEdges: {self.edges}"
