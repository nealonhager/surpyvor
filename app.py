from player import Player


if __name__ == "__main__":
    for _ in range(10):
        player = Player()
        print(player.get_full_name(), player.age, player.profession, sep=", ")
