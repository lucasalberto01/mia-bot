import random
from src.data_layer import DataLayer
from src.utils.log import logger
from src.utils.clear import Clear
from src.brain import Brain
from src.interfaces import IntegrationBot
from src.utils import actions


class Command:
    def __init__(self, data_layer: DataLayer, brain: Brain):
        self.data_layer = data_layer
        self.brain = brain
        self.utils = Clear()
        self.bot = None

    def set_bot(self, bot: IntegrationBot):
        """ Set bot instance """
        self.bot = bot

    def execute(self, command):
        if command == "start":
            return "Oii, Meu nome é Mia e eu estou aqui para conversar! Bora bater um papo cabeça"

        elif command == "info":
            return "Eu sou a Mia, uma inteligência artificial criada para conversar com vocês."

    async def thinking(self, msg, user_id, user_name, user_username, reply_id, server_id, server_name):
        """ Process message """

        self.data_layer.check_exist_user(user_id, user_name, user_username)

        if server_id is not None:
            if not self.data_layer.check_exist_user_group(user_id, server_id):
                logger.info("Novo usuário no grupo")
                message = self.data_layer.welcome_message(user_id, user_name, user_username, server_id, server_name)
                await self.bot.send_message(server_id, message)

        if self.utils.check_name_bot(msg):
            await self.bot.send_action(server_id)

            self.data_layer.server_active(server_id, server_name)

            if self.data_layer.last_message(user_id, msg, user_username, user_name):
                await self.bot.send_message(server_id, "🌸 Oii, eu sou a Mia, e estou aqui para conversar! Bora bater um papo cabeça 🌸")

            first_message = True
            response_ai = self.brain.chat(msg, user_id)
            logger.info("Response AI: %s", response_ai)

            for sentence in response_ai.split("#"):
                action = actions.ACTIONS.get(sentence)
                if action:
                    if 'path' in action:
                        if 'max_index' in action:
                            img = random.randint(1, action['max_index'])
                            file = open(action['path'].format(img), 'rb')
                        else:
                            file = open(action['path'], 'rb')

                        if 'private' in action:
                            await self.bot.send_photo(user_id, file)
                        else:
                            await self.bot.send_photo(server_id, file)

                    elif 'file' in action:
                        await self.bot.send_photo(server_id, action['file'])

                else:
                    if first_message:
                        await self.bot.send_reply(server_id, sentence, reply_id)
                        first_message = False
                    else:
                        await self.bot.send_message(server_id, sentence)

            return
