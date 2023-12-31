from typing import List, Tuple, Union
from players import Player, host
import random
from script_write import ScriptWriter as sw
from collections import Counter
import utils


class TribalCouncil:
    def __init__(self, players: List[Player]):
        self.players = players

    def simulate(
        self, jury: Union[List[Player], None] = None
    ) -> Tuple[List[Player], Player]:
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
                    "Looks like we have a tie. We will have a revote.",
                )
                # Tiebreaker: Revote among tied players
                tied_players = [
                    k
                    for k, v in dict(Counter(tally)).items()
                    if v == highest_vote_count
                ]
                tied_players = [
                    player
                    for player in self.players
                    if player.get_full_name() in tied_players
                ]
                revote_tally = []
                for player in self.players:
                    if player not in tied_players:
                        revoted_player = player.vote(tied_players)
                        revote_tally.append(revoted_player)

                # Check if the revote breaks the tie
                revote_counts = dict(Counter([p.get_full_name() for p in revote_tally]))

                number_of_players_with_highest_votes = 0
                for k, v in revote_counts.items():
                    if v == highest_vote_count:
                        number_of_players_with_highest_votes += 1
                if number_of_players_with_highest_votes == 1:
                    voted_out_player = max(revote_counts, key=revote_counts.get)
                else:
                    # Go to rocks
                    sw.add_dialog(
                        host.get_full_name(),
                        "Since we still have a tie, we will have to go to rocks.",
                    )
                    voted_out_player = random.choice(tied_players)

        for player in self.players:
            if player.get_full_name() == voted_out_player:
                voted_out_player = player
                break

        new_players = []
        for player in self.players:
            if player != voted_out_player:
                new_players.append(player)

        jury_mod = (
            ""
            if jury is None
            else f", and the {utils.ordinal(len(jury)+1)} member of our jury"
        )
        sw.add_dialog(
            host.get_full_name(),
            f"n-th person voted out of surpyvor{jury_mod}: {voted_out_player.get_full_name()}",
        )
        sw.add_action(
            f"{voted_out_player.get_full_name()} get's their torch snuffed out."
        )
        sw.add_dialog(
            host.get_full_name(),
            f"{voted_out_player.get_full_name()} your tribe has spoken.",
        )
        sw.add_action("Players walk back to their camps.")
        sw.add_action("Day ends.\n\n")

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
