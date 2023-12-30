import logging


class ScriptWriter:
    @staticmethod
    def write_to_file(text: str):
        """
        Writes to the script files.
        """
        with open("script.txt", "a") as file:
            file.write(f"{text}\n\n")

        logging.info(f"{text}")

    @staticmethod
    def clear_file():
        """
        Clears the existing script file.
        """
        with open("script.txt", "w") as file:
            file.write("")

    @classmethod
    def add_dialog(cls, name: str, dialog: str):
        """
        Writes dialog to the script file.
        """
        cls.write_to_file(f"{name.upper()}: {dialog}")

    @classmethod
    def add_action(cls, action: str):
        """
        Writes an action to the script file.
        """
        cls.write_to_file(action.upper())
