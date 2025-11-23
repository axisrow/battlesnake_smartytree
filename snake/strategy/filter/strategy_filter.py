from abc import ABC, abstractmethod
from typing import List
from snake.direction import Direction


class StrategyFilter(ABC):
    @abstractmethod
    def filter_moves(self, ctx, possible_moves: List[Direction]) -> None:
        pass
