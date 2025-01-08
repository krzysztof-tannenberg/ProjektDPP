# JSON Loader API

## Opis modułu
Moduł `json_loader.py` odpowiada za wczytywanie i walidację danych w formacie JSON.

## Funkcje

### load_json_file
```python
def load_json_file(file_path: str) -> Dict[str, Any]
```

Wczytuje i parsuje plik JSON.

### validate_graph_data
```python
def validate_graph_data(data: Dict[str, Any]) -> bool
```

Sprawdza poprawność struktury danych grafu. 