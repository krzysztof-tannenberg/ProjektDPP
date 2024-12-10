import json
from graph import Graph

def load_graph_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    graph = Graph()

    for node in data["nodes"]:
        graph.add_node(node["id"], node["type"], node["name"])

    for edge in data["edges"]:
        graph.add_edge(edge["from"], edge["to"], distance=edge["distance"], time=edge["time"])

    return graph

