from typing import List
from snake.direction import Direction
from snake.entities.snake import Snake
from snake.strategy.strategy import Strategy
from snake.strategy.utils import Utils
from snake.graph.cc import CC
from snake.strategy.filter.area_control import AreaControl
from snake.strategy.filter.avoid_borders import AvoidBorders
from snake.strategy.filter.avoid_obstacles import AvoidObstacles
from snake.strategy.filter.avoid_closed_spaces_without_expansion import AvoidClosedSpacesWithoutExpansion


class Constrictor(Strategy):
    def find_move(self, ctx) -> Direction:
        possible_moves = self._init_constrictor_mode_possible_moves(ctx)

        if not self.is_snake_alone(ctx):
            AreaControl().filter_moves(ctx, possible_moves)
            return Utils.move_forward(ctx, possible_moves)

        return Utils.fill_space(ctx, possible_moves)

    def is_snake_alone(self, ctx) -> bool:
        me = ctx.state().me
        cc = CC(ctx.board_graph(), me.health)

        clusters = set(self._get_snake_clusters(ctx, me, cc))

        for snake in ctx.state().snakes:
            if snake == me:
                continue

            if any(cluster in clusters for cluster in self._get_snake_clusters(ctx, snake, cc)):
                return False

        return True

    def _init_constrictor_mode_possible_moves(self, ctx) -> List[Direction]:
        possible_moves = Utils.init_directions(ctx, ctx.state().me)
        AvoidBorders().filter_moves(ctx, possible_moves)
        AvoidObstacles().filter_moves(ctx, possible_moves)
        AvoidClosedSpacesWithoutExpansion().filter_moves(ctx, possible_moves)
        return possible_moves

    def _get_snake_clusters(self, ctx, snake: Snake, cc: CC) -> List[int]:
        board = ctx.board()
        clusters = []

        for d in Utils.init_directions(ctx, snake):
            p = board.move_point_direction(snake.head(), d)
            if p:
                clusters.append(cc.get_id(board.value_of_point(p)))

        return clusters
