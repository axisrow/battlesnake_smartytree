class DirectedEdge:
    def __init__(self, v: int, w: int, weight: float):
        self.v = v
        self.w = w
        self.weight = weight

    def get_weight(self) -> float:
        return self.weight

    def get_source(self) -> int:
        return self.v

    def get_destination(self) -> int:
        return self.w

    def __str__(self) -> str:
        return f"{self.get_source()} -> {self.get_destination()} {self.get_weight():.2f}"
