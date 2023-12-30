from typing import Tuple, Optional, List
from tribe import Tribe
from random import randint
from players import Player
import math
from players import host
from script_write import ScriptWriter as sw
import logging


class Challenge:
    def __init__(self):
        self.attributes = Player.get_attribute_names()
        self.weights = [1.0 for _ in self.attributes]

    def increase_weight_for_attribute(
        self, attribute: str, weight_modifier: float = 2.0
    ):
        """
        Increases the importance of the attribute.
        """
        self.weights[self.attributes.index(attribute)] *= weight_modifier

    def increase_weight_for_attributes(
        self, attributes: List[str], weight_modifier: float = 2.0
    ):
        """
        Increases the importance of the attributes.
        """
        for attribute in attributes:
            self.increase_weight_for_attribute(attribute, weight_modifier)

    def add_puzzle(self, weight_modifier: float = 2.0):
        """
        Increases the importance of creativity, intelligence, and strategic_ability.
        """
        self.increase_weight_for_attributes(
            ["creativity", "intelligence", "strategic_ability"], weight_modifier
        )

    def add_balancing_section(self, weight_modifier: float = 2.0):
        """
        Increases the importance of balance.
        """
        self.increase_weight_for_attribute("balance", weight_modifier)


class GroupChallenge:
    def __init__(self, groups: List[Tribe]):
        self.groups = groups

    def play(self, announce: bool = True) -> Tuple[Tribe, Optional[Tribe]]:
        """
        Determines a winning group, and optionally a losing group.
        """
        if announce:
            sw.add_dialog(host.get_full_name(), "Come on in guys!")

        winner = self.groups.pop(randint(0, len(self.groups) - 1))
        loser = self.groups.pop(randint(0, len(self.groups) - 1))

        sw.add_dialog(
            host.get_full_name(),
            f"{winner.color} tribe wins it, and is safe from elimination!",
        )
        sw.add_dialog(
            host.get_full_name(),
            f"{loser.color} tribe, got nothing for you, see you tonight at tribal council.",
        )
        sw.add_action("Players walk back to their camps.")
        return winner, loser


class IndividualChallenge:
    def __init__(self, players: List[Player]):
        self.players = players
        self.attribute_products = []

    def play(self, num_winners: int = 1) -> Tuple[List[Player], List[Player]]:
        """
        Determines the winning player(s), and also return the losers.
        """
        sw.add_dialog(
            host.get_full_name(),
            "Come on in guys! Let's get right into this individual challenge.",
        )
        winners = []
        challenge = Challenge()
        challenge.add_puzzle()
        challenge.add_balancing_section()

        for player in self.players:
            players_attributes = [
                getattr(player, attribute) for attribute in Player.get_attribute_names()
            ]
            players_attributes = [
                players_attribute * challenge.weights[i]
                for i, players_attribute in enumerate(players_attributes)
            ]
            self.attribute_products.append(math.prod(players_attributes))

        for _ in range(num_winners):
            best_player_idx = max(
                enumerate(self.attribute_products), key=lambda x: x[1]
            )[0]
            winner = self.players.pop(best_player_idx)
            logging.info(
                f"{winner.get_full_name()} won the individual challenge.".upper()
            )
            sw.add_dialog(
                host.get_full_name(),
                f"Congrats, {winner.get_full_name()} you are safe in tonight's tribal council. How does it feel?",
            )
            sw.add_dialog(winner.get_full_name(), winner.get_challenge_win_speech())
            winners.append(winner)
            winner.immunity_challenges_won += 1

        sw.add_action("Players walk back to their camps.")
        return winners, self.players
