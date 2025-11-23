from snake.direction import Direction
from snake.strategy.strategy import Strategy
from snake.strategy.utils import Utils
from snake.graph.lsp import LSP


class Fill(Strategy):
    def find_move(self, ctx) -> Direction:
        me = ctx.state().me

        if me.length == 0:
            return Direction.DOWN

        possible_moves = Utils.init_possible_directions(ctx, me)

        path = LSP(ctx.board_graph(), ctx.state().me.head()).find_longest_path()
        if path:
            return Utils.move_thru_path(ctx, possible_moves, path)

        return Utils.move_forward(ctx, possible_moves)
