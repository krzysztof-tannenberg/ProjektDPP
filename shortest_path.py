import heapq

def dijkstra(graph, start_node, end_node, weight="distance"):
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0
    previous_nodes = {node: None for node in graph.nodes}
    visited = set()
    priority_queue = [(0, start_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == end_node:
            break

        for neighbor, properties in graph.edges.get(current_node, {}).items():
            edge_weight = properties.get(weight, 1)  # Domyślnie "distance"
            new_distance = current_distance + edge_weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

    # Rekonstrukcja ścieżki
    path = []
    current = end_node
    while current:
        path.append(current)
        current = previous_nodes[current]
    path.reverse()

    return distances[end_node], path if distances[end_node] != float('inf') else []

