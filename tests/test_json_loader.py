"""
Moduł testów dla funkcji ładowania danych JSON.

Ten moduł zawiera testy jednostkowe sprawdzające poprawność
wczytywania i przetwarzania danych z plików JSON.
"""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graph import Graph
from json_loader import load_graph_from_json


def test_load_graph_from_json():
    """
    Test wczytywania grafu z pliku JSON.
    
    Sprawdza czy:
    - Dane są poprawnie wczytywane z pliku
    - Węzły są poprawnie utworzone
    - Krawędzie są poprawnie utworzone
    - Atrybuty węzłów i krawędzi są zachowane
    
    Note:
        Test tworzy tymczasowy plik JSON, który jest usuwany po zakończeniu testu.
    """
    test_json = {
        "nodes": [
            {"id": "A", "type": "bus_stop", "name": "Przystanek Główna"},
            {"id": "B", "type": "bus_stop", "name": "Przystanek Młynarska"}
        ],
        "edges": [
            {"from": "A", "to": "B", "distance": 3, "time": 6}
        ]
    }

    with open("test_network.json", "w") as f:
        json.dump(test_json, f)

    graph = load_graph_from_json("test_network.json")

    # Test węzłów
    assert "A" in graph.nodes
    assert graph.nodes["A"]["name"] == "Przystanek Główna"

    # Test krawędzi
    assert "B" in graph.edges["A"]
    assert graph.edges["A"]["B"]["distance"] == 3
    assert graph.edges["A"]["B"]["time"] == 6

    os.remove("test_network.json")
