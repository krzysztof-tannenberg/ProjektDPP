# Pierwsze kroki

## Podstawowe użycie

1. Przygotuj plik JSON z danymi grafu:
```json
{
    "nodes": [
        {"id": 1, "type": "city", "name": "Warszawa"},
        {"id": 2, "type": "city", "name": "Kraków"}
    ],
    "edges": [
        {"from": 1, "to": 2, "distance": 300, "time": 180}
    ]
}
```

2. Wczytaj i zwaliduj dane:
```python
from json_loader import load_json_file, validate_graph_data

data = load_json_file("graph.json")
if validate_graph_data(data):
    print("Dane wczytane poprawnie")
``` 