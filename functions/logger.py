import sys


class Logger():
    def __init__(self) -> None:
        self.is_enabled: bool = False

        for command in sys.argv:
            if command.strip().lower() == "--verbose":
                self.is_enabled = True

    def debug(self, message: str) -> None:
        if self.is_enabled:
            print(message)

    def only_production(self, message: str) -> None:
        if not self.is_enabled:
            print(message)
