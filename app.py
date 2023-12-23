from player import Player
from random import randint
from tribe import Tribe


def dialog(player: Player, text: str):
    print(f"{player.get_full_name()}\n\t{text}")


if __name__ == "__main__":
    host = Player(tribe="None", first_name="Jeff", last_name="Probst", age=50)
    players = []

    # Generate Players
    for _ in range(18):
        players.append(Player())

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

    dialog(
        host,
        "Welcome to Surpyvor, 18 Americans from different walks of life will be competing to be the sole Surpyvor, and a million dollars.",
    )

    for tribe in tribes:
        x = f"On the {tribe.color} tribe, we have "
        for player in tribe.players:
            x += f"{player.get_full_name()}, a {player.age} year old {player.profession}. "
        dialog(host, x)

    ...
