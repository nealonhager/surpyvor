from typing import List
from challenges import IndividualChallenge
from players import Player
from tribal_council import TribalCouncil, FinalTribalCouncil
from tribe import TribeFactory


def test_individual_challenge_and_tribal():
    players = [Player() for _ in range(10)]
    assert len(players) == 10
    jury = []
    winners, losers = IndividualChallenge(players).play(num_winners=1)

    assert len(winners) == 1
    assert len(losers) == 9

    players, new_jury_member = TribalCouncil(losers).simulate()

    assert len(players) == 8

    players.extend(winners)
    jury.append(new_jury_member)

    assert len(players) == 9
    assert len(jury) == 1


def test_looping_individual_challenge_and_tribal():
    players = [Player() for _ in range(10)]
    assert len(players) == 10
    jury = []

    initial_player_count = 10
    loop = 0
    while True:
        loop += 1
        winners, losers = IndividualChallenge(players).play(num_winners=1)
        players, new_jury_member = TribalCouncil(losers).simulate()
        players.extend(winners)

        assert type(new_jury_member) is Player
        assert len(players) == initial_player_count - loop
        for player in players:
            assert type(player) is Player

        jury.append(new_jury_member)
        if len(players) <= 3:
            break

    assert len(players) == 3


def test_final_tribal_council():
    players = [Player() for _ in range(3)]
    jury = [Player() for _ in range(7)]

    winner = FinalTribalCouncil(jury, players).simulate()
    assert winner in [player.get_full_name() for player in players]


def test_tie():
    all_players = [Player() for _ in range(10)]
    tribe = TribeFactory().create_empty_tribe()
    global flipper
    flipper = 1

    def force_vote(self, players: List["Player"]) -> "Player":
        global flipper
        flipper = 0 if flipper == 1 else 1
        vote = all_players[flipper]

        return vote

    Player.vote = force_vote

    for player in all_players:
        player.tribe = tribe
        player.charisma = 1
        player.pride = 1
        player.intelligence = 1
        player.emotional_intelligence = 1
        player.popularity = 1
        player.loyalty = 1
        player.endurance = 1
        player.intelligence = 1
        player.creativity = 1
        player.fortitude = 1
        player.hunger = 1
        player.speed = 1
        player.balance = 1
        player.strength = 1

    jury = []
    all_players, new_jury_member = TribalCouncil(all_players).simulate(jury=jury)

    with open("script.txt", "r") as f:
        lines = "\n".join(f.readlines())
        assert "Since we still have a tie, we will have to go to rocks" in lines
