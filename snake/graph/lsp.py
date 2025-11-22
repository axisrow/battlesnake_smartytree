from typing import List
from snake.point import Point
from snake.graph.graph import Graph
from snake.graph.directed_edge import DirectedEdge


class LSP:
    """Longest Simple Path algorithm"""

    def __init__(self, graph: Graph, start_point: Point):
        self.iterations = 15000
        self.longest_path: List[DirectedEdge] = []

        marked = [False] * graph.V()
        v = graph.board.value_of_point(start_point)
        path: List[DirectedEdge] = []

        self._dfs(graph, v, marked, path)

    def _dfs(self, graph: Graph, v: int, marked: List[bool], path: List[DirectedEdge]):
        if self.iterations <= 0:
            return

        self.iterations -= 1
        marked[v] = True

        for edge in graph.adj(v, 0):
            if not marked[edge.get_destination()]:
                path.append(edge)
                self._dfs(graph, edge.get_destination(), marked, path)
                path.pop()

        if len(path) > len(self.longest_path):
            self.longest_path = path.copy()

        marked[v] = False

    def find_longest_path(self) -> List[DirectedEdge]:
        return self.longest_path
