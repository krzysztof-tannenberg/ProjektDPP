from json_loader import load_graph_from_json
from shortest_path import dijkstra

def main():
    graph = load_graph_from_json("data/network.json")
    print("Sieć autobusowa załadowana:")
    print(graph)

    start, target = "A", "D"
    path, distance = dijkstra(graph, start, target)
    print(f"Najkrótsza trasa z {start} do {target}: {path} (dystans: {distance})")

if __name__ == "__main__":
    main()
