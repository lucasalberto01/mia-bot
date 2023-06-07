#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unicodedata import normalize
from time import gmtime, strftime

from sqlalchemy import update
from src.database.connect import session
from src.database.model.User import User
from src.database.model.History import History
from src.database.model.Conversation import Conversation
import src.libs.aiml as aiml


class Brain:
    def __init__(self):
        self.ai_neutra = aiml.Kernel()
        self.ai_neutra.learn('brain/neutro.xml')
        self.ai_neutra.respond('load aiml b')
        print('\n')

        self.ai_fofa = aiml.Kernel()
        self.ai_fofa.learn('brain/fofa.xml')
        self.ai_fofa.respond('load aiml b')
        print('\n')

        self.ai_puta = aiml.Kernel()
        self.ai_puta.learn('brain/puta.xml')
        self.ai_puta.respond('load aiml b')
        print('\n')

        self.ai_sexy = aiml.Kernel()
        self.ai_sexy.learn('brain/sexy.xml')
        self.ai_sexy.respond('load aiml b')
        print('\n')

    def chat2(self, msg, id) -> str:
        return self.ai_neutra.respond(msg, id)

    def getUser(self, id) -> User:
        user = session.query(User).filter_by(id=id).first()
        if not user:
            raise Exception('User not found')
        return user

    def getTimeByConversation(self, id) -> int:
        conversation = session.query(Conversation).filter_by(id=id).first()
        return int(conversation.tempo) + 10 if conversation else 0

    def setPoint(self, msg: str, id: int, point: int, emoji: str) -> None:
        time_now: int = int(strftime("%Y%m%d%H%M", gmtime()))
        update(User).where(User.id == id).values(pontos=point)
        update(
            Conversation
        ).where(
            Conversation.id == id
        ).values(
            tempo=time_now
        )

        history = History(
            user_id=id,
            frase=msg,
            humor=emoji,
            pontos=point,
            tempo=time_now
        )
        session.add(history)
        session.commit()

    def applyDictionary(self, msg: str) -> str:
        # dicionario
        # --------------- palavra antiga -- palavra nova
        msg1 = normalize(
            'NFKD', msg
        ).encode(
            'ASCII', 'ignore'
        ).decode(
            'ASCII'
        ).lower()
        msg1 = ' ' + msg1

        msg1 = msg1.replace(' voce', ' vc')
        msg1 = msg1.replace(' mia ', '')
        msg1 = msg1.replace(' nudez', ' nude')
        msg1 = msg1.replace(' privado', ' pv')
        msg1 = msg1.replace(' pvd', ' pv')
        msg1 = msg1.replace(' obrigado', ' obg')
        msg1 = msg1.replace(' brigado', ' obg')
        msg1 = msg1.replace(' ond', ' onde')
        msg1 = msg1.replace(' aonde', ' onde')
        msg1 = msg1.replace(' zap', ' wpp')
        msg1 = msg1.replace(' whatsapp', ' wpp')
        msg1 = msg1.replace(' wts', ' wpp')
        msg1 = msg1.replace(' ft', ' foto')
        msg1 = msg1.replace(' peitos', ' tetas')
        msg1 = msg1.replace(' peito', ' tetas')
        msg1 = msg1.replace(' teta', ' tetas')
        msg1 = msg1.replace(' tc', ' fala')
        # msg1 = msg1.replace(' d', ' de')
        msg1 = msg1.replace(' vamos', ' vamo')
        msg1 = msg1.replace(' foda-se', ' fodase')
        msg1 = msg1.replace(' fds', ' fodase')
        msg1 = msg1.replace(' nois', ' nos')
        msg1 = msg1.replace(' comigo', 'cmg')

        if (msg == 'mia') or (msg == 'MIA'):
            msg1 = 'mia'

        return msg1

    def responseByHumor(self, humor: str, msg: str, id: int) -> str:
        response = ''
        if humor == 'Neutro':
            response = self.ai_neutra.respond(msg, id)

        elif humor == 'Fofa':
            response = self.ai_fofa.respond(msg, id)

        elif humor == 'Puta':
            response = self.ai_puta.respond(msg, id)

        elif humor == 'Sexy':
            response = self.ai_sexy.respond(msg, id)

        elif humor == 'Block':
            response = 'Vc está permanentemente bloqueado pela bot por **mau comportamento**.\n\nEntre em contato com os desenvolvedores pelo link na descrição do bot para reverter a situação'

        return response

    def chat(self, msg: str, id: int):
        response: str = ''
        msg1: str = self.applyDictionary(msg)
        user = self.getUser(id)
        print('User: H: {}, PL {}', user.humor, user.pontos)
        print('Input of AI->', msg1)
        response = self.responseByHumor(user.humor, msg1, id)
        print('Output of AI->', response)

        time_now: int = int(strftime("%Y%m%d%H%M", gmtime()))
        time_last = self.getTimeByConversation(id)

        final: str = ''
        pontos: int = user.pontos
        events: list[str] = response.split('§')

        print(time_now)
        print(time_last)

        for event in events:
            if event == 'addpoint':
                if time_now > time_last:
                    pontos2 = 1 + pontos
                    print('adicionar um ponto')
                    final = '#Ganhou um pontinho cmg 😝'
                    self.setPoint(msg, id, pontos2, '➕')

            elif event == 'addpoint-s':
                if time_now > time_last:
                    pontos2 = 1 + pontos
                    self.setPoint(msg, id, pontos2, '➕')

            elif event == 'removepoint':
                pontos2 = pontos - 1
                print('remover um ponto')
                final = '#Perdeu um ponto cmg 😥'
                self.setPoint(msg, id, pontos2, '➖')

            elif event == 'removepoint-s':
                pontos2 = pontos - 1
                print('remover um ponto')
                self.setPoint(msg, id, pontos2, '➖')

        return events[0] + final
