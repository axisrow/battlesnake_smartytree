from typing import List
from snake.direction import Direction
from snake.strategy.filter.strategy_filter import StrategyFilter


class AvoidBorders(StrategyFilter):
    def filter_moves(self, ctx, possible_moves: List[Direction]) -> None:
        board = ctx.board()
        head = ctx.state().me.head()

        to_remove = []
        for direction in possible_moves:
            if board.move_point_direction(head, direction) is None:
                to_remove.append(direction)

        for direction in to_remove:
            possible_moves.remove(direction)
