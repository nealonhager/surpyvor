from challenges import IndividualChallenge
from players import Player


def test_individual_challenge():
    players = [Player() for _ in range(10)]
    winners, losers = IndividualChallenge(players).play(num_winners=1)

    assert len(winners) == 1
    assert len(losers) == 9
