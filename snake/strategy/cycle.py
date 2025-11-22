from typing import List
from snake.direction import Direction
from snake.strategy.strategy import Strategy
from snake.strategy.utils import Utils
from snake.graph.dijkstra import Dijkstra
from snake.graph.graph import Graph


class Cycle(Strategy):
    CORNER = 0

    def find_move(self, ctx) -> Direction:
        me = ctx.state().me

        if me.length == 0:
            return Direction.DOWN

        possible_moves = Utils.init_possible_directions(ctx, me)

        if len(possible_moves) == 1:
            return possible_moves[0]

        head = me.head()
        tail = me.tail()

        dijkstra_head = Dijkstra(ctx.board_graph(), head)
        closest_food = Utils.find_closest_point(ctx.state().food, dijkstra_head)

        if ctx.turn() > 700:
            return Utils.fill_space(ctx, possible_moves)

        food_reserve = 3
        if closest_food and dijkstra_head.find_distance(closest_food) + food_reserve > me.health:
            return Utils.move_thru_path(ctx, possible_moves, dijkstra_head.find_path(closest_food))

        # Do not enter closed without insufficient health
        tail_offset = 1 if me.is_next_to_tail() else 0
        if len(ctx.board_graph().adj(me.tail(tail_offset), 0)) <= 1:
            if me.health <= me.length:
                return Utils.move_thru_path(ctx, possible_moves, dijkstra_head.find_path(closest_food))

        # Try to avoid food
        food_hazard = Graph.create_food_hazard_graph(ctx)
        dijkstra = Dijkstra(food_hazard, head)

        if dijkstra.find_distance(self.CORNER) != float('inf'):
            path = dijkstra.find_path(self.CORNER)
            return Utils.move_thru_path(ctx, possible_moves, path)

        if me.is_next_to_tail() and not me.is_expanding():
            return Utils.move_towards(ctx, possible_moves, tail)

        return self._move_to_tail(ctx, possible_moves, dijkstra)

    def _move_to_tail(self, ctx, possible_moves: List[Direction], dijkstra: Dijkstra) -> Direction:
        around_tail = [
            edge.get_destination()
            for edge in ctx.board_graph().points_around(ctx.state().me.tail(1), 0)
        ]

        if len(around_tail) < 1:
            return Utils.random_move(possible_moves)

        destination = around_tail[0]
        for p in around_tail:
            if dijkstra.find_distance(destination) > dijkstra.find_distance(p):
                destination = p

        path = dijkstra.find_path(destination)
        return Utils.move_thru_path(ctx, possible_moves, path)
