from abc import ABC, abstractmethod
from snake.point import Point
from snake.direction import Direction


class BoardContext(ABC):
    def __init__(self, height: int, width: int):
        self._height = height
        self._width = width

    def height(self) -> int:
        return self._height

    def width(self) -> int:
        return self._width

    def value_of_point(self, p: Point) -> int:
        return self._width * p.y + p.x

    def from_value(self, point_value: int) -> Point:
        x = point_value % self._width
        y = point_value // self._width
        return Point(x, y)

    def is_valid(self, p: Point) -> bool:
        if p is None:
            return False
        return 0 <= p.x < self._width and 0 <= p.y < self._height

    @abstractmethod
    def move_point(self, source: Point, vector: Point) -> Point:
        pass

    def move_point_direction(self, s: Point, direction: Direction) -> Point:
        return self.move_point(s, direction.offset())


class BorderedBoardContext(BoardContext):
    def __init__(self, height: int, width: int):
        super().__init__(height, width)

    def move_point(self, source: Point, vector: Point) -> Point:
        point = Point(source.x + vector.x, source.y + vector.y)
        if not self.is_valid(point):
            return None
        return point


class WrappedBoardContext(BoardContext):
    def __init__(self, height: int, width: int):
        super().__init__(height, width)

    def move_point(self, source: Point, vector: Point) -> Point:
        return Point(
            (source.x + vector.x + self.width()) % self.width(),
            (source.y + vector.y + self.height()) % self.height()
        )
