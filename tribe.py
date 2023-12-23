from dataclasses import dataclass, field
from players import Player


@dataclass
class Tribe:
    color: str
    players: list = field(default_factory=list)

    def add_player(self, player: Player):
        self.players.append(player)

    def remove_player(self, player: Player):
        self.players.remove(player)
