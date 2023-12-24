from players import Player, host
from random import randint, shuffle
from tribe import Tribe, TribeFactory
from challenges import GroupChallenge, IndividualChallenge
from tribal_council import TribalCouncil, FinalTribalCouncil
from utils import dialog
from dataclasses import asdict
import json


if __name__ == "__main__":
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
    tribe_factory = TribeFactory()
    tribes = [tribe_factory.create_empty_tribe() for _ in range(num_tribes)]

    for i, player in enumerate(players):
        player.tribe = tribes[i % num_tribes]
        player.tribe.add_player(player)

    # Generate pictures of contenstants
    for player in players:
        try:
            player.create_profile_image(player.tribe.color)
        except:
            print(f"{player.get_full_name()}'s image could not be created.")

    dialog(
        host,
        "Welcome to Surpyvor, 18 Americans from different walks of life will be competing to be the sole Surpyvor, and a million dollars.",
    )

    for tribe in tribes:
        x = f"On the {tribe.color} tribe, we have "
        for player in tribe.players:
            x += f"{player.get_full_name()}, a {player.age} year old {player.profession}. "
        dialog(host, x)

    # First Tribal Council
    dialog(host, "Let's get right into the first challenge.")
    winning_tribe, losing_tribe = GroupChallenge(tribes).play()
    tribes = [winning_tribe, losing_tribe, *tribes]
    dialog(host, f"{winning_tribe.color} tribe wins it, and is safe from elimination!")
    dialog(
        host,
        f"{losing_tribe.color} tribe, got nothing for you, see you tonight at tribal council.",
    )
    losing_tribe.players, _ = TribalCouncil(losing_tribe.players).simulate()

    # Run challenges + tribal council until merge or tribe swap
    merge = False
    while True:
        dialog(host, "Come on in guys!")
        winning_tribe, losing_tribe = GroupChallenge(tribes).play()
        tribes = [winning_tribe, losing_tribe, *tribes]
        dialog(
            host, f"{winning_tribe.color} tribe wins it, and is safe from elimination!"
        )
        dialog(
            host,
            f"{losing_tribe.color} tribe, got nothing for you, see you tonight at tribal council.",
        )
        losing_tribe.players, _ = TribalCouncil(losing_tribe.players).simulate()

        number_of_players_remaining = sum([len(tribe.players) for tribe in tribes])

        if number_of_players_remaining <= 10:
            merge = True
            break
        if len(losing_tribe.players) < 3:
            break

    # Determine if there is going to be a merge or a tribe swap
    if merge:
        dialog(host, "Drop your buffs, because we're merging.")
    else:
        dialog(host, "Drop your buffs, because we're swapping tribes.")
        players = []

        for tribe in tribes:
            players.extend(tribe.players)

        for player in players:
            player.tribe = None

        num_tribes = 2
        tribes = [TribeFactory().create_empty_tribe() for _ in range(num_tribes)]
        shuffle(players)
        for i, player in enumerate(players):
            player.tribe = tribes[i % num_tribes]
            player.tribe.add_player(player)

        while True:
            dialog(host, "Come on in guys!")
            winning_tribe, losing_tribe = GroupChallenge(tribes).play()
            tribes = [winning_tribe, losing_tribe, *tribes]
            dialog(
                host,
                f"{winning_tribe.color} tribe wins it, and is safe from elimination!",
            )
            dialog(
                host,
                f"{losing_tribe.color} tribe, got nothing for you, see you tonight at tribal council.",
            )
            losing_tribe.players, _ = TribalCouncil(losing_tribe.players).simulate()

            number_of_players_remaining = sum([len(tribe.players) for tribe in tribes])

            if number_of_players_remaining <= 10:
                merge = True
                break
            if len(losing_tribe.players) < 3:
                break
        dialog(host, "Drop your buffs, because we're merging.")

    # Loop
    players = []
    jury = []
    for tribe in tribes:
        players.extend(tribe.players)
    while True:
        winners, losers = IndividualChallenge(players).play(num_winners=1)
        players, new_jury_member = TribalCouncil(losers).simulate()
        players.extend(winners)
        jury.append(new_jury_member)
        if len(players) <= 3:
            break

    # jury votes on who wins
    final_3 = [player.get_full_name() for player in players]
    dialog(host, f"Here is your final 3: {final_3}")
    winner = FinalTribalCouncil(jury, players).simulate()

    ...
