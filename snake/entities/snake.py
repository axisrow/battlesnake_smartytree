from typing import List
from snake.point import Point
from snake.direction import Direction


class Snake:
    def __init__(self, id: str, name: str, health: int, body: List[Point],
                 length: int = None, head: Point = None, shout: str = ""):
        self.id = id
        self.name = name
        self.shout = shout
        self.health = health
        self.length = length if length is not None else len(body)
        self.body = body
        self._head = head

    def head(self) -> Point:
        return self.body[0] if self.body else self._head

    def head_direction(self) -> Direction:
        if len(self.body) < 2:
            return Direction.UP

        neck = self.body[1]
        directions = neck.direction_to(self.head())

        if not directions:
            return Direction.UP

        direction = directions[0]
        if neck.manhattan_to(self.head()) > 1:
            direction = direction.invert()

        return direction

    def tail(self, offset: int = 0) -> Point:
        return self.body[len(self.body) - 1 - offset]

    def is_next_to_tail(self) -> bool:
        return self.head().manhattan_to(self.tail()) == 1

    def is_expanding(self) -> bool:
        if len(self.body) < 2:
            return False
        return self.tail(1) == self.tail()

    def __eq__(self, other) -> bool:
        if isinstance(other, Snake):
            return self.id == other.id
        return False

    @classmethod
    def from_dict(cls, data: dict) -> 'Snake':
        return cls(
            id=data['id'],
            name=data['name'],
            health=data['health'],
            body=[Point.from_dict(p) for p in data['body']],
            length=data.get('length', len(data['body'])),
            head=Point.from_dict(data['head']) if 'head' in data else None,
            shout=data.get('shout', '')
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'health': self.health,
            'body': [p.to_dict() for p in self.body],
            'length': self.length,
            'head': self.head().to_dict(),
            'shout': self.shout
        }
