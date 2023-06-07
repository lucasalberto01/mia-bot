

from src.controller.telegram import TelegramBot
from src.brain import Brain
from src.command import Command
from src.data_layer import DataLayer


class Application:
    def __init__(self):
        self.data_layer = DataLayer()
        self.brain = Brain()
        self.commands = Command(self.data_layer, self.brain)
        self.bot = TelegramBot(self.commands)
        self.commands.set_bot(self.bot)

    def run(self):
        self.bot.running()
        self.bot.sendMessage("Hello, world!")
        self.bot.sendPhoto("Hello, world!", "photo.jpg")
        self.bot.getUserId("Hello, world!")


if __name__ == "__main__":
    Application().run()
