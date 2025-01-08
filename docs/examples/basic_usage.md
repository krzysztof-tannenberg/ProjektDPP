# Przykłady użycia

## Podstawowe operacje

### Wczytywanie danych
```python
from json_loader import load_json_file

# Wczytaj dane z pliku
data = load_json_file("examples/sample_graph.json")
```

### Walidacja danych
```python
from json_loader import validate_graph_data

# Sprawdź poprawność struktury
if validate_graph_data(data):
    print("Struktura danych jest poprawna")
``` 