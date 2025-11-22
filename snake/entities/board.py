from typing import List
from snake.point import Point
from snake.entities.snake import Snake


class Board:
    def __init__(self, height: int, width: int, food: List[Point],
                 hazards: List[Point], snakes: List[Snake]):
        self.height = height
        self.width = width
        self.food = food
        self.hazards = hazards
        self.snakes = snakes

    def __str__(self) -> str:
        board = [['.' for _ in range(self.width)] for _ in range(self.height)]

        for snake_idx, snake in enumerate(self.snakes):
            for p in snake.body:
                if 0 <= p.y < self.height and 0 <= p.x < self.width:
                    board[p.y][p.x] = str(snake_idx + 1)

            head = snake.head()
            if 0 <= head.y < self.height and 0 <= head.x < self.width:
                board[head.y][head.x] = 'H'

        result = []
        for y in range(self.height - 1, -1, -1):
            result.append(''.join(board[y]))

        return '\n'.join(result)

    @classmethod
    def from_dict(cls, data: dict) -> 'Board':
        return cls(
            height=data['height'],
            width=data['width'],
            food=[Point.from_dict(p) for p in data.get('food', [])],
            hazards=[Point.from_dict(p) for p in data.get('hazards', [])],
            snakes=[Snake.from_dict(s) for s in data.get('snakes', [])]
        )

    def to_dict(self) -> dict:
        return {
            'height': self.height,
            'width': self.width,
            'food': [p.to_dict() for p in self.food],
            'hazards': [p.to_dict() for p in self.hazards],
            'snakes': [s.to_dict() for s in self.snakes]
        }
