from dataclasses import dataclass, field
from players import Player
from random import randint


@dataclass
class Tribe:
    color: str
    players: list = field(default_factory=list)

    def add_player(self, player: Player):
        self.players.append(player)

    def remove_player(self, player: Player):
        self.players.remove(player)


class TribeFactory:
    def __init__(self):
        self.colors = [
            "Red",
            "Blue",
            "Yellow",
            "Green",
            "Purple",
            "Orange",
            "Black",
            "White",
            "Pink",
            "Brown",
            "Gray",
            "Tan",
            "Lime",
            "Maroon",
            "Teal",
        ]

    def create_empty_tribe(self) -> Tribe:
        """
        Creates a tribe, and picks a color.

        Removes the selected color from the pool of available colors.
        """
        tribe_color = self.colors.pop(randint(0, len(self.colors) - 1))
        return Tribe(tribe_color)
