import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from src.interfaces import IntegrationBot
from src.brain import Brain
from src.command import Command


load_dotenv()


class TelegramBot(IntegrationBot):
    """ Telegram Bot """

    def __init__(self, commands: Command) -> None:
        self.token = os.getenv("TOKEN_TELEGRAM")
        self.commands = commands
        self.application = Application.builder().token(self.token).build()

    async def start(self, update: Update, context: ContextTypes):
        return self.commands.execute("start")

    async def status(self, update: Update, context: ContextTypes):
        return self.commands.execute("status")

    async def info(self, update: Update, context: ContextTypes):
        return self.commands.execute("info")

    async def check(self, update: Update, context: ContextTypes):
        return self.commands.execute("check")

    async def clear(self, update: Update, context: ContextTypes):
        return self.commands.execute("clear")

    async def plublicar(self, update: Update, context: ContextTypes):
        return self.commands.execute("publicar")

    async def thinking(self, update: Update, context: ContextTypes):
        bot = context.bot
        message = update.message
        reply_id = message.reply_to_message.message_id if message.reply_to_message else None

        user_id = int(message.from_user.id)
        user_nome = str(message.from_user.full_name)
        user_username = str(message.from_user.username)

        # is_reply_of_me = message.reply_to_message and message.reply_to_message.from_user.id == bot.id

        try:
            serve_id = int(message.chat.id)
            serve_nome = str(message.chat.title)
        except:
            serve_id = None
            serve_nome = None

        await self.commands.thinking(message.text, user_id, user_nome, user_username, reply_id, serve_id, serve_nome)

    async def send_message(self, chat_id, message):
        await self.application.bot.send_message(chat_id=chat_id, text=message)

    async def send_reply(self, chat_id, message, reply_message_id):
        await self.application.bot.send_message(chat_id=chat_id, text=message, reply_to_message_id=reply_message_id)

    async def send_photo(self, chat_id, photo, message=None):
        await self.application.bot.send_photo(chat_id=chat_id, photo=photo, caption=message)

    async def send_action(self, chat_id):
        await self.application.bot.send_chat_action(chat_id=chat_id, action="typing")

    def running(self):

        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("status", self.status))
        self.application.add_handler(CommandHandler("info", self.info))
        self.application.add_handler(CommandHandler("check", self.check))
        self.application.add_handler(CommandHandler("clear", self.clear))
        self.application.add_handler(CommandHandler("publicar", self.plublicar))
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.thinking))
        self.application.run_polling()
        return
