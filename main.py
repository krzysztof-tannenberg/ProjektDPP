from json_loader import load_graph_from_json
from shortest_path import dijkstra
from graph_UI import Graph, launch_gui
def main():
    # Załaduj graf z pliku
    graph = Graph()
    graph.load_from_file("data/network.json")

    # Uruchom GUI
    launch_gui(graph)

    graph = load_graph_from_json("data/network.json")
    print("Sieć autobusowa załadowana:")
    print(graph)

    start, target = "A", "C"
    path, distance = dijkstra(graph, start, target)
    print(f"Najkrótsza trasa z {start} do {target}: {path} (dystans: {distance})")

if __name__ == "__main__":
    main()
