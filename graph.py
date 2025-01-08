"""
Moduł implementujący podstawową strukturę grafu.

Ten moduł zawiera klasę Graph, która reprezentuje graf jako kolekcję
wierzchołków i krawędzi. Umożliwia podstawowe operacje na grafie,
takie jak dodawanie i usuwanie wierzchołków oraz krawędzi.

Example:
    >>> graph = Graph()
    >>> graph.add_node(1, "city", "Warszawa")
    >>> graph.add_edge(1, 2, distance=300)
"""

class Graph:
    """
    Klasa reprezentująca graf.

    Attributes:
        nodes (dict): Słownik wierzchołków grafu.
        edges (dict): Słownik krawędzi grafu.
    """

    def __init__(self):
        """
        Inicjalizuje pusty graf.
        """
        self.nodes = {}
        self.edges = {}

    def add_node(self, node_id, node_type, name):
        """
        Dodaje nowy wierzchołek do grafu.

        Args:
            node_id: Unikalny identyfikator wierzchołka.
            node_type (str): Typ wierzchołka.
            name (str): Nazwa wierzchołka.
        """
        self.nodes[node_id] = {"type": node_type, "name": name}

    def add_edge(self, from_node, to_node, **kwargs):
        """
        Dodaje nową krawędź do grafu.

        Args:
            from_node: Identyfikator wierzchołka początkowego.
            to_node: Identyfikator wierzchołka końcowego.
            **kwargs: Dodatkowe atrybuty krawędzi (np. distance, weight).

        Raises:
            KeyError: Gdy wierzchołek początkowy lub końcowy nie istnieje.
        """
        if from_node not in self.edges:
            self.edges[from_node] = {}
        self.edges[from_node][to_node] = kwargs

    def remove_node(self, node_id):
        """
        Usuwa wierzchołek z grafu.

        Args:
            node_id: Identyfikator wierzchołka do usunięcia.

        Note:
            Usuwa również wszystkie krawędzie związane z tym wierzchołkiem.
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node with ID {node_id} does not exist.")
        del self.nodes[node_id]
        # Usuń krawędzie wychodzące z usuwanego węzła
        self.edges.pop(node_id, None)
        # Usuń krawędzie prowadzące do usuwanego węzła
        for from_node in list(self.edges.keys()):
            if node_id in self.edges[from_node]:
                del self.edges[from_node][node_id]

    def remove_edge(self, from_node, to_node):
        """
        Usuwa krawędź z grafu.

        Args:
            from_node: Identyfikator wierzchołka początkowego.
            to_node: Identyfikator wierzchołka końcowego.
        """
        if from_node in self.edges and to_node in self.edges[from_node]:
            del self.edges[from_node][to_node]

    def __str__(self):
        """
        Zwraca tekstową reprezentację grafu.

        Returns:
            str: String zawierający informacje o wierzchołkach i krawędziach grafu.
        """
        return f"Nodes: {self.nodes}\nEdges: {self.edges}"
