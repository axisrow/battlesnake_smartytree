from typing import List, Set
from snake.direction import Direction
from snake.graph.cc import CC
from snake.strategy.filter.strategy_filter import StrategyFilter


class AvoidClosedSpaces(StrategyFilter):
    def filter_moves(self, ctx, possible_moves: List[Direction]) -> None:
        if len(possible_moves) <= 1:
            return

        head = ctx.state().me.head()
        board = ctx.board()
        board_graph = ctx.board_graph()

        cc = CC(board_graph, ctx.state().me.health)
        area_sizes = [0] * len(possible_moves)

        expanding_clusters = self.get_expanding_clusters(ctx, cc)

        for i in range(len(possible_moves)):
            move_dst = board.value_of_point(board.move_point_direction(head, possible_moves[i]))
            area_sizes[i] = cc.component_size(move_dst)
            if cc.get_id(move_dst) in expanding_clusters:
                area_sizes[i] = float('inf')

        max_area = max(area_sizes)
        to_remove = []
        for i in range(len(possible_moves) - 1, -1, -1):
            if area_sizes[i] < max_area:
                to_remove.append(possible_moves[i])

        for direction in to_remove:
            possible_moves.remove(direction)

    def get_expanding_clusters(self, ctx, cc: CC) -> Set[int]:
        expanding_clusters = set()
        for snake in ctx.state().snakes:
            tail = snake.tail()
            expanding_clusters.add(cc.get_id(ctx.board().value_of_point(tail)))
            for edge in ctx.board_graph().points_around(tail, 1):
                expanding_clusters.add(cc.get_id(edge.get_destination()))
        return expanding_clusters
