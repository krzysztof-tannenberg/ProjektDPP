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

def visualize_graph(graph, highlight_path=None):
    """
    Tworzy wizualizację grafu za pomocą matplotlib i networkx.
    
    Args:
        graph: Obiekt grafu do wizualizacji
        highlight_path: Lista węzłów tworzących ścieżkę do podświetlenia
    """
    plt.clf()  # Wyczyść poprzedni wykres
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

    # Kolory węzłów
    node_colors = ["lightblue" if node not in (highlight_path or []) else "lightgreen" for node in G.nodes()]
    
    # Kolory krawędzi
    edge_colors = []
    if highlight_path:
        for u, v in G.edges():
            if u in highlight_path and v in highlight_path and highlight_path.index(u) + 1 == highlight_path.index(v):
                edge_colors.append("green")
            else:
                edge_colors.append("gray")
    else:
        edge_colors = ["gray"] * len(G.edges())

    # Rysowanie węzłów i krawędzi
    nx.draw(G, pos, 
            with_labels=True, 
            node_color=node_colors, 
            edge_color=edge_colors,
            node_size=2000, 
            font_size=10,
            arrowsize=20,
            width=2)
            
    nx.draw_networkx_labels(G, pos, labels, font_size=12, font_color="black")

    # Rysowanie etykiet krawędzi
    edge_labels = {}
    for (u, v, data) in G.edges(data=True):
        dist = data.get('distance', '')
        time = data.get('time', '')
        edge_labels[(u, v)] = f"D:{dist}\nT:{time}"
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)

    plt.title("Network Graph Visualization")
    plt.axis('off')  
    plt.tight_layout()  
    plt.show()

from shortest_path import dijkstra

class GraphApp:
    def __init__(self, root, graph):
        self.graph = graph
        self.root = root
        self.root.title("Network Graph Analyzer")
        
        # Załaduj przykładowy graf jeśli istnieje
        try:
            self.graph.load_from_file("graph.json")
        except:
            pass
            
        self.create_widgets()
        self.update_lists()  # Inicjalna aktualizacja list

    def create_widgets(self):
        """Tworzy wszystkie elementy GUI."""
        # Główny kontener z możliwością przewijania
        self.canvas = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        # Konfiguracja przewijania
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Tworzenie okna w canvas z ramką
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pakowanie elementów
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Dodanie obsługi przewijania myszką
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Główny kontener
        main_container = tk.Frame(self.scrollable_frame, padx=10, pady=10)
        main_container.pack(expand=True, fill='both')
        
        # Lewa strona - operacje
        left_frame = tk.Frame(main_container)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Frame dla list
        lists_frame = tk.LabelFrame(left_frame, text="Network Structure", padx=5, pady=5)
        lists_frame.pack(fill='x', pady=(0, 10))
        
        # Lista węzłów
        tk.Label(lists_frame, text="Nodes:").pack()
        self.nodes_list = tk.Text(lists_frame, height=8, width=40)
        self.nodes_list.pack(fill='x', pady=(0, 10))
        
        # Lista krawędzi
        tk.Label(lists_frame, text="Edges:").pack()
        self.edges_list = tk.Text(lists_frame, height=8, width=40)
        self.edges_list.pack(fill='x')
        
        # Frame dla operacji na węzłach
        node_frame = tk.LabelFrame(left_frame, text="Node Operations", padx=5, pady=5)
        node_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(node_frame, text="Node ID:").pack()
        self.node_id_entry = tk.Entry(node_frame)
        self.node_id_entry.pack(fill='x')
        
        tk.Label(node_frame, text="Node Type:").pack()
        self.node_type_entry = tk.Entry(node_frame)
        self.node_type_entry.pack(fill='x')
        
        tk.Label(node_frame, text="Node Name:").pack()
        self.node_name_entry = tk.Entry(node_frame)
        self.node_name_entry.pack(fill='x')
        
        button_frame = tk.Frame(node_frame)
        button_frame.pack(fill='x', pady=5)
        tk.Button(button_frame, text="Add Node", command=self.add_node).pack(side='left', expand=True, padx=2)
        tk.Button(button_frame, text="Remove Node", command=self.remove_node).pack(side='left', expand=True, padx=2)
        
        # Frame dla operacji na krawędziach
        edge_frame = tk.LabelFrame(left_frame, text="Edge Operations", padx=5, pady=5)
        edge_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(edge_frame, text="From Node:").pack()
        self.edge_from_entry = tk.Entry(edge_frame)
        self.edge_from_entry.pack(fill='x')
        
        tk.Label(edge_frame, text="To Node:").pack()
        self.edge_to_entry = tk.Entry(edge_frame)
        self.edge_to_entry.pack(fill='x')
        
        tk.Label(edge_frame, text="Distance:").pack()
        self.edge_distance_entry = tk.Entry(edge_frame)
        self.edge_distance_entry.pack(fill='x')
        
        tk.Label(edge_frame, text="Time:").pack()
        self.edge_time_entry = tk.Entry(edge_frame)
        self.edge_time_entry.pack(fill='x')
        
        button_frame = tk.Frame(edge_frame)
        button_frame.pack(fill='x', pady=5)
        tk.Button(button_frame, text="Add Edge", command=self.add_edge).pack(side='left', expand=True, padx=2)
        tk.Button(button_frame, text="Remove Edge", command=self.remove_edge).pack(side='left', expand=True, padx=2)
        
        # Frame dla wyszukiwania najkrótszej ścieżki
        path_frame = tk.LabelFrame(left_frame, text="Find Shortest Path", padx=5, pady=5)
        path_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(path_frame, text="Start Node:").pack()
        self.path_start_entry = tk.Entry(path_frame)
        self.path_start_entry.pack(fill='x')
        
        tk.Label(path_frame, text="End Node:").pack()
        self.path_end_entry = tk.Entry(path_frame)
        self.path_end_entry.pack(fill='x')
        
        tk.Button(path_frame, text="Find Path", command=self.find_shortest_path).pack(fill='x', pady=5)
        
        # Frame dla wyników
        self.result_frame = tk.LabelFrame(left_frame, text="Path Results", padx=5, pady=5)
        self.result_frame.pack(fill='x')
        self.result_text = tk.Text(self.result_frame, height=5, width=40)
        self.result_text.pack(fill='x')
        
        # Przyciski operacji na grafie
        operations_frame = tk.Frame(left_frame)
        operations_frame.pack(fill='x', pady=10)
        tk.Button(operations_frame, text="Save to JSON", command=self.save_to_json).pack(fill='x', pady=2)
        tk.Button(operations_frame, text="Load from JSON", command=self.load_from_json).pack(fill='x', pady=2)
        tk.Button(operations_frame, text="Visualize Graph", command=self.visualize).pack(fill='x', pady=2)

    def update_lists(self):
        """Aktualizuje listy węzłów i krawędzi w interfejsie."""
        # Aktualizacja listy węzłów
        self.nodes_list.delete(1.0, tk.END)
        if not self.graph.nodes:
            self.nodes_list.insert(tk.END, "No nodes in the graph")
        else:
            for node_id, node_data in self.graph.nodes.items():
                self.nodes_list.insert(tk.END, 
                    f"ID: {node_id} | Type: {node_data['type']} | Name: {node_data['name']}\n")
        
        # Aktualizacja listy krawędzi
        self.edges_list.delete(1.0, tk.END)
        if not any(self.graph.edges.values()):
            self.edges_list.insert(tk.END, "No edges in the graph")
        else:
            for from_node, edges in self.graph.edges.items():
                for edge in edges:
                    self.edges_list.insert(tk.END, 
                        f"From: {from_node} -> To: {edge['to']} | Distance: {edge.get('distance')} | Time: {edge.get('time')}\n")

    def add_node(self):
        try:
            node_id = self.node_id_entry.get()
            node_type = self.node_type_entry.get()
            node_name = self.node_name_entry.get()

            if not node_id or not node_type or not node_name:
                raise ValueError("All fields are required.")

            self.graph.add_node(node_id, node_type, node_name)
            messagebox.showinfo("Success", f"Node {node_name} added successfully!")
            self.update_lists()  
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_node(self):
        try:
            node_id = self.node_id_entry.get()
            if not node_id:
                raise ValueError("Node ID is required.")
            self.graph.remove_node(node_id)
            messagebox.showinfo("Success", f"Node {node_id} removed successfully!")
            self.update_lists()  
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
            self.update_lists() 
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
            self.update_lists()  
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def save_to_json(self):
        try:
            self.graph.save_to_file("graph.json")
            messagebox.showinfo("Success", "Graph saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save graph: {e}")

    def find_shortest_path(self):
        """Znajduje i wyświetla najkrótszą ścieżkę między dwoma węzłami."""
        try:
            start = self.path_start_entry.get()
            end = self.path_end_entry.get()
            
            if not start or not end:
                raise ValueError("Both start and end nodes are required.")
                
            distance, path = dijkstra(self.graph, start, end)
            
            if not path:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "No path found between these nodes.")
                return
                
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Distance: {distance}\nPath: {' -> '.join(path)}")
            
           
            self.visualize(highlight_path=path)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def load_from_json(self):
        """Wczytuje graf z pliku JSON."""
        try:
            self.graph.load_from_file("graph.json")
            messagebox.showinfo("Success", "Graph loaded successfully!")
            self.update_lists()  
            self.visualize()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load graph: {e}")

    def _on_mousewheel(self, event):
        """Obsługa przewijania myszką."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def visualize(self, highlight_path=None):
        """Wywołuje funkcję wizualizacji grafu."""
        try:
            visualize_graph(self.graph, highlight_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to visualize graph: {e}")

def launch_gui(graph):
    root = tk.Tk()
    app = GraphApp(root, graph)
    root.mainloop()

if __name__ == "__main__":
    graph = Graph()
    launch_gui(graph)
