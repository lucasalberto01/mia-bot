
import discord
from dotenv import load_dotenv
from src.command import Command
from src.interfaces import IntegrationBot
from src.utils.typings import IChannel, IUser
load_dotenv()


class DiscordBot(discord.Client, IntegrationBot):
    """ Discord Bot interface """

    def __init__(self, commands_bot: Command):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.commands_bot = commands_bot

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message: discord.Message):
        user = IUser(message.author.id, message.author.name, message.author.discriminator)
        if not message.guild is None:
            server = IChannel(message.channel.id, message.channel.name, message.guild.id, message.guild.name)
        else:
            server = IChannel(message.author.id, message.author.name, message.author.id, message.author.name, True)

        if message.author.id == self.user.id or message.author.bot:
            return

        if message.content.startswith('?'):
            if message.content.startswith('?status'):
                response = self.commands_bot.status(user)
                await message.channel.send(response)
                return

            if message.content.startswith('?history'):
                response = self.commands_bot.history(user)
                await message.channel.send(response)
                return

            if message.content.startswith('?gif'):
                response = self.commands_bot.gif()
                file = discord.File(response, filename="file.gif")
                resp = await message.channel.send(file=file)
                await resp.delete(delay=5)
                return

            if message.content.startswith('?reload'):
                response = self.commands_bot.reload()
                await message.channel.send(response)
                return

        is_response_of_me = message.reference is not None and message.reference.resolved.author.id == self.user.id

        await self.commands_bot.thinking(message.content, user, message.id, server, is_response_of_me)

    async def send_message(self, chat_id, message):
        await self.get_channel(chat_id).send(message)

    async def send_reply(self, chat_id, message, reply_message_id):
        reference = await self.get_channel(chat_id).fetch_message(reply_message_id)
        return await self.get_channel(chat_id).send(message, reference=reference)

    async def send_photo(self, chat_id: int, photo, message=None, private=False):
        if not private:
            channel = self.get_channel(chat_id)
            await channel.send(message, file=discord.File(photo))
        else:
            try:
                user = discord.utils.get(self.get_all_members(), id=chat_id)
                if user is not None:
                    await user.send(message, file=discord.File(photo))
                else:
                    print(f"User {chat_id} not found")
            except discord.errors.Forbidden:
                channel = self.get_channel(chat_id)
                await channel.send("Eita, não consigo enviar mensagem privada para você 😢")
                print(f"User {chat_id} not found")

    async def send_git(self, chat_id, gif, message=None):
        """ Send gif """
        await self.get_channel(chat_id).send(message, file=discord.File(gif))

    async def send_action(self, chat_id):
        """ Send action typing in chat """
        await self.get_channel(chat_id).typing()

    async def delete_message(self, chat_id, message_id):
        """ Delete message """
        message = await self.get_channel(chat_id).fetch_message(message_id)
        await message.delete()
