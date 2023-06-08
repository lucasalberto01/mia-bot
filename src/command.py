import random
from src.data_layer import DataLayer
from src.utils.log import logger
from src.utils.clear import Clear
from src.brain import Brain
from src.interfaces import IntegrationBot
from src.utils import actions
from src.utils.typings import IUser, IServer


class Command:
    """ Command """

    def __init__(self, data_layer: DataLayer, brain: Brain):
        self.data_layer = data_layer
        self.brain = brain
        self.utils = Clear()
        self.bot = None

    def set_bot(self, bot: IntegrationBot):
        """ Set bot instance """
        self.bot = bot

    ## COMMANDS ##

    def start(self,):
        return "Oii, Meu nome é Mia e eu estou aqui para conversar! Bora bater um papo cabeça"

    def status(self, user: IUser):
        points, humor = self.data_layer.get_status(user)
        message = '🌸 Pontos: {}\n🌸 Humor: {}'.format(points, humor)
        return message

    def history(self, user: IUser):
        """ Get history of user """
        history = self.data_layer.get_history(user)
        message = '📂 Historico de pontos 📂\n'
        for i in history:
            message += '🔖 {} - {} ponto\n'.format(i.frase, i.humor)
        return message

    def gif(self,):
        file = open('assets/gif/1.gif', 'rb')
        return file

    def reset(self,):
        self.brain.reload_brain()
        return "Resetado"

    ## ALL TEXTO MESSAGE ##

    async def thinking(self, msg: str, user: IUser, reply_id: int, server: IServer, force=False):
        """ Process message """

        self.data_layer.check_exist_user(user)

        if server.serve_id is not None:
            if not self.data_layer.check_exist_user_group(user.user_id, server.serve_id):
                logger.info("Novo usuário no grupo")
                message = self.data_layer.welcome_message(user, server)
                await self.bot.send_message(server.serve_id, message)
                return

        if self.utils.check_name_bot(msg) or force:
            await self.bot.send_action(server.serve_id)

            self.data_layer.server_active(server)

            if self.data_layer.last_message(user, msg):
                await self.bot.send_message(server.serve_id, "Pare de me mandar a mesma mensagem, eu não sou burra!")
                return

            first_message = True
            response_ai = self.brain.chat(msg, user.user_id)
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
                            await self.bot.send_photo(user.user_id, file)
                        else:
                            await self.bot.send_photo(server.serve_id, file)

                    elif 'file' in action:
                        await self.bot.send_photo(server.serve_id, action['file'])

                else:
                    if first_message:
                        await self.bot.send_reply(server.serve_id, sentence, reply_id)
                        first_message = False
                    else:
                        await self.bot.send_message(server.serve_id, sentence)

            return
