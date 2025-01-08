"""
Moduł testów dla algorytmu najkrótszej ścieżki.

Ten moduł zawiera testy jednostkowe sprawdzające poprawność
implementacji algorytmu Dijkstry dla różnych przypadków użycia.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graph import Graph
from shortest_path import dijkstra


def test_dijkstra_shortest_path():
    """
    Test znajdowania najkrótszej ścieżki w grafie.
    
    Sprawdza czy:
    - Algorytm znajduje najkrótszą ścieżkę
    - Długość ścieżki jest poprawna
    - Kolejność wierzchołków w ścieżce jest prawidłowa
    """
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
    """
    Test zachowania algorytmu gdy nie istnieje ścieżka między wierzchołkami.
    
    Sprawdza czy:
    - Algorytm zwraca nieskończoność jako dystans
    - Zwracana ścieżka jest pustą listą
    """
    graph = Graph()
    graph.add_node("A", "bus_stop", "Przystanek A")
    graph.add_node("B", "bus_stop", "Przystanek B")
    distance, path = dijkstra(graph, "A", "B", weight="distance")
    assert distance == float("inf")
    assert path == []
