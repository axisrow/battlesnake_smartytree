from snake.strategy.strategy import Strategy
from snake.strategy.find_food import FindFood
from snake.strategy.find_tail import FindTail
from snake.strategy.cycle import Cycle
from snake.strategy.constrictor import Constrictor
from snake.strategy.fill import Fill


class StrategyFactory:
    STRATEGY_FIND_FOOD = "FindFood"
    STRATEGY_FIND_TAIL = "FindTail"
    STRATEGY_CYCLE = "Cycle"
    STRATEGY_CONSTRICTOR = "Constrictor"
    STRATEGY_FILL = "Fill"

    @staticmethod
    def build(strategy: str) -> Strategy:
        strategies = {
            StrategyFactory.STRATEGY_FIND_FOOD: FindFood,
            StrategyFactory.STRATEGY_FIND_TAIL: FindTail,
            StrategyFactory.STRATEGY_CYCLE: Cycle,
            StrategyFactory.STRATEGY_CONSTRICTOR: Constrictor,
            StrategyFactory.STRATEGY_FILL: Fill
        }

        strategy_class = strategies.get(strategy)
        if not strategy_class:
            raise RuntimeError(f"Unknown strategy {strategy}")

        return strategy_class()
