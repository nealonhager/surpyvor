from player import Player
from random import randint


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
    print(num_tribes, "tribes:", tribe_colors)
    for i, player in enumerate(players):
        player.tribe = tribe_colors[i % num_tribes]

    # Show Players
    for player in players:
        print(
            player.get_full_name(),
            player.age,
            player.profession,
            f"{player.tribe} Tribe",
            sep=", ",
        )

    ...
