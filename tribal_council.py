from typing import List, Tuple
from players import Player, host
import random
from script_write import ScriptWriter as sw
from collections import Counter


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

        votes = []

        # Each player votes
        for player in self.players:
            voted_player = player.vote(self.players)
            votes.append(voted_player.get_full_name())

        sw.add_dialog(host.get_full_name(), "I'll go tally the votes.")

        tally = []

        def get_dialog_from_tally(player_name: str) -> str:
            tally.append(player_name)
            tally_grouped = dict(Counter(tally))

            _dialog = f"{player_name}. "

            if len(tally) > 1:
                for k, v in tally_grouped.items():
                    _dialog += f"{v} vote{'s' if v > 1 else ''} {k}. "
                votes_remaining = len(votes) - len(tally)
                if votes_remaining in range(1, 3):
                    _dialog += f"{len(votes) - len(tally)} vote{'s' if len(votes) - len(tally) > 1 else ''} left. "

            return _dialog

        voted_out_player = None
        for vote in votes:
            dialog_from_tally = get_dialog_from_tally(vote)
            if max(list(dict(Counter(tally)).values())) > (len(votes) // 2):
                voted_out_player = vote
            sw.add_dialog(host.get_full_name(), dialog_from_tally)

        highest_vote_count = max(dict(Counter(tally)).values())
        number_of_players_with_highest_votes = 0
        for k, v in dict(Counter(tally)).items():
            if v == highest_vote_count:
                number_of_players_with_highest_votes += 1
        if not voted_out_player:
            if number_of_players_with_highest_votes > 1:
                sw.add_dialog(
                    host.get_full_name(),
                    "Looks like we have a tie, here's what's going to happen.",
                )
                # TODO
                voted_out_player = random.choice(votes)
            else:
                for k, v in dict(Counter(tally)).items():
                    if v == highest_vote_count:
                        voted_out_player = k

        for player in self.players:
            if player.get_full_name() == voted_out_player:
                voted_out_player = player
                break

        new_players = []
        for player in self.players:
            if player != voted_out_player:
                new_players.append(player)

        sw.add_dialog(
            host.get_full_name(),
            f"n-th person voted out of surpyvor: {voted_out_player.get_full_name()}",
        )
        sw.add_action(
            f"{voted_out_player.get_full_name()} get's their torch snuffed out."
        )
        sw.add_dialog(
            host.get_full_name(),
            f"{voted_out_player.get_full_name()} your tribe has spoken.",
        )
        sw.add_action("Players walk back to their camps.")

        return new_players, voted_out_player


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
