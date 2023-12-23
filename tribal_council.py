from typing import List
from player import Player
import random


class TribalCouncil:
    def __init__(self, players: List[Player]):
        self.players = players

    def simulate(self) -> List[Player]:
        """
        Simulates a tribal council, and return the remaining players.
        """
        votes = {}
        for player in self.players:
            vote = player.vote(self.players)
            if vote.get_full_name() not in votes:
                votes[vote.get_full_name()] = 1
            else:
                votes[vote.get_full_name()] += 1

        max_votes = max(votes.values())
        players_with_max_votes = [
            player for player, vote_count in votes.items() if vote_count == max_votes
        ]
        random_player = random.choice(players_with_max_votes)

        print(f"{random_player}, your tribe has spoken.")

        new_players = []
        for player in self.players:
            if player.get_full_name() != random_player:
                new_players.append(player)

        return new_players
