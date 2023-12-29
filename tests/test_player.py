import os
from players import Player
from tribe import Tribe
from dotenv import load_dotenv

load_dotenv()


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

    assert desc != ""
    assert desc == new_desc


def test_chacter_image_creation():
    if int(os.environ.get("TEST_WITH_API_KEY")) == 1:
        player = Player()
        print(player.descriptor)
        player.create_profile_image_prompt_prompt("red")
