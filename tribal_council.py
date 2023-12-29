from typing import List, Tuple
from players import Player, host
import random
from script_write import ScriptWriter as sw


class TribalCouncil:
    def __init__(self, players: List[Player]):
        self.players = players

    def simulate(self) -> Tuple[List[Player], Player]:
        """
        Simulates a tribal council, and return the remaining players, and the person that got voted on.
        """
        sw.add_action("players walk to tribal council.")
        sw.add_dialog(
            host.get_full_name(),
            f"It is, time to vote. {self.players[0].get_full_name()}, start us off.",
        )

        votes = {}
        for player in self.players:
            vote = player.vote(self.players)
            if vote.get_full_name() not in votes:
                votes[vote.get_full_name()] = 1
            else:
                votes[vote.get_full_name()] += 1

        sw.add_dialog(host.get_full_name(), "I'll go tally the votes.")

        max_votes = max(votes.values())
        players_with_max_votes = [
            player for player, vote_count in votes.items() if vote_count == max_votes
        ]
        random_player = random.choice(players_with_max_votes)
        for player in self.players:
            if player.get_full_name() == random_player:
                random_player = player
        if not isinstance(random_player, Player):
            raise ValueError('The player that got voted out was not of type "Person".')

        sw.add_dialog(
            host.get_full_name(),
            f"{random_player.get_full_name()}, your tribe has spoken.",
        )

        new_players = []
        for player in self.players:
            if player != random_player:
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

        sw.add_dialog(
            host.get_full_name(), f"{random_player}, you are the sole survivor."
        )

        return random_player
