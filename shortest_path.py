"""
Moduł implementujący algorytmy znajdowania najkrótszej ścieżki w grafie.

Ten moduł zawiera implementacje różnych algorytmów do znajdowania najkrótszej
ścieżki między wierzchołkami w grafie, w tym algorytm Dijkstry i A*.

Attributes:
    INF (float): Wartość reprezentująca nieskończoność w algorytmach.
"""

from typing import Dict, List, Tuple, Set
import heapq

INF = float('inf')

class Graph:
    def __init__(self):
        self.nodes = {}  # Słownik wierzchołków
        self.edges = {}  # Słownik krawędzi: {wierzchołek: lista krawędzi}

    def add_node(self, id, type, name):
        self.nodes[id] = {"type": type, "name": name}

    def add_edge(self, from_node, to_node, **attributes):
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append({"to": to_node, **attributes})

def dijkstra(graph, start: str, end: str) -> Tuple[float, List[str]]:
    """
        Implementacja algorytmu Dijkstry do znajdowania najkrótszej ścieżki.

        Args:
            graph (Dict): Słownik reprezentujący graf w formie list sąsiedztwa.
            start (int): Wierzchołek początkowy.
            end (int): Wierzchołek końcowy.

        Returns:
            Tuple[List[int], float]: Krotka zawierająca listę wierzchołków tworzących
                najkrótszą ścieżkę oraz jej długość.

        Raises:
            ValueError: Gdy start lub end nie istnieją w grafie.
        """
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    previous_nodes = {node: None for node in graph.nodes}
    visited = set()
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == end:
            break

        if current_node not in graph.edges:
            continue

        for edge in graph.edges[current_node]:
            neighbor = edge["to"]
            if neighbor in visited:
                continue

            edge_weight = float(edge.get("distance", float('inf')))
            new_distance = current_distance + edge_weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

    path = []
    current = end
    while current:
        path.append(current)
        current = previous_nodes[current]
    path.reverse()

    return distances[end], path if distances[end] != float('inf') else []

def find_path(prev: Dict[int, int], start: int, end: int) -> List[int]:
    """
    Odtwarza ścieżkę na podstawie słownika poprzedników.

    Args:
        prev (Dict[int, int]): Słownik poprzedników dla każdego wierzchołka.
        start (int): Wierzchołek początkowy.
        end (int): Wierzchołek końcowy.

    Returns:
        List[int]: Lista wierzchołków tworzących ścieżkę od start do end.
    """
    path = []
    current = end
    while current:
        path.append(current)
        current = prev[current]
    path.reverse()
    return path
