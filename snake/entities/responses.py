from snake.direction import Direction


class DetailsResponse:
    API_VERSION = "1"
    AUTHOR = "Serhii Zasenko"
    VERSION = "1.0.0"
    DEFAULT_SKIN = "default"
    DEFAULT_NAME = "Unnamed"
    DEFAULT_COLOR = "#0F0"

    def __init__(self, apiversion: str = API_VERSION, name: str = DEFAULT_NAME,
                 author: str = AUTHOR, color: str = DEFAULT_COLOR,
                 head: str = DEFAULT_SKIN, tail: str = DEFAULT_SKIN,
                 version: str = VERSION):
        self.apiversion = apiversion
        self.name = name
        self.author = author
        self.color = color
        self.head = head
        self.tail = tail
        self.version = version

    def to_dict(self) -> dict:
        return {
            'apiversion': self.apiversion,
            'author': self.author,
            'color': self.color,
            'head': self.head,
            'tail': self.tail,
            'version': self.version
        }


class MoveResponse:
    def __init__(self, move: Direction, shout: str = None):
        self.move = move
        self.shout = shout

    def to_dict(self) -> dict:
        result = {'move': str(self.move)}
        if self.shout:
            result['shout'] = self.shout
        return result
