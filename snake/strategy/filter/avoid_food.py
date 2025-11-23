from typing import List
from snake.direction import Direction
from snake.strategy.filter.strategy_filter import StrategyFilter


class AvoidFood(StrategyFilter):
    def filter_moves(self, ctx, possible_moves: List[Direction]) -> None:
        board = ctx.board()
        food_set = set(ctx.state().food)

        i = 0
        while len(possible_moves) > 1 and i < len(possible_moves):
            direction = possible_moves[i]
            move_point = board.move_point_direction(ctx.state().me.head(), direction)

            if move_point in food_set:
                possible_moves.remove(direction)
            else:
                i += 1
