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

## Development

The codebase is organized into:
- `snake/entities/`: Game entities (Snake, Board, etc.)
- `snake/graph/`: Graph algorithms (Dijkstra, LSP, etc.)
- `snake/strategy/`: AI strategies
- `snake/strategy/filter/`: Move filters
- `snake/context/`: Game context management
