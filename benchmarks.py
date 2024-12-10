import time
from shortest_path import dijkstra
from graph import Graph

def benchmark(graph, start, target, weight_key="distance"):
    start_time = time.time()
    dijkstra(graph, start, target, weight_key)
    end_time = time.time()
    return end_time - start_time
