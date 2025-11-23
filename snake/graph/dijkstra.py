import heapq
from typing import List, Optional
from snake.point import Point
from snake.graph.graph import Graph
from snake.graph.directed_edge import DirectedEdge


class Dijkstra:
    def __init__(self, graph: Graph, source: Point | int):
        self.G = graph
        if isinstance(source, Point):
            self.source = graph.board.value_of_point(source)
        else:
            self.source = source

        self.edge_to: List[Optional[DirectedEdge]] = [None] * self.G.V()
        self.dist_to: List[float] = [float('inf')] * self.G.V()

        # Priority queue: (distance, vertex)
        pq = []

        self.dist_to[self.source] = 0.0
        heapq.heappush(pq, (0.0, self.source))

        while pq:
            dist, v = heapq.heappop(pq)

            # Skip if we've found a better path already
            if dist > self.dist_to[v]:
                continue

            for e in self.G.adj(v, 0):
                self._relax(e, pq)

    def _relax(self, e: DirectedEdge, pq: list):
        v = e.get_source()
        w = e.get_destination()
        new_distance = self.dist_to[v] + e.get_weight()

        if self.dist_to[w] > new_distance:
            self.dist_to[w] = new_distance
            self.edge_to[w] = e
            heapq.heappush(pq, (new_distance, w))

    def find_path(self, d: Point | int) -> Optional[List[DirectedEdge]]:
        if isinstance(d, Point):
            d = self.G.board.value_of_point(d)

        if self.edge_to[d] is None:
            return None

        path = []
        current = d

        while current != self.source:
            edge = self.edge_to[current]
            if edge is None:
                return None
            path.insert(0, edge)
            current = edge.get_source()

        return path

    def find_distance(self, d: Point | int) -> float:
        if isinstance(d, Point):
            d = self.G.board.value_of_point(d)
        return self.dist_to[d]

    def __str__(self) -> str:
        sb = []
        for y in range(self.G.board.height() - 1, -1, -1):
            for x in range(self.G.board.width()):
                distance = self.dist_to[self.G.board.value_of_point(Point(x, y))]
                if distance != float('inf'):
                    sb.append(f"{distance:4.1f}")
                else:
                    sb.append(" ---")

                if x != self.G.board.width() - 1:
                    sb.append(" ")
            sb.append("\n")
        return "".join(sb)
