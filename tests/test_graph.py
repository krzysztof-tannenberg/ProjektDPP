import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graph import Graph

def test_add_node():
    graph = Graph()
    graph.add_node("A", "bus_stop", "Przystanek A")
    assert "A" in graph.nodes
    assert graph.nodes["A"]["type"] == "bus_stop"
    assert graph.nodes["A"]["name"] == "Przystanek A"

def test_remove_node():
    graph = Graph()
    graph.add_node("A", "bus_stop", "Przystanek A")
    graph.remove_node("A")
    assert "A" not in graph.nodes

def test_add_edge():
    graph = Graph()
    graph.add_node("A", "bus_stop", "Przystanek A")
    graph.add_node("B", "bus_stop", "Przystanek B")
    graph.add_edge("A", "B", distance=10, time=15)
    assert "B" in graph.edges["A"]
    assert graph.edges["A"]["B"]["distance"] == 10
    assert graph.edges["A"]["B"]["time"] == 15


def test_remove_edge():
    graph = Graph()
    graph.add_node("A", "bus_stop", "Przystanek A")
    graph.add_node("B", "bus_stop", "Przystanek B")
    graph.add_edge("A", "B", distance=10, time=15)

    # Sprawdzamy, czy krawędź istnieje przed usunięciem
    assert "B" in graph.edges["A"]

    # Usuwamy krawędź
    graph.remove_edge("A", "B")

    # Sprawdzamy, czy krawędź została usunięta
    assert "B" not in graph.edges["A"]
