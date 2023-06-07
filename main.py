

import discord
from src.controller.telegram import TelegramBot
from src.controller.discord import DiscordBot
from src.brain import Brain
from src.command import Command
from src.data_layer import DataLayer
from dotenv import load_dotenv
import os
load_dotenv()


class Application:
    def __init__(self):
        self.data_layer = DataLayer()
        self.brain = Brain(self.data_layer)
        self.commands = Command(self.data_layer, self.brain)
        # self.bot = DiscordBot(self.commands)
        intents = discord.Intents.default()
        intents.message_content = True

        self.bot = DiscordBot(self.commands, intents)
        self.commands.set_bot(self.bot)

    def run(self):
        self.bot.run(os.getenv('TOKEN_DISCORD'))
        # self.bot.running()


if __name__ == "__main__":
    Application().run()
