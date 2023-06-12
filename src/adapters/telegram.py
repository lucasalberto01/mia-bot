import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import concurrent.futures
from src.interfaces import IntegrationBot
from src.command import Command
from src.utils.typings import IUser, IChannel

load_dotenv()

class TelegramBot(IntegrationBot):
    """ Telegram Bot """

    def __init__(self, commands: Command):
        self.token = os.getenv("TOKEN_TELEGRAM")
        self.commands = commands
        self.application = None
        self.sudo_user: list[int] = list(map(int, os.getenv("SUDO_USER").split(',')))

    ### PUBLIC COMMANDS ###
    async def start(self, update: Update, context: ContextTypes):
        message = self.commands.start()
        await update.message.reply_text(message)

    async def status(self, update: Update, context: ContextTypes):
        user = IUser(
            user_id=update.message.from_user.id,
            user_nome=update.message.from_user.first_name,
            user_username=update.message.from_user.username
        )
        message = self.commands.status(user)
        await update.message.reply_text(message)

    async def info(self, update: Update, context: ContextTypes):
        # PEGAR DADOS
        chat = update.message.chat.type
        chat_titulo = update.message.chat.title
        nome_usuario = update.message.from_user.first_name
        user_usuario = update.message.from_user.username
        id_usuario = update.message.from_user.id
        id_chat = update.message.chat_id

        frase = 'Olá {}.\nAqui vai algumas informações sobre vc!\n\n👤 Nome: {}\n👤 User: @{}\n👤 Id: {}\n👥 Id do Grupo: {}\n👥 Chat do tipo: {}\n👥 Nome do grupo: {}\n'
        await update.message.reply_text(frase.format(nome_usuario, nome_usuario, user_usuario, id_usuario, id_chat, chat, chat_titulo))

    async def history(self, update: Update, context: ContextTypes):
        user = IUser(
            user_id=update.message.from_user.id,
            user_nome=update.message.from_user.first_name,
            user_username=update.message.from_user.username
        )
        response = self.commands.history(user)
        await update.message.reply_text(response)

    
    ### SUDO COMMANDS ###
    async def gif(self, update: Update, context: ContextTypes):
        if update.message.from_user.id not in self.sudo_user:
            return
        
        file = open('assets/gif/1.gif', 'rb')
        await update.message.reply_animation(file)
    
    async def check_group(self, group):
        try:
            group_id = group.id_grupo
            chat = await self.application.bot.get_chat(group_id)
            name_group = chat.title
            user_group = chat.username
            # await chat.send_message("Oiii, volte! 🚀")
            return [group_id, name_group, user_group]
        except Exception:
            return None
    
    async def check(self, update: Update, context: ContextTypes):
        if update.message.from_user.id not in self.sudo_user:
            return

        all_group = self.commands.all_group()
        li = []
        lo = ["Verificando Nome dos Grupos"]
        i = 0
        o = 0

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.check_group, group) for group in all_group]

            for future in concurrent.futures.as_completed(futures):
                result = await future.result()
                if result:
                    li.append(result)
                    lo.append('👥 {} - {} - @{}'.format(i, result[1], result[2]))
                    print('👥 {} - {} - @{}'.format(i, result[1], result[2]))
                else:
                    lo.append('❌ {} - {} - @{}'.format(i, result[1], result[2]))

                o += 1
                i += 1

                if o == 51:
                    msg = '\n'.join(lo)
                    await self.application.bot.send_message(chat_id=update.message.chat_id, text=msg)
                    lo.clear()
                    lo.append("Verificando Nome dos Grupos")
                    o = 1

        for group in li:
            print("Updating group: {}".format(group[1]))
            self.commands.update_name_group(group[0], group[1])

        msg = '\n'.join(lo)
        await self.application.bot.send_message(chat_id=update.message.chat_id, text=msg)
        await self.application.bot.send_message(chat_id=update.message.chat_id, text="Atualização finalizada")

                
    async def reload(self, update: Update, context: ContextTypes):
        if update.message.from_user.id not in self.sudo_user:
            return
        self.commands.reload()
        await update.message.reply_text("Reloaded")

    
    ### CONVERSATION ###
    async def thinking(self, update: Update, context: ContextTypes):
        bot = context.bot
        message = update.message
        reply_id = message.message_id

        user_id = int(message.from_user.id)
        user_nome = str(message.from_user.full_name)
        user_username = str(message.from_user.username)

        is_reply_of_me: bool = message.reply_to_message and message.reply_to_message.from_user.id == bot.id
        is_private: bool = message.chat.type == "private"

        try:
            serve_id = int(message.chat.id)
            serve_nome = str(message.chat.title)
        except Exception:
            serve_id = None
            serve_nome = None

        user = IUser(
            user_id=user_id,
            user_nome=user_nome,
            user_username=user_username
        )
        server = IChannel(serve_id, serve_nome, serve_id, serve_nome)

        await self.commands.thinking(message.text, user, reply_id, server, is_reply_of_me or is_private)
        
    ### INTEGRATION BOT ###
    async def send_message(self, chat_id, message):
        await self.application.bot.send_message(chat_id=chat_id, text=message)

    async def send_reply(self, chat_id, message, reply_message_id):
        await self.application.bot.send_message(chat_id=chat_id, text=message, reply_to_message_id=reply_message_id)

    async def send_photo(self, chat_id, photo, message=None, private=False):
        await self.application.bot.send_photo(chat_id=chat_id, photo=photo, caption=message)

    async def send_git(self, chat_id, gif, message=None):
        await self.application.bot.send_animation(chat_id=chat_id, animation=gif, caption=message)

    async def send_action(self, chat_id):
        await self.application.bot.send_chat_action(chat_id=chat_id, action="typing")

    def run(self, token: str):
        self.application = Application.builder().token(token).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("status", self.status))
        self.application.add_handler(CommandHandler("history", self.history))
        self.application.add_handler(CommandHandler("gif", self.gif))
        self.application.add_handler(CommandHandler("info", self.info))
        self.application.add_handler(CommandHandler("check", self.check))
        self.application.add_handler(CommandHandler("reload", self.reload))
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.thinking))
        self.application.run_polling()
