from players import Player, host
from random import randint, shuffle
from tribe import TribeFactory
from challenges import GroupChallenge, IndividualChallenge
from tribal_council import TribalCouncil, FinalTribalCouncil
from script_write import ScriptWriter as sw
from dataclasses import asdict
import json
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    sw.clear_file()
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
            player.create_profile_image_prompt(player.tribe.color)
        except _:
            print(f"{player.get_full_name()}'s image could not be created.")

    sw.add_dialog(
        host.get_full_name(),
        "Welcome to Surpyvor, 18 Americans from different walks of life will be competing to be the sole Surpyvor, and a million dollars.",
    )

    for tribe in tribes:
        x = f"On the {tribe.color} tribe, we have "
        for player in tribe.players:
            x += f"{player.get_full_name()}, a {player.age} year old {player.profession} from {player.home_state}. "
        sw.add_dialog(host.get_full_name(), x)

    # First Tribal Council
    sw.add_dialog(host.get_full_name(), "Let's get right into the first challenge.")
    winning_tribe, losing_tribe = GroupChallenge(tribes).play()
    tribes = [winning_tribe, losing_tribe, *tribes]
    sw.add_dialog(
        host.get_full_name(),
        f"{winning_tribe.color} tribe wins it, and is safe from elimination!",
    )
    sw.add_dialog(
        host.get_full_name(),
        f"{losing_tribe.color} tribe, got nothing for you, see you tonight at tribal council.",
    )
    losing_tribe.players, _ = TribalCouncil(losing_tribe.players).simulate()

    sw.add_action("Players walk back to their camps.")

    # Run challenges + tribal council until merge or tribe swap
    merge = False
    while True:
        sw.add_dialog(host.get_full_name(), "Come on in guys!")
        winning_tribe, losing_tribe = GroupChallenge(tribes).play()
        tribes = [winning_tribe, losing_tribe, *tribes]
        sw.add_dialog(
            host.get_full_name(),
            f"{winning_tribe.color} tribe wins it, and is safe from elimination!",
        )
        sw.add_dialog(
            host.get_full_name(),
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
        sw.add_dialog(host.get_full_name(), "Drop your buffs, because we're merging.")
    else:
        sw.add_dialog(
            host.get_full_name(), "Drop your buffs, because we're swapping tribes."
        )
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
            sw.add_dialog(host.get_full_name(), "Come on in guys!")
            winning_tribe, losing_tribe = GroupChallenge(tribes).play()
            tribes = [winning_tribe, losing_tribe, *tribes]
            sw.add_dialog(
                host.get_full_name(),
                f"{winning_tribe.color} tribe wins it, and is safe from elimination!",
            )
            sw.add_dialog(
                host.get_full_name(),
                f"{losing_tribe.color} tribe, got nothing for you, see you tonight at tribal council.",
            )
            losing_tribe.players, _ = TribalCouncil(losing_tribe.players).simulate()

            number_of_players_remaining = sum([len(tribe.players) for tribe in tribes])

            if number_of_players_remaining <= 10:
                merge = True
                break
            if len(losing_tribe.players) < 3:
                break
        sw.add_dialog(host.get_full_name(), "Drop your buffs, because we're merging.")

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
    sw.add_dialog(host.get_full_name(), f"Here is your final 3: {final_3}")
    winner = FinalTribalCouncil(jury, players).simulate()

    ...
