"""
Moduł do przeprowadzania testów wydajnościowych.

Ten moduł zawiera funkcje do mierzenia czasu wykonania
algorytmów grafowych, w szczególności algorytmu najkrótszej ścieżki.

Example:
    >>> graph = Graph()
    >>> time_taken = benchmark(graph, "A", "B")
    >>> print(f"Czas wykonania: {time_taken:.4f} sekund")
"""

import time
from shortest_path import dijkstra
from graph import Graph

def benchmark(graph: Graph, start: str, target: str, weight_key: str = "distance") -> float:
    """
    Mierzy czas wykonania algorytmu najkrótszej ścieżki.

    Funkcja wykonuje algorytm Dijkstry i mierzy czas jego wykonania
    od momentu rozpoczęcia do zakończenia.

    Args:
        graph (Graph): Graf, na którym wykonywany jest algorytm.
        start (str): Wierzchołek początkowy.
        target (str): Wierzchołek końcowy.
        weight_key (str, optional): Klucz wagi krawędzi. Domyślnie "distance".

    Returns:
        float: Czas wykonania algorytmu w sekundach.

    Example:
        >>> g = Graph()
        >>> g.add_node("A", "city", "Warszawa")
        >>> g.add_node("B", "city", "Kraków")
        >>> g.add_edge("A", "B", distance=300)
        >>> time = benchmark(g, "A", "B")
    """
    start_time = time.time()
    dijkstra(graph, start, target, weight_key)
    end_time = time.time()
    return end_time - start_time
