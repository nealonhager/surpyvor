from typing import Tuple, Optional, List
from tribe import Tribe
from random import randint


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
