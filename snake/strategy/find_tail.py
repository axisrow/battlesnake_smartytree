from snake.direction import Direction
from snake.strategy.strategy import Strategy
from snake.strategy.utils import Utils
from snake.strategy.filter.avoid_borders import AvoidBorders
from snake.strategy.filter.avoid_obstacles import AvoidObstacles
from snake.strategy.filter.avoid_closed_spaces import AvoidClosedSpaces


class FindTail(Strategy):
    MIN_HEALTH = 10

    def find_move(self, ctx) -> Direction:
        towards_tail = self._move_to_tail(ctx)

        if ctx.state().me.health >= self.MIN_HEALTH:
            return towards_tail
        else:
            # Move towards food
            board = ctx.board()
            food = ctx.state().food
            head = ctx.state().me.head()

            for direction in [towards_tail,
                              towards_tail.rotate_clockwise(),
                              towards_tail.rotate_counterclockwise()]:
                move_point = board.move_point_direction(head, direction)
                if move_point in food:
                    return direction

            from snake.strategy.find_food import FindFood
            return FindFood().find_move(ctx)

    def _move_to_tail(self, ctx) -> Direction:
        head = ctx.state().me.head()
        possible_moves = Utils.init_directions(ctx, ctx.state().me)
        body = ctx.state().me.body
        tail = body[-1]

        AvoidBorders().filter_moves(ctx, possible_moves)
        AvoidObstacles().filter_moves(ctx, possible_moves)
        AvoidClosedSpaces().filter_moves(ctx, possible_moves)

        if head.manhattan_to(tail) > 1 or body[-2] != tail:
            print("Moving to tail")
            return Utils.move_towards(ctx, possible_moves, tail)

        print("Moving forward")
        return Utils.move_forward(ctx, possible_moves)
