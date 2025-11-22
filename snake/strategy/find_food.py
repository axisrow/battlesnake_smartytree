from snake.direction import Direction
from snake.strategy.strategy import Strategy
from snake.strategy.utils import Utils
from snake.graph.dijkstra import Dijkstra


class FindFood(Strategy):
    def find_move(self, ctx) -> Direction:
        game_ctx = ctx.state()
        me = game_ctx.me

        dijkstra = Dijkstra(ctx.board_graph(), me.head())

        targets = list(game_ctx.food)
        targets.extend([snake.head() for snake in game_ctx.snakes if snake.length < me.length])

        closest_target = Utils.find_closest_point(targets, dijkstra)

        path = dijkstra.find_path(closest_target) if closest_target else None
        if not path or dijkstra.find_distance(closest_target) > me.health:
            from snake.strategy.fill import Fill
            return Fill().find_move(ctx)

        board = ctx.board()
        possible_moves = Utils.init_possible_directions(ctx, me)

        if len(possible_moves) == 1:
            return Utils.move_forward(ctx, possible_moves)

        if not path or dijkstra.find_distance(closest_target) > me.health:
            targets = [
                board.move_point_direction(me.head(), direction)
                for direction in possible_moves
                if board.move_point_direction(me.head(), direction) is not None
            ]
            closest_target = Utils.find_closest_point(targets, dijkstra)
            path = dijkstra.find_path(closest_target) if closest_target else None

        return Utils.move_thru_path(ctx, possible_moves, path)
