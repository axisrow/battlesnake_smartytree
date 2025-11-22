from typing import Set
from snake.graph.cc import CC
from snake.strategy.filter.avoid_closed_spaces import AvoidClosedSpaces


class AvoidClosedSpacesWithoutExpansion(AvoidClosedSpaces):
    def get_expanding_clusters(self, ctx, cc: CC) -> Set[int]:
        return set()
