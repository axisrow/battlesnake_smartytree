from typing import List
from snake.direction import Direction
from snake.strategy.filter.strategy_filter import StrategyFilter
from snake.strategy.filter.avoid_borders import AvoidBorders
from snake.strategy.filter.avoid_obstacles import AvoidObstacles
from snake.strategy.filter.avoid_closed_spaces import AvoidClosedSpaces


class AvoidProblems(StrategyFilter):
    def filter_moves(self, ctx, possible_moves: List[Direction]) -> None:
        AvoidBorders().filter_moves(ctx, possible_moves)
        AvoidObstacles().filter_moves(ctx, possible_moves)
        AvoidClosedSpaces().filter_moves(ctx, possible_moves)
