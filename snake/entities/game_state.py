from snake.entities.game import Game
from snake.entities.board import Board
from snake.entities.snake import Snake


class GameState:
    def __init__(self, game: Game, board: Board, turn: int, you: Snake):
        self.game = game
        self.board = board
        self.turn = turn
        self.you = you

    def __str__(self) -> str:
        return str(self.board)

    @classmethod
    def from_dict(cls, data: dict) -> 'GameState':
        return cls(
            game=Game.from_dict(data['game']),
            board=Board.from_dict(data['board']),
            turn=data['turn'],
            you=Snake.from_dict(data['you'])
        )

    def to_dict(self) -> dict:
        return {
            'game': self.game.to_dict(),
            'board': self.board.to_dict(),
            'turn': self.turn,
            'you': self.you.to_dict()
        }
