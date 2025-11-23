from snake.entities.game_state import GameState
from snake.entities.game import Ruleset
from snake.context.board_context import BoardContext, BorderedBoardContext, WrappedBoardContext


class BoardContextFactory:
    @staticmethod
    def create_board(game_state: GameState) -> BoardContext:
        board = game_state.board
        ruleset_name = game_state.game.ruleset.name

        if ruleset_name in (Ruleset.WRAPPED, Ruleset.WRAPPED_CONSTRICTOR):
            return WrappedBoardContext(board.height, board.width)
        else:
            return BorderedBoardContext(board.height, board.width)
