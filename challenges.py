from typing import Tuple, Optional, List
from tribe import Tribe
from random import randint
from players import Player
import math


class GroupChallenge:
    def __init__(self, groups: List[Tribe]):
        self.groups = groups

    def play(self) -> Tuple[Tribe, Optional[Tribe]]:
        """
        Determines a winning group, and optionally a losing group.
        """
        winner = self.groups.pop(randint(0, len(self.groups) - 1))
        loser = self.groups.pop(randint(0, len(self.groups) - 1))

        return winner, loser


class IndividualChallenge:
    def __init__(self, players: List[Player], attributes_to_use: List[str]):
        self.players = players
        self.attributes_to_use = attributes_to_use
        self.attribute_products = []

    def play(self, num_winners: int = 1) -> Tuple[List[Player], List[Player]]:
        """
        Determines the winning player(s), and also return the losers.
        """
        winners = []

        for player in self.players:
            players_attributes = [
                getattr(player, attribute) for attribute in self.attributes_to_use
            ]
            self.attribute_products.append(math.prod(players_attributes))

        for _ in range(num_winners):
            best_player_idx = max(
                enumerate(self.attribute_products), key=lambda x: x[1]
            )[0]
            winner = self.players.pop(best_player_idx)
            winners.append(winner)

        return winners, self.players
