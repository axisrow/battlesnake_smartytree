import logging
import yaml
from flask import Flask, request, jsonify

from snake.entities.game_state import GameState
from snake.entities.responses import DetailsResponse, MoveResponse
from snake.context.context import Context
from snake.strategy.strategy_factory import StrategyFactory
from snake.strategy.constrictor import Constrictor
from snake.strategy.fill import Fill
from snake.entities.game import Ruleset

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

app = Flask(__name__)

# Build default strategy
strategy_name = config['app']['snake'].get('strategy', 'FindFood')
logger.info(f"Building strategy {strategy_name}")
default_strategy = StrategyFactory.build(strategy_name)


@app.route('/', methods=['GET'])
def information():
    snake_config = config['app']['snake']
    details = DetailsResponse(
        name=snake_config.get('name', DetailsResponse.DEFAULT_NAME),
        color=snake_config.get('color', DetailsResponse.DEFAULT_COLOR),
        head=snake_config.get('head', DetailsResponse.DEFAULT_SKIN),
        tail=snake_config.get('tail', DetailsResponse.DEFAULT_SKIN)
    )
    return jsonify(details.to_dict())


@app.route('/start', methods=['POST'])
def start():
    return '', 204


@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    game_state = GameState.from_dict(data)
    return perform_turn(game_state)


@app.route('/end', methods=['POST'])
def end():
    return '', 204


def perform_turn(game_state: GameState):
    strategy = create_strategy(game_state)

    logger.info(f"Game {game_state.game.id}, Turn {game_state.turn}")
    logger.debug(f"Strategy {strategy.__class__.__name__}")

    context = Context.from_game_state(game_state)
    move_direction = context.find_move(strategy)

    response = MoveResponse(move_direction)
    return jsonify(response.to_dict())


def create_strategy(state: GameState):
    ruleset_name = state.game.ruleset.name
    if ruleset_name in (Ruleset.CONSTRICTOR, Ruleset.WRAPPED_CONSTRICTOR):
        return Constrictor()
    elif ruleset_name == Ruleset.SOLO:
        return Fill()
    else:
        return default_strategy


if __name__ == '__main__':
    port = config['server'].get('port', 8080)
    host = config['server'].get('host', '0.0.0.0')

    logger.info(f"SNAKE is up! http://{host}:{port}/")

    app.run(host=host, port=port, debug=False)
