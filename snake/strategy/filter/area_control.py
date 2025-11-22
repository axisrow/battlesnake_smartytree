from typing import List
from snake.direction import Direction
from snake.graph.dijkstra import Dijkstra
from snake.strategy.filter.strategy_filter import StrategyFilter
from snake.strategy.utils import Utils


class AreaControl(StrategyFilter):
    def filter_moves(self, ctx, possible_moves: List[Direction]) -> None:
        if len(possible_moves) <= 1:
            return

        me = ctx.state().me
        d = Dijkstra(ctx.board_graph(), me.head())

        targets = [snake.head() for snake in ctx.state().snakes if snake != me]

        target = Utils.find_closest_point(targets, d)
        path = d.find_path(target)

        direction = Utils.move_thru_path(ctx, possible_moves, path)
        possible_moves.clear()
        possible_moves.append(direction)
