import os
from src.adapters.telegram import TelegramBot
from src.adapters.discord import DiscordBot
from src.brain import Brain
from src.command import Command
from src.data_layer import DataLayer
from dotenv import load_dotenv

load_dotenv()


class Application:
    def __init__(self):
        self.data_layer = DataLayer()
        self.brain = Brain(self.data_layer)
        self.commands = Command(self.data_layer, self.brain)
        self.use = os.getenv("USE")
        self.token = None
        print(f"USE: {self.use}")

        if self.use == 'DISCORD':
            self.token = os.getenv("TOKEN_DISCORD")
            self.bot = DiscordBot(self.commands)

        elif self.use == 'TELEGRAM':
            self.token = os.getenv("TOKEN_TELEGRAM")
            self.bot = TelegramBot(self.commands)

        else:
            raise Exception("USE not defined")

        self.commands.set_bot(self.bot)

    def run(self):
        self.bot.run(self.token)


if __name__ == "__main__":
    app = Application()
    try:
        app.run()
    except KeyboardInterrupt:
        print("Bye")
