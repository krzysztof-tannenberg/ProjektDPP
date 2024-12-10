import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graph import Graph
from shortest_path import dijkstra


def test_dijkstra_shortest_path():
    graph = Graph()
    graph.add_node("A", "bus_stop", "Przystanek A")
    graph.add_node("B", "bus_stop", "Przystanek B")
    graph.add_node("C", "bus_stop", "Przystanek C")
    graph.add_edge("A", "B", distance=5, time=10)
    graph.add_edge("B", "C", distance=3, time=6)
    graph.add_edge("A", "C", distance=10, time=15)

    distance, path = dijkstra(graph, "A", "C", weight="distance")
    assert distance == 8  # Najkrótsza droga: A -> B -> C
    assert path == ["A", "B", "C"]


def test_dijkstra_no_path():
    graph = Graph()
    graph.add_node("A", "bus_stop", "Przystanek A")
    graph.add_node("B", "bus_stop", "Przystanek B")
    distance, path = dijkstra(graph, "A", "B", weight="distance")
    assert distance == float("inf")
    assert path == []
