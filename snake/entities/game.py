class GameSettings:
    def __init__(self, food_spawn_chance: int = 0, hazard_damage_per_turn: int = 0):
        self.food_spawn_chance = food_spawn_chance
        self.hazard_damage_per_turn = hazard_damage_per_turn

    @classmethod
    def from_dict(cls, data: dict) -> 'GameSettings':
        return cls(
            food_spawn_chance=data.get('foodSpawnChance', 0),
            hazard_damage_per_turn=data.get('hazardDamagePerTurn', 0)
        )

    def to_dict(self) -> dict:
        return {
            'foodSpawnChance': self.food_spawn_chance,
            'hazardDamagePerTurn': self.hazard_damage_per_turn
        }


class Ruleset:
    STANDARD = "standard"
    ROYALE = "royale"
    SQUAD = "squad"
    CONSTRICTOR = "constrictor"
    WRAPPED_CONSTRICTOR = "wrapped-constrictor"
    WRAPPED = "wrapped"
    SOLO = "solo"

    def __init__(self, name: str, version: str, settings: GameSettings = None):
        self.name = name
        self.version = version
        self.settings = settings or GameSettings()

    @classmethod
    def from_dict(cls, data: dict) -> 'Ruleset':
        return cls(
            name=data['name'],
            version=data.get('version', ''),
            settings=GameSettings.from_dict(data.get('settings', {}))
        )

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'version': self.version,
            'settings': self.settings.to_dict()
        }


class Game:
    def __init__(self, id: str, ruleset: Ruleset, timeout: int = 500, source: str = ""):
        self.id = id
        self.source = source
        self.ruleset = ruleset
        self.timeout = timeout

    @classmethod
    def from_dict(cls, data: dict) -> 'Game':
        return cls(
            id=data['id'],
            ruleset=Ruleset.from_dict(data.get('ruleset', {})),
            timeout=data.get('timeout', 500),
            source=data.get('source', '')
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'source': self.source,
            'ruleset': self.ruleset.to_dict(),
            'timeout': self.timeout
        }
