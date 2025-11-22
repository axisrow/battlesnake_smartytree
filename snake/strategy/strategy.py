from abc import ABC, abstractmethod
from snake.direction import Direction


class Strategy(ABC):
    @abstractmethod
    def find_move(self, ctx) -> Direction:
        pass
