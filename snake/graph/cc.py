from typing import List
from snake.point import Point
from snake.graph.graph import Graph


class CC:
    """Connected Components algorithm"""

    def __init__(self, graph: Graph, max_hazard: int):
        self.G = graph
        self.max_hazard = max(max_hazard, Graph.MOVE_WEIGHT * 2)

        self.marked: List[bool] = [False] * self.G.V()
        self.id: List[int] = [0] * self.G.V()
        self.count = 0

        for s in range(self.G.V()):
            if not self.marked[s]:
                self._dfs(self.G, s)
                self.count += 1

        self.components_size: List[int] = [0] * self.count
        for v in self.id:
            self.components_size[v] += 1

    def _dfs(self, G: Graph, v: int):
        self.marked[v] = True
        self.id[v] = self.count

        for edge in G.adj(v, 0):
            destination = edge.get_destination()
            if (not self.marked[destination] and
                    not G.is_obstacle(v) and
                    edge.get_weight() < self.max_hazard):
                self._dfs(G, destination)

    def connected(self, v: int, w: int) -> bool:
        return self.id[v] == self.id[w]

    def get_id(self, v: int) -> int:
        return self.id[v]

    def component_size(self, v: int) -> int:
        return self.components_size[self.id[v]]

    def __str__(self) -> str:
        sb = []
        for y in range(self.G.board.height()):
            for x in range(self.G.board.width()):
                component_id = self.get_id(self.G.board.value_of_point(Point(x, y)))
                sb.append(f"{component_id:3d} ")
            sb.append("\n")
        return "".join(sb)
