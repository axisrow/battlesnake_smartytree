from snake.direction import Direction
from snake.entities.game_state import GameState
from snake.context.board_context import BoardContext
from snake.context.game_state_context import GameStateContext
from snake.context.board_context_factory import BoardContextFactory
from snake.graph.graph import Graph


class Context:
    def __init__(self, board_context: BoardContext, game_state_context: GameStateContext, turn: int):
        self.board_context = board_context
        self.game_state_context = game_state_context
        self.turn_number = turn
        self._board_graph = None

    @classmethod
    def from_game_state(cls, game_state: GameState) -> 'Context':
        return cls(
            BoardContextFactory.create_board(game_state),
            GameStateContext.from_game_state(game_state),
            game_state.turn
        )

    def find_move(self, strategy) -> Direction:
        from snake.strategy.strategy import Strategy
        return strategy.find_move(self)

    def state(self) -> GameStateContext:
        return self.game_state_context

    def board(self) -> BoardContext:
        return self.board_context

    def board_graph(self) -> Graph:
        if self._board_graph is None:
            self._board_graph = Graph.create_generic_game_graph(self)
        return self._board_graph

    def turn(self) -> int:
        return self.turn_number
