from __future__ import annotations
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from snake.direction import Direction


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def manhattan_to(self, to: Point) -> int:
        return abs(self.x - to.x) + abs(self.y - to.y)

    def direction_to(self, destination: Point) -> List[Direction]:
        from snake.direction import Direction

        dx = destination.x - self.x
        dy = destination.y - self.y
        ret = []

        if dx < 0:
            ret.append(Direction.LEFT)
        elif dx > 0:
            ret.append(Direction.RIGHT)

        if dy < 0:
            ret.append(Direction.DOWN)
        elif dy > 0:
            ret.append(Direction.UP)

        return ret

    def __str__(self) -> str:
        return f"{{{self.y}, {self.x}}}"

    def __eq__(self, other) -> bool:
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __lt__(self, other: Point) -> bool:
        if self.y != other.y:
            return self.y < other.y
        return self.x < other.x

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    @classmethod
    def from_dict(cls, data: dict) -> Point:
        return cls(x=data['x'], y=data['y'])

    def to_dict(self) -> dict:
        return {'x': self.x, 'y': self.y}
