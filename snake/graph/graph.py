from typing import List, Dict, TYPE_CHECKING
from snake.point import Point
from snake.direction import Direction
from snake.graph.directed_edge import DirectedEdge

if TYPE_CHECKING:
    from snake.context.board_context import BoardContext
    from snake.context.context import Context


class Graph:
    MOVE_WEIGHT = 1
    DEFAULT_HAZARD_WEIGHT = 14

    def __init__(self, board: 'BoardContext', hazard_weight: int):
        self.board = board
        self.hazard_weight = hazard_weight
        self.obstacles: Dict[int, int] = {}
        self.hazards: Dict[int, int] = {}

    @staticmethod
    def create_generic_game_graph(context: 'Context') -> 'Graph':
        from snake.context.context import Context

        game_state_context = context.state()
        graph = Graph(context.board(), game_state_context.hazard_damage)

        for snake in game_state_context.snakes:
            ttl = 0
            body = snake.body

            for i in range(len(body) - 1, -1, -1):
                if ttl > 0:
                    obstacle = body[i]
                    graph.obstacles[graph.board.value_of_point(obstacle)] = ttl
                ttl += 1

        for p in game_state_context.hazards:
            v = graph.board.value_of_point(p)
            weight = graph.hazard_weight + graph.hazards.get(v, 0)
            graph.hazards[graph.board.value_of_point(p)] = weight

        return graph

    @staticmethod
    def create_food_hazard_graph(ctx: 'Context') -> 'Graph':
        graph = Graph(ctx.board(), ctx.state().hazard_damage)

        for p in ctx.state().food:
            graph.hazards[graph.board.value_of_point(p)] = Graph.DEFAULT_HAZARD_WEIGHT

        return graph

    def V(self) -> int:
        return self.board.width() * self.board.height()

    def adj(self, v: int | Point, time: int = 0) -> List[DirectedEdge]:
        if isinstance(v, int):
            return self.adj_point(self.board.from_value(v), time)
        else:
            return self.adj_point(v, time)

    def adj_point(self, start_point: Point, time: int) -> List[DirectedEdge]:
        return self.points_around(start_point, time)

    def is_obstacle(self, p: Point | int) -> bool:
        if isinstance(p, Point):
            return self.board.value_of_point(p) in self.obstacles
        else:
            return p in self.obstacles

    def points_around(self, start_point: Point, time: int) -> List[DirectedEdge]:
        start_point_v = self.board.value_of_point(start_point)
        result = []

        for direction in Direction:
            moved_point = self.board.move_point_direction(start_point, direction)
            if moved_point and self.board.is_valid(moved_point):
                destination = self.board.value_of_point(moved_point)
                if destination not in self.obstacles or self.obstacles[destination] < time:
                    weight = self.get_move_weight(destination)
                    result.append(DirectedEdge(start_point_v, destination, weight))

        return result

    def get_move_weight(self, destination: int) -> float:
        return self.hazards.get(destination, self.MOVE_WEIGHT)

    def __str__(self) -> str:
        sb = []
        for v in range(self.V()):
            adj_list = self.adj(v, 0)
            if not adj_list:
                continue

            sb.append(str(self.board.from_value(v)))
            sb.append(" -> ")
            sb.append(", ".join([str(self.board.from_value(d.get_destination())) for d in adj_list]))
            sb.append("\n")

        return "".join(sb)
