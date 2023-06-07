#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import gmtime, strftime
from src.data_layer import DataLayer
from src.utils.clear import Clear
from src.libs import aiml


class Brain:
    def __init__(self, data_layer: DataLayer) -> None:
        self.data_layer = data_layer
        self.clean = Clear()
        
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
        response = ''
        msg1 = self.clean.normalize_message(msg)
        user = self.data_layer.get_user(id)
        
        print('User: H: {}, PL {}', user.humor, user.pontos)
        print('Input of AI->', msg1)
        
        response = self.responseByHumor(user.humor, msg1, id)
        
        print('Output of AI->', response)

        time_now = int(strftime("%Y%m%d%H%M", gmtime()))
        time_last = self.data_layer.get_time_by_conversation(id)

        final = ''
        pontos = user.pontos
        events = response.split('§')

        print(time_now)
        print(time_last)

        for event in events:
            if time_now > time_last:
                if event == 'addpoint':
                    pontos2 = pontos + 1
                    print('adicionar um ponto')
                    final = '#Ganhou um pontinho cmg 😝'
                    self.data_layer.set_point(msg, id, pontos2, '➕')
                    
                elif event == 'addpoint-s':
                    pontos2 = pontos + 1
                    self.data_layer.set_point(msg, id, pontos2, '➕')

                elif event == 'removepoint':
                    pontos2 = pontos - 1
                    print('remover um ponto')
                    final = '#Perdeu um ponto cmg 😥'
                    self.data_layer.set_point(msg, id, pontos2, '➖')

                elif event == 'removepoint-s':
                    pontos2 = pontos - 1
                    print('remover um ponto')
                    self.data_layer.set_point(msg, id, pontos2, '➖')

        return events[0] + final
