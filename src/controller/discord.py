
import discord
from dotenv import load_dotenv
from src.command import Command
from src.interfaces import IntegrationBot
from src.utils.typings import IServer, IUser
load_dotenv()


class DiscordBot(discord.Client, Command, IntegrationBot):
    def __init__(self, commands_bot: Command, intents=None):
        super().__init__(intents=intents)
        self.commands_bot = commands_bot

    """ Discord Bot """

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.content.startswith('?'):
            if message.content.startswith('?status'):
                user = IUser(message.author.id, message.author.name, message.author.discriminator)
                response = self.commands_bot.status(user)
                await message.channel.send(response)

            if message.content.startswith('?history'):
                user = IUser(message.author.id, message.author.name, message.author.discriminator)
                response = self.commands_bot.history(user)
                await message.channel.send(response)

        user = IUser(message.author.id, message.author.name, message.author.discriminator)
        server = IServer(message.channel.id, message.channel.name)
        message = message.content

        await self.commands_bot.thinking(message, user, 1, server, False)

    async def send_message(self, chat_id, message):
        """ Send message """
        print("send_message")
        print(chat_id)
        channel = self.get_channel(chat_id)
        await channel.send(message)

    async def send_reply(self, chat_id, message, reply_message_id):
        """ Send reply message """
        await self.get_channel(chat_id).send(message)

    async def send_photo(self, chat_id, photo, message=None):
        """ Send photo """
        await self.get_channel(chat_id).send(message, file=discord.File(photo))

    async def send_git(self, chat_id, gif, message=None):
        """ Send gif """
        await self.get_channel(chat_id).send(message, file=discord.File(gif))

    async def send_action(self, chat_id):
        """ Send action typing in chat """
        pass
