from typing import List
from snake.direction import Direction
from snake.point import Point
from snake.strategy.filter.strategy_filter import StrategyFilter


class AvoidObstacles(StrategyFilter):
    def filter_moves(self, ctx, possible_moves: List[Direction]) -> None:
        state = ctx.state()
        board = ctx.board()
        me = state.me
        body = me.body
        avoider = Avoider(ctx, possible_moves)

        possible_obstacles = []
        obstacles = body[2:-1].copy()

        if me.health == 100:
            obstacles.append(body[-1])

        for snake in state.snakes:
            if snake == me:
                continue

            if snake.length >= me.length:
                enemy_head = snake.body[0]
                obstacles.append(enemy_head)

                directions = snake.body[1].direction_to(enemy_head)
                enemy_forward_direction = Direction.UP if not directions else directions[0]

                for direction in [
                    enemy_forward_direction,
                    enemy_forward_direction.rotate_clockwise(),
                    enemy_forward_direction.rotate_counterclockwise()
                ]:
                    possible_position = board.move_point_direction(enemy_head, direction)
                    if possible_position:
                        possible_obstacles.append(possible_position)

            obstacles.extend(snake.body[1:-1])

        if state.hazard_damage >= me.health:
            obstacles.extend(state.hazards)

        for point in obstacles:
            avoider.avoid_obstacle(point)

        for possible_obstacle in possible_obstacles:
            if len(possible_moves) <= 1:
                break
            avoider.avoid_obstacle(possible_obstacle)


class Avoider:
    def __init__(self, ctx, possible_moves: List[Direction]):
        self.head = ctx.state().me.head()
        self.possible_moves = possible_moves

    def avoid_obstacle(self, obstacle: Point):
        if self.head.manhattan_to(obstacle) == 1:
            directions = self.head.direction_to(obstacle)
            if directions and directions[0] in self.possible_moves:
                self.possible_moves.remove(directions[0])
