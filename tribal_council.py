from typing import List, Tuple
from players import Player, host
import random
from utils import dialog


class TribalCouncil:
    def __init__(self, players: List[Player]):
        self.players = players

    def simulate(self) -> Tuple[List[Player], Player]:
        """
        Simulates a tribal council, and return the remaining players, and the person that got voted on.
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

        dialog(host, f"{random_player}, your tribe has spoken.")

        new_players = []
        for player in self.players:
            if player.get_full_name() != random_player:
                new_players.append(player)

        return new_players, random_player


class FinalTribalCouncil:
    def __init__(self, jury: List[Player], players: List[Player]):
        self.jury = jury
        self.players = players

    def simulate(self) -> str:
        """
        Simulates final tribal council, returns the name of the winner.
        """
        votes = {}
        for player in self.jury:
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

        dialog(host, f"{random_player}, you are the sole survivor.")

        return random_player
