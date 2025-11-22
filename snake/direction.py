from enum import Enum
from snake.point import Point


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    _DIRECTION_TO_OFFSET = {
        1: Point(0, 1),   # UP
        2: Point(0, -1),  # DOWN
        3: Point(-1, 0),  # LEFT
        4: Point(1, 0)    # RIGHT
    }

    _DIRECTION_TO_STRING = {
        1: "up",
        2: "down",
        3: "left",
        4: "right"
    }

    def offset(self) -> Point:
        return self._DIRECTION_TO_OFFSET[self.value]

    def __str__(self) -> str:
        return self._DIRECTION_TO_STRING[self.value]

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
