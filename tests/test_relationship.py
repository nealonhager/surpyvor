from players import Player
from relationship import Relationship


def test_create_relationship():
    player1 = Player()
    player2 = Player()
    player1.create_bond(player2)

    assert len(player1.relationships) == 1
    assert isinstance(player1.relationships[0], Relationship)
    assert player1.relationships[0].player == player2

    assert len(player2.relationships) == 1
    assert isinstance(player2.relationships[0], Relationship)
    assert player2.relationships[0].player == player1
