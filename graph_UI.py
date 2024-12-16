import tkinter as tk
from tkinter import messagebox
import json
import matplotlib.pyplot as plt
import networkx as nx

class Graph:
    def __init__(self):
        self.nodes = {}  # Węzły
        self.edges = {}  # Krawędzie

    def add_node(self, node_id, node_type, name):
        """Dodanie węzła do grafu."""
        if node_id in self.nodes:
            raise ValueError(f"Node with ID {node_id} already exists.")
        self.nodes[node_id] = {"type": node_type, "name": name}

    def remove_node(self, node_id):
        """Usunięcie węzła z grafu."""
        if node_id not in self.nodes:
            raise ValueError(f"Node with ID {node_id} does not exist.")
        del self.nodes[node_id]
        self.edges.pop(node_id, None)
        for key in self.edges:
            self.edges[key] = [edge for edge in self.edges[key] if edge["to"] != node_id]

    def add_edge(self, from_node, to_node, **attributes):
        """Dodanie krawędzi do grafu."""
        if from_node not in self.nodes or to_node not in self.nodes:
            raise ValueError("Both nodes must exist in the graph.")
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append({"to": to_node, **attributes})

    def remove_edge(self, from_node, to_node):
        """Usunięcie krawędzi z grafu."""
        if from_node in self.edges:
            self.edges[from_node] = [edge for edge in self.edges[from_node] if edge["to"] != to_node]

    def to_json(self):
        """Konwertuje graf do formatu JSON."""
        nodes = [
            {"id": node_id, "type": node_data["type"], "name": node_data["name"]}
            for node_id, node_data in self.nodes.items()
        ]
        edges = [
            {"from": from_node, "to": edge["to"], "distance": edge.get("distance"), "time": edge.get("time")}
            for from_node, edges in self.edges.items()
            for edge in edges
        ]
        return {"nodes": nodes, "edges": edges}

    def save_to_file(self, filename):
        """Zapisuje graf do pliku JSON."""
        with open(filename, "w") as f:
            json.dump(self.to_json(), f, indent=2)

    def load_from_file(self, filename):
        """Wczytuje graf z pliku JSON."""
        with open(filename, "r") as f:
            data = json.load(f)
        self.nodes = {node["id"]: {"type": node["type"], "name": node["name"]} for node in data["nodes"]}
        self.edges = {}
        for edge in data["edges"]:
            if edge["from"] not in self.edges:
                self.edges[edge["from"]] = []
            self.edges[edge["from"]].append({"to": edge["to"], "distance": edge.get("distance"), "time": edge.get("time")})

def visualize_graph(graph):
    """Tworzy wizualizację grafu za pomocą matplotlib i networkx."""
    G = nx.DiGraph()  # Używamy skierowanego grafu

    # Dodanie węzłów
    for node_id, node_data in graph.nodes.items():
        G.add_node(node_id, label=node_data["name"], type=node_data["type"])

    # Dodanie krawędzi
    for from_node, edges in graph.edges.items():
        for edge in edges:
            G.add_edge(from_node, edge["to"], distance=edge.get("distance"), time=edge.get("time"))

    pos = nx.spring_layout(G)  # Automatyczne rozmieszczenie węzłów
    labels = nx.get_node_attributes(G, 'label')

    # Rysowanie węzłów i krawędzi
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=1500, font_size=10)
    nx.draw_networkx_labels(G, pos, labels, font_size=12, font_color="black")

    # Rysowanie etykiet krawędzi
    edge_labels = nx.get_edge_attributes(G, 'distance')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"D: {v}" for k, v in edge_labels.items()})

    plt.title("Graph Visualization")
    plt.show()

class GraphApp:
    def __init__(self, root, graph):
        self.graph = graph
        self.root = root
        self.root.title("Graph Network")
        self.create_widgets()

    def create_widgets(self):
        """Tworzy wszystkie elementy GUI."""
        tk.Label(self.root, text="Node ID:").grid(row=0, column=0)
        self.node_id_entry = tk.Entry(self.root)
        self.node_id_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Node Type:").grid(row=1, column=0)
        self.node_type_entry = tk.Entry(self.root)
        self.node_type_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Node Name:").grid(row=2, column=0)
        self.node_name_entry = tk.Entry(self.root)
        self.node_name_entry.grid(row=2, column=1)

        tk.Button(self.root, text="Add Node", command=self.add_node).grid(row=3, column=0, columnspan=2)
        tk.Button(self.root, text="Remove Node", command=self.remove_node).grid(row=4, column=0, columnspan=2)

        tk.Label(self.root, text="From Node (Edge):").grid(row=5, column=0)
        self.edge_from_entry = tk.Entry(self.root)
        self.edge_from_entry.grid(row=5, column=1)

        tk.Label(self.root, text="To Node (Edge):").grid(row=6, column=0)
        self.edge_to_entry = tk.Entry(self.root)
        self.edge_to_entry.grid(row=6, column=1)

        tk.Label(self.root, text="Distance (Edge):").grid(row=7, column=0)
        self.edge_distance_entry = tk.Entry(self.root)
        self.edge_distance_entry.grid(row=7, column=1)

        tk.Label(self.root, text="Time (Edge):").grid(row=8, column=0)
        self.edge_time_entry = tk.Entry(self.root)
        self.edge_time_entry.grid(row=8, column=1)

        tk.Button(self.root, text="Add Edge", command=self.add_edge).grid(row=9, column=0, columnspan=2)
        tk.Button(self.root, text="Remove Edge", command=self.remove_edge).grid(row=10, column=0, columnspan=2)
        tk.Button(self.root, text="Save to JSON", command=self.save_to_json).grid(row=11, column=0, columnspan=2)
        tk.Button(self.root, text="Visualize Graph", command=self.visualize).grid(row=12, column=0, columnspan=2)

    def add_node(self):
        try:
            node_id = self.node_id_entry.get()
            node_type = self.node_type_entry.get()
            node_name = self.node_name_entry.get()

            if not node_id or not node_type or not node_name:
                raise ValueError("All fields are required.")

            self.graph.add_node(node_id, node_type, node_name)
            messagebox.showinfo("Success", f"Node {node_name} added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_node(self):
        try:
            node_id = self.node_id_entry.get()
            if not node_id:
                raise ValueError("Node ID is required.")
            self.graph.remove_node(node_id)
            messagebox.showinfo("Success", f"Node {node_id} removed successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def add_edge(self):
        try:
            from_node = self.edge_from_entry.get()
            to_node = self.edge_to_entry.get()
            distance = self.edge_distance_entry.get()
            time = self.edge_time_entry.get()

            if not from_node or not to_node or not distance or not time:
                raise ValueError("All fields are required.")

            self.graph.add_edge(from_node, to_node, distance=int(distance), time=int(time))
            messagebox.showinfo("Success", f"Edge from {from_node} to {to_node} added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_edge(self):
        try:
            from_node = self.edge_from_entry.get()
            to_node = self.edge_to_entry.get()

            if not from_node or not to_node:
                raise ValueError("Both nodes for the edge are required.")

            self.graph.remove_edge(from_node, to_node)
            messagebox.showinfo("Success", f"Edge from {from_node} to {to_node} removed successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def save_to_json(self):
        try:
            self.graph.save_to_file("graph.json")
            messagebox.showinfo("Success", "Graph saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save graph: {e}")

    def visualize(self):
        """Wywołuje funkcję wizualizacji grafu."""
        try:
            visualize_graph(self.graph)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to visualize graph: {e}")


def launch_gui(graph):
    root = tk.Tk()
    app = GraphApp(root, graph)
    root.mainloop()

if __name__ == "__main__":
    graph = Graph()
    launch_gui(graph)
