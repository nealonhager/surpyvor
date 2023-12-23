from player import Player


def dialog(player: Player, text: str):
    """
    Prints a line of dialog to the console.
    """
    print(f"\n{player.get_full_name()}:\n\t{text}\n")
