

from src.controller.telegram import TelegramBot
from src.brain import Brain
from src.command import Command
from src.data_layer import DataLayer


class Application:
    def __init__(self):
        self.data_layer = DataLayer()
        self.brain = Brain(self.data_layer)
        self.commands = Command(self.data_layer, self.brain)
        self.bot = TelegramBot(self.commands)
        self.commands.set_bot(self.bot)

    def run(self):
        self.bot.running()


if __name__ == "__main__":
    Application().run()
