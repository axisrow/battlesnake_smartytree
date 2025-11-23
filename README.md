# Smarty Tree battlesnake

A Python-based Battlesnake implementation with multiple strategies and game modes.

## Setup

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Run Battlesnake Server

### Development
```bash
python server.py
```

### Production (with Gunicorn)
```bash
gunicorn -b 0.0.0.0:8080 -w 4 server:app
```

### Docker
```bash
docker build -t battlesnake-smartytree .
docker run -p 8080:8080 battlesnake-smartytree
```

## Configuration

Edit `config.yaml` to customize your snake:
- `name`: Snake name
- `color`: Snake color (hex code)
- `head`: Snake head style
- `tail`: Snake tail style
- `strategy`: Default strategy (FindFood, FindTail, Cycle, Fill)

## Supported Battlesnake Modes
- Standard
- Constrictor
- Solo
- Wrapped

## Strategies
- **FindFood**: Seeks food and smaller snakes
- **FindTail**: Follows own tail
- **Cycle**: Advanced cycling strategy
- **Fill**: Space-filling algorithm
- **Constrictor**: Constrictor mode specific strategy

## How It Works
- On startup the Flask app reads `config.yaml`, builds the default strategy via `StrategyFactory`, and exposes `/`, `/start`, `/move`, `/end`.
- Each `/move` call converts the Battlesnake JSON into domain objects (`GameState`, `Board`, `Snake`) and wraps them in a `Context` that knows board geometry (bordered vs wrapped) and hazard damage.
- A weighted `Graph` is built per turn: snake bodies become time-decaying obstacles, hazards add extra move cost, and neighbors come from board-aware offsets.
- Strategies operate on that graph:
  - **FindFood** runs Dijkstra from your head to food or weaker snake heads, falling back to **Fill** if paths are unsafe.
  - **FindTail** chases your own tail to stay alive when space is tight.
  - **Cycle** keeps movement loops open, selecting detours that preserve freedom.
  - **Fill** floods remaining safe cells to maximize survivability.
  - **Constrictor** prioritizes wrapping lanes while respecting hazards and body growth.
- Ruleset detection swaps in **Constrictor** for constrictor modes and **Fill** for solo; otherwise the configured default strategy is used.

## Development

The codebase is organized into:
- `snake/entities/`: Game entities (Snake, Board, etc.)
- `snake/graph/`: Graph algorithms (Dijkstra, LSP, etc.)
- `snake/strategy/`: AI strategies
- `snake/strategy/filter/`: Move filters
- `snake/context/`: Game context management

## README на русском

Python-реализация Battlesnake с несколькими стратегиями и режимами игры.

### Установка
```bash
pip install -r requirements.txt
```

### Запуск сервера Battlesnake
- Дев: `python server.py`
- Прод (Gunicorn): `gunicorn -b 0.0.0.0:8080 -w 4 server:app`
- Docker: `docker build -t battlesnake-smartytree .` затем `docker run -p 8080:8080 battlesnake-smartytree`

### Конфигурация
Правьте `config.yaml`:
- `name`, `color`, `head`, `tail` — оформление змейки
- `strategy` — стратегия по умолчанию (FindFood, FindTail, Cycle, Fill)

### Поддерживаемые режимы
Standard, Constrictor, Solo, Wrapped.

### Стратегии
- **FindFood**: ищет еду и головы более слабых змей
- **FindTail**: следует за собственным хвостом
- **Cycle**: поддерживает циклические маршруты, чтобы не запираться
- **Fill**: заполняет свободное пространство, максимизируя выживаемость
- **Constrictor**: заточена под Constrictor-режим

### Как работает
- При старте Flask читает `config.yaml`, собирает стратегию через `StrategyFactory` и открывает маршруты `/`, `/start`, `/move`, `/end`.
- На `/move` входной JSON превращается в `GameState`/`Board`/`Snake`, затем в `Context`, который знает геометрию доски и урон опасностей.
- Каждый ход строится взвешенный `Graph`: тела змей становятся временными препятствиями, опасные клетки получают повышенную стоимость, соседние клетки зависят от типа доски (границы или тор).
- Стратегии работают поверх графа (Dijkstra в **FindFood**, погоня за хвостом в **FindTail**, циклы в **Cycle**, заливка в **Fill**, приоритет коридоров в **Constrictor**). Ruleset автоматически переключает стратегию: Constrictor/Wrap → **Constrictor**, Solo → **Fill**, иначе — стратегия из конфигурации.

### Структура проекта
- `snake/entities/`: сущности игры
- `snake/graph/`: графовые алгоритмы (Dijkstra, LSP и др.)
- `snake/strategy/`: стратегии ИИ
- `snake/strategy/filter/`: фильтры ходов
- `snake/context/`: управление контекстом игры
