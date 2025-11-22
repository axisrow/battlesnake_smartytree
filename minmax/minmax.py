from snake.direction import Direction
from snake.entities.snake import Snake
from snake.context.context import Context
from snake.context.game_state_context import GameStateContext
from snake.strategy.utils import Utils


class DirectionPriority:
    def __init__(self, direction: Direction, score: float):
        self.direction = direction
        self.score = score

    def __lt__(self, other):
        return self.score < other.score


class MinMax:
    LENGTH_MULTIPLIER = 10

    def invoke(self, context: Context):
        pass

    def _find_snake_move(self, ctx: Context, snake: Snake):
        game_state_context = GameStateContext(
            me=snake,
            snakes=ctx.state().snakes,
            food=ctx.state().food,
            hazards=ctx.state().hazards,
            hazard_damage=ctx.state().hazard_damage
        )
        local_context = Context(ctx.board(), game_state_context, ctx.turn())
        moves = Utils.init_possible_directions(local_context, snake)

    @staticmethod
    def calculate_score(context: Context, me: Snake, opponent: Snake) -> float:
        if len(Utils.init_possible_directions(context, me)) == 0:
            return float('-inf')

        if len(Utils.init_possible_directions(context, opponent)) == 0:
            return float('inf')

        return (me.length - opponent.length) * MinMax.LENGTH_MULTIPLIER
