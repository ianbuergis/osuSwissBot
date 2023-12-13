from .entity import Entity


class Player(Entity):
    id: int

    userId: int

    username: str

    rank: int

    def __init__(self, values: list):
        self.id = values[0]
        self.userId = values[1]
        self.username = values[2]
        self.rank = values[3]

    def toList(self):
        return [
            self.id,
            self.userId,
            self.username,
            self.rank
        ]
