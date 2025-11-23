from typing import Dict, Set, List, Optional
from snake.point import Point
from snake.entities.snake import Snake
from snake.graph.dijkstra import Dijkstra


class VoronoiDiagram:
    def __init__(self, ctx):
        self.snakes_areas: Dict[str, Set[Point]] = {}

        for snake in ctx.state().snakes:
            self.snakes_areas[snake.id] = set()

        self._build_voronoi_diagram(ctx)

    def _build_voronoi_diagram(self, ctx):
        g = ctx.board_graph()
        dijkstras = [Dijkstra(g, snake.head()) for snake in ctx.state().snakes]

        for y in range(ctx.board().height()):
            for x in range(ctx.board().width()):
                p = Point(x, y)
                if g.is_obstacle(p):
                    continue

                snake = self._find_area_controlling_snake(ctx.state().snakes, dijkstras, p)
                if snake:
                    self.snakes_areas[snake.id].add(p)

    @staticmethod
    def _find_area_controlling_snake(
            snakes: List[Snake],
            dijkstras: List[Dijkstra],
            p: Point
    ) -> Optional[Snake]:
        closest_snake_ind = 0
        closest_snake_distance = dijkstras[closest_snake_ind].find_distance(p)
        closest_snake_size = snakes[closest_snake_ind].length

        for i in range(1, len(dijkstras)):
            snake_distance = dijkstras[i].find_distance(p)

            if snake_distance > closest_snake_distance:
                continue

            snake_size = snakes[i].length

            if snake_distance == closest_snake_distance:
                if closest_snake_size > snake_size:
                    continue

                if closest_snake_size == snake_size:
                    closest_snake_ind = -1
                    continue

            closest_snake_ind = i
            closest_snake_distance = snake_distance
            closest_snake_size = snake_size

        if closest_snake_ind < 0:
            return None

        return snakes[closest_snake_ind]

    def get_snake_area(self, snake: Snake) -> Set[Point]:
        return self.snakes_areas.get(snake.id, set())
