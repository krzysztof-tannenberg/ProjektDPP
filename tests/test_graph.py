"""
Moduł testów dla klasy Graph.

Ten moduł zawiera testy jednostkowe sprawdzające poprawność
implementacji podstawowych operacji na grafie.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graph import Graph

def test_add_node():
    """
    Test dodawania wierzchołka do grafu.
    
    Sprawdza czy:
    - Wierzchołek został dodany do grafu
    - Atrybuty wierzchołka są poprawne
    """
    graph = Graph()
    graph.add_node("A", "bus_stop", "Przystanek A")
    assert "A" in graph.nodes
    assert graph.nodes["A"]["type"] == "bus_stop"
    assert graph.nodes["A"]["name"] == "Przystanek A"

def test_remove_node():
    """
    Test usuwania wierzchołka z grafu.
    
    Sprawdza czy wierzchołek został poprawnie usunięty z grafu.
    """
    graph = Graph()
    graph.add_node("A", "bus_stop", "Przystanek A")
    graph.remove_node("A")
    assert "A" not in graph.nodes

def test_add_edge():
    """
    Test dodawania krawędzi do grafu.
    
    Sprawdza czy:
    - Krawędź została dodana
    - Atrybuty krawędzi są poprawne (distance, time)
    """
    graph = Graph()
    graph.add_node("A", "bus_stop", "Przystanek A")
    graph.add_node("B", "bus_stop", "Przystanek B")
    graph.add_edge("A", "B", distance=10, time=15)
    assert "B" in graph.edges["A"]
    assert graph.edges["A"]["B"]["distance"] == 10
    assert graph.edges["A"]["B"]["time"] == 15

def test_remove_edge():
    """
    Test usuwania krawędzi z grafu.
    
    Sprawdza czy:
    - Krawędź istnieje przed usunięciem
    - Krawędź została poprawnie usunięta
    """
    graph = Graph()
    graph.add_node("A", "bus_stop", "Przystanek A")
    graph.add_node("B", "bus_stop", "Przystanek B")
    graph.add_edge("A", "B", distance=10, time=15)
    assert "B" in graph.edges["A"]
    graph.remove_edge("A", "B")
    assert "B" not in graph.edges["A"]
