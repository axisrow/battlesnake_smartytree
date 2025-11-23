from enum import Enum
from snake.point import Point


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    def offset(self) -> Point:
        return _DIRECTION_TO_OFFSET[self]

    def __str__(self) -> str:
        return _DIRECTION_TO_STRING[self]

    def rotate_clockwise(self) -> 'Direction':
        rotation_map = {
            Direction.UP: Direction.RIGHT,
            Direction.DOWN: Direction.LEFT,
            Direction.RIGHT: Direction.DOWN,
            Direction.LEFT: Direction.UP
        }
        return rotation_map[self]

    def rotate_counterclockwise(self) -> 'Direction':
        rotation_map = {
            Direction.DOWN: Direction.RIGHT,
            Direction.UP: Direction.LEFT,
            Direction.LEFT: Direction.DOWN,
            Direction.RIGHT: Direction.UP
        }
        return rotation_map[self]

    def invert(self) -> 'Direction':
        inversion_map = {
            Direction.DOWN: Direction.UP,
            Direction.UP: Direction.DOWN,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        return inversion_map[self]


_DIRECTION_TO_OFFSET = {
    Direction.UP: Point(0, 1),
    Direction.DOWN: Point(0, -1),
    Direction.LEFT: Point(-1, 0),
    Direction.RIGHT: Point(1, 0),
}

_DIRECTION_TO_STRING = {
    Direction.UP: "up",
    Direction.DOWN: "down",
    Direction.LEFT: "left",
    Direction.RIGHT: "right",
}
