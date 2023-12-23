from typing import Tuple, Optional, List
from tribe import Tribe
from random import randint
from players import Player


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
    def __init__(self, players: List[Player]):
        self.players = players

    def play(self, num_winners: int = 1) -> Tuple[List[Player], List[Player]]:
        """
        Determines the winning player(s), and also return the losers.
        """
        winners = []
        for _ in range(num_winners):
            winner = self.players.pop(randint(0, len(self.players) - 1))
            winners.append(winner)

        return winners, self.players
