import random
from typing import List, Optional
from snake.direction import Direction
from snake.point import Point
from snake.entities.snake import Snake
from snake.graph.directed_edge import DirectedEdge
from snake.graph.dijkstra import Dijkstra
from snake.graph.lsp import LSP


class Utils:
    @staticmethod
    def init_directions(context, snake: Snake) -> List[Direction]:
        forward_direction = snake.head_direction()

        return [
            forward_direction,
            forward_direction.rotate_clockwise(),
            forward_direction.rotate_counterclockwise()
        ]

    @staticmethod
    def init_possible_directions(context, snake: Snake) -> List[Direction]:
        from snake.strategy.filter.avoid_problems import AvoidProblems

        directions = Utils.init_directions(context, snake)
        AvoidProblems().filter_moves(context, directions)

        return directions

    @staticmethod
    def move_forward(context, possible_moves: List[Direction]) -> Direction:
        if len(possible_moves) == 0:
            return context.state().me.head_direction()

        return possible_moves[0]

    @staticmethod
    def move_towards(context, possible_moves: List[Direction], target: Point) -> Direction:
        if len(possible_moves) == 1:
            return Utils.move_forward(context, possible_moves)

        possible_moves_to_target = set(
            d for d in context.state().me.head().direction_to(target)
            if d in possible_moves
        )

        if len(possible_moves_to_target) > 0:
            possible_moves = list(possible_moves_to_target)

        return Utils.move_forward(context, possible_moves)

    @staticmethod
    def move_thru_path(context, possible_moves: List[Direction],
                       path: Optional[List[DirectedEdge]]) -> Direction:
        if not path or len(path) == 0:
            return Utils.move_forward(context, possible_moves)

        next_point = context.board().from_value(path[0].get_destination())
        return Utils.move_towards(context, possible_moves, next_point)

    @staticmethod
    def random_move(possible_moves: List[Direction]) -> Direction:
        return random.choice(possible_moves)

    @staticmethod
    def find_closest_point(points: List[Point], dijkstra: Dijkstra) -> Optional[Point]:
        if len(points) == 0:
            return None

        distances = [(dijkstra.find_distance(p), p) for p in points]
        distances.sort(key=lambda x: x[0])

        return distances[0][1]

    @staticmethod
    def find_closest_point_waypoints(points: List[Point], waypoints: List[Dijkstra]) -> Optional[Point]:
        if len(points) == 0:
            return None

        distances = []
        for p in points:
            total_distance = sum(d.find_distance(p) for d in waypoints)
            distances.append((total_distance, p))

        distances.sort(key=lambda x: x[0])
        return distances[0][1]

    @staticmethod
    def fill_space(ctx, possible_moves: List[Direction]) -> Direction:
        path = LSP(ctx.board_graph(), ctx.state().me.head()).find_longest_path()
        if path:
            return Utils.move_thru_path(ctx, possible_moves, path)

        return Utils.move_forward(ctx, possible_moves)
