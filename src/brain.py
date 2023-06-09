#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import gmtime, strftime
from src.data_layer import DataLayer
from src.utils.clear import Clear
from libs import aiml


class Brain:
    def __init__(self, data_layer: DataLayer) -> None:
        self.data_layer = data_layer
        self.clean = Clear()
        
        # Load AIML files
        self.ai_neutra = aiml.Kernel()
        self.ai_neutra.setPredicate('name', 'Mia')
        self.ai_fofa = aiml.Kernel()
        self.ai_fofa.setPredicate('name', 'Mia')
        self.ai_irritada = aiml.Kernel()
        self.ai_irritada.setPredicate('name', 'Mia')
        self.ai_sexy = aiml.Kernel()
        self.ai_sexy.setPredicate('name', 'Mia')

        self.load_brain()

    def response_by_mood(self, humor: str, msg: str, user_id: int) -> str:
        print('>>>>>> Entrada: ', msg)
        response = ''
        if humor == 'Neutro':
            response = self.ai_neutra.respond(msg, user_id)

        elif humor == 'Fofa':
            response = self.ai_fofa.respond(msg, user_id)

        elif humor == 'Irritada':
            response = self.ai_irritada.respond(msg, user_id)

        elif humor == 'Sexy':
            response = self.ai_sexy.respond(msg, user_id)

        elif humor == 'Block':
            response = 'Vc está permanentemente bloqueado pela bot por **mau comportamento**.\n\nEntre em contato com os desenvolvedores pelo link na descrição do bot para reverter a situação'

        return response
    
    
    def load_brain(self) -> None:
        self.ai_neutra.resetBrain()
        self.ai_neutra.learn('brain/neutro.xml')
        self.ai_neutra.respond('load aiml b')
        self.ai_fofa.resetBrain()
        self.ai_fofa.learn('brain/fofa.xml')
        self.ai_fofa.respond('load aiml b')
        self.ai_irritada.resetBrain()
        self.ai_irritada.learn('brain/irritada.xml')
        self.ai_irritada.respond('load aiml b')
        self.ai_sexy.resetBrain()
        self.ai_sexy.learn('brain/sexy.xml')
        self.ai_sexy.respond('load aiml b')
        return

    def chat(self, message: str, user_id: int):
        message = self.clean.normalize_message(message)
        
        user = self.data_layer.get_user(user_id)
        
        response = self.response_by_mood(user.humor, message, user_id)
        
        time_now = int(strftime("%Y%m%d%H%M", gmtime()))
        time_last = self.data_layer.get_time_by_conversation(user_id)

        final = ''
        pontos = user.pontos
        events = response.split('§')

        for event in events:
            if time_now > time_last:
                if event == 'addpoint':
                    pontos2 = pontos + 1
                    print('adicionar um ponto')
                    final = '#Ganhou um pontinho cmg 😝'
                    self.data_layer.set_point(message, user_id, pontos2, '➕')
                    
                elif event == 'addpoint-s':
                    pontos2 = pontos + 1
                    self.data_layer.set_point(message, user_id, pontos2, '➕')

                elif event == 'removepoint':
                    pontos2 = pontos - 1
                    print('remover um ponto')
                    final = '#Perdeu um ponto cmg 😥'
                    self.data_layer.set_point(message, user_id, pontos2, '➖')

                elif event == 'removepoint-s':
                    pontos2 = pontos - 1
                    print('remover um ponto')
                    self.data_layer.set_point(message, user_id, pontos2, '➖')

        return events[0] + final
