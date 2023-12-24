from players import Player


def test_vote():
    players = [Player() for _ in range(10)]
    voted_player = players[0].vote(players)
    assert len(players) == 10
    voted_player = players[0].vote(players[1:])
    assert len(players) == 10


def test_descriptor():
    player = Player()
    desc = player.generate_descriptors()
    new_desc = player.generate_descriptors()

    print(desc)
    assert desc != ""
    assert desc == new_desc
