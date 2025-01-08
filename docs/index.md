# System Wizualizacji Grafów

## Wprowadzenie
System Wizualizacji Grafów to narzędzie stworzone w ramach zajęć z Dobrych Praktyk Programowania, służące do analizy i wizualizacji struktur grafowych.

## Szybki start

```python
from json_loader import load_json_file, validate_graph_data

# Wczytaj dane
data = load_json_file("graph.json")

# Zwaliduj strukturę
if validate_graph_data(data):
    print("Dane poprawne")
```

## Struktura dokumentacji
- **API** - dokumentacja techniczna modułów
- **Poradnik** - przewodnik krok po kroku 