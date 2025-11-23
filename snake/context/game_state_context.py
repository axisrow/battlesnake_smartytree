from typing import List
from snake.point import Point
from snake.entities.snake import Snake
from snake.entities.game_state import GameState


class GameStateContext:
    def __init__(self, me: Snake, snakes: List[Snake], food: List[Point],
                 hazards: List[Point], hazard_damage: int):
        self.me = me
        self.snakes = snakes
        self.food = food
        self.hazards = hazards
        self.hazard_damage = hazard_damage

    @classmethod
    def from_game_state(cls, game_state: GameState) -> 'GameStateContext':
        return cls(
            me=game_state.you,
            snakes=game_state.board.snakes,
            food=game_state.board.food,
            hazards=game_state.board.hazards,
            hazard_damage=game_state.game.ruleset.settings.hazard_damage_per_turn
        )
