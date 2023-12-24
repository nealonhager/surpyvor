from challenges import IndividualChallenge
from players import Player
from tribal_council import TribalCouncil, FinalTribalCouncil


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
