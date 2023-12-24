from challenges import IndividualChallenge, GroupChallenge
from players import Player
import json
from random import randint
from dataclasses import asdict
from tribe import Tribe
from tribal_council import TribalCouncil


def test_individual_challenge():
    players = [Player() for _ in range(10)]
    winners, losers = IndividualChallenge(players).play(num_winners=1)

    assert len(winners) == 1
    assert len(losers) == 9


def test_group_challenge():
    players = []

    # Generate Players
    for _ in range(18):
        players.append(Player())

    # Write player info to a file
    with open("player_info.txt", "w") as file:
        for player in players:
            file.write(json.dumps(asdict(player)) + "\n")

    # Generate Tribes
    num_tribes = randint(2, 3)
    colors = [
        "Red",
        "Blue",
        "Yellow",
        "Green",
        "Purple",
        "Orange",
        "Black",
        "White",
        "Pink",
        "Brown",
        "Gray",
        "Tan",
        "Lime",
        "Maroon",
        "Teal",
    ]
    tribe_colors = [colors.pop(randint(0, len(colors) - 1)) for _ in range(num_tribes)]
    tribes = [Tribe(tribe_colors[i], []) for i in range(num_tribes)]
    for i, player in enumerate(players):
        player.tribe = tribes[i % num_tribes]
        player.tribe.add_player(player)
        assert player.tribe is not None

    # First Tribal Council
    winning_tribe, losing_tribe = GroupChallenge(tribes).play()

    assert isinstance(winning_tribe, Tribe)
    assert isinstance(losing_tribe, Tribe)

    tribes = [winning_tribe, losing_tribe, *tribes]

    assert len(tribes) == num_tribes

    losing_tribe.players, player_voted_out = TribalCouncil(
        losing_tribe.players
    ).simulate()

    assert isinstance(player_voted_out, Player)


def test_looping_group_challenges():
    players = []

    # Generate Players
    for _ in range(18):
        players.append(Player())
    initial_player_count = 18

    # Write player info to a file
    with open("player_info.txt", "w") as file:
        for player in players:
            file.write(json.dumps(asdict(player)) + "\n")

    # Generate Tribes
    num_tribes = randint(2, 3)
    colors = [
        "Red",
        "Blue",
        "Yellow",
        "Green",
        "Purple",
        "Orange",
        "Black",
        "White",
        "Pink",
        "Brown",
        "Gray",
        "Tan",
        "Lime",
        "Maroon",
        "Teal",
    ]
    tribe_colors = [colors.pop(randint(0, len(colors) - 1)) for _ in range(num_tribes)]
    tribes = [Tribe(tribe_colors[i], []) for i in range(num_tribes)]
    for i, player in enumerate(players):
        player.tribe = tribes[i % num_tribes]
        player.tribe.add_player(player)
        assert player.tribe is not None

    # First Tribal Council
    winning_tribe, losing_tribe = GroupChallenge(tribes).play()
    initial_player_count -= 1

    assert isinstance(winning_tribe, Tribe)
    assert isinstance(losing_tribe, Tribe)

    tribes = [winning_tribe, losing_tribe, *tribes]

    assert len(tribes) == num_tribes

    losing_tribe.players, player_voted_out = TribalCouncil(
        losing_tribe.players
    ).simulate()

    assert isinstance(player_voted_out, Player)

    # Run challenges + tribal council until merge or tribe swap
    loop = 0
    while True:
        loop += 1
        winning_tribe, losing_tribe = GroupChallenge(tribes).play()

        assert isinstance(winning_tribe, Tribe)
        assert isinstance(losing_tribe, Tribe)

        tribes = [winning_tribe, losing_tribe, *tribes]

        assert len(tribes) == num_tribes

        losing_tribe.players, player_voted_out = TribalCouncil(
            losing_tribe.players
        ).simulate()

        assert isinstance(player_voted_out, Player)

        number_of_players_remaining = sum([len(tribe.players) for tribe in tribes])

        assert number_of_players_remaining == initial_player_count - loop

        if number_of_players_remaining <= 10:
            break
        if len(losing_tribe.players) < 3:
            break
