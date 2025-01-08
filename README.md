# Network Graph Analyzer

## Opis projektu
Zaawansowany system do analizy i wizualizacji grafów sieciowych, umożliwiający interaktywne tworzenie, edycję i analizę struktur grafowych. Aplikacja oferuje graficzny interfejs użytkownika do zarządzania grafem oraz implementuje algorytm Dijkstry do znajdowania najkrótszych ścieżek.

## Główne funkcjonalności
- Interaktywny interfejs graficzny (GUI) do zarządzania grafem
- Dodawanie i usuwanie węzłów z określonymi atrybutami (ID, typ, nazwa)
- Tworzenie i usuwanie krawędzi z parametrami (dystans, czas)
- Wizualizacja grafu z wykorzystaniem biblioteki NetworkX
- Algorytm Dijkstry do znajdowania najkrótszych ścieżek
- Zapisywanie i wczytywanie grafów w formacie JSON
- Podświetlanie znalezionych ścieżek na wizualizacji
- Wyświetlanie aktualnej struktury grafu (lista węzłów i krawędzi)

## Wymagania systemowe
- Python 3.8+
- Biblioteki:
  - tkinter (GUI)
  - networkx (wizualizacja grafów)
  - matplotlib (renderowanie grafów)
  - pytest (testy)

## Instalacja
1. Klonowanie repozytorium:
```bash
git clone https://github.com/MarcinPop1/Projekt.git
cd network-graph-analyzer
```

2. Instalacja zależności:
```bash
pip install -r requirements.txt
```

## Uruchomienie
Aby uruchomić aplikację:
```bash
python graph_UI.py
```

## Format danych
Aplikacja wykorzystuje format JSON do przechowywania grafów. Przykładowa struktura:
```json
{
  "nodes": [
    {
      "id": "WAW",
      "type": "airport",
      "name": "Warszawa"
    },
    {
      "id": "KRK",
      "type": "airport",
      "name": "Kraków"
    }
  ],
  "edges": [
    {
      "from": "WAW",
      "to": "KRK",
      "distance": 300,
      "time": 45
    }
  ]
}
```

## Struktura projektu
```
project/
├── docs/                  # Dokumentacja
│   ├── api/              # Dokumentacja API
│   ├── examples/         # Przykłady użycia
│   └── guide/            # Przewodnik użytkownika
├── data/                 # Przykładowe dane
├── tests/                # Testy jednostkowe
├── graph_UI.py          # Główny plik interfejsu
├── graph.py             # Implementacja grafu
├── shortest_path.py     # Algorytm najkrótszej ścieżki
├── json_loader.py       # Obsługa plików JSON
└── requirements.txt     # Zależności projektu
```

## Dokumentacja
Pełna dokumentacja projektu dostępna jest w następujących formach:
- Dokumentacja API w docstringach kodu
- Wygenerowana dokumentacja na GitHub Pages
- Przewodnik użytkownika w katalogu docs/

## Testy
Uruchomienie testów jednostkowych:
```bash
python -m pytest tests/
```

## Przykład użycia programowego
```python
from graph import Graph
from json_loader import load_graph_from_json

# Utworzenie nowego grafu
graph = Graph()

# Dodanie węzłów
graph.add_node("WAW", "airport", "Warszawa")
graph.add_node("KRK", "airport", "Kraków")

# Dodanie krawędzi
graph.add_edge("WAW", "KRK", distance=300, time=45)

# Zapisanie grafu
graph.save_to_file("graph.json")

# Wczytanie grafu
loaded_graph = Graph()
loaded_graph.load_from_file("graph.json")
```

## Funkcje interfejsu
1. Zarządzanie węzłami:
   - Dodawanie węzłów (ID, typ, nazwa)
   - Usuwanie węzłów
   - Przeglądanie listy węzłów

2. Zarządzanie krawędziami:
   - Dodawanie krawędzi (węzeł początkowy, końcowy, dystans, czas)
   - Usuwanie krawędzi
   - Przeglądanie listy krawędzi

3. Analiza grafu:
   - Wyszukiwanie najkrótszej ścieżki między węzłami
   - Wizualizacja wyników
   - Podświetlanie znalezionej ścieżki

4. Operacje na plikach:
   - Zapisywanie grafu do pliku JSON
   - Wczytywanie grafu z pliku JSON




