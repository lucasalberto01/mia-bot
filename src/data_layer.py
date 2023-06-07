#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import gmtime, strftime
from src.database.connect import session
from src.database.model.Conversation import Conversation
from src.database.model.History import History
from src.database.model.User import User
from src.database.model.UserActive import UserActive
from src.database.model.UserGroup import UserGroup


class DataLayer:
    """ Layer of connection to database"""

    def __init__(self) -> None:
        self.session = session

    def check_exist_user(self, id: int, nome: str, user: str) -> bool:
        """
        Verifica se o usuário existe no banco de dados

        :param id: id do usuário
        :param nome: nome do usuário
        :param user: username do usuário
        :return: True se existir, False se não existir
        """

        exist = self.session.query(User).filter_by(id=id).first()
        if exist:
            print('Ja ta no banco de dados geral')
            return False

        print('Nao ta no banco de dados geral')
        new_user = User(id=id, nome=nome, user=user, humor='Neutro', pontos=0)
        self.session.add(new_user)
        self.session.commit()
        return True

    def check_exist_user_group(self, user_id, group_id) -> bool:
        """
        Verifica se o usuário existe no grupo

        :param user_id: id do usuário
        :param group_id: id do grupo
        :return: True se existir, False se não existir
        """

        exist = session.query(UserGroup).filter_by(
            id_grupo=group_id,
            id_usuario=user_id
        ).first()
        return True if exist else False

    def welcome_message(self, id_usuario, nome_usuario, user, id_grupo, nome_grupo):
        """
        Gera mensagem de boas vindas para o usuário depenando dos grupos que ele esta

        :param id_usuario: id do usuário
        :param nome_usuario: nome do usuário
        :param user: username do usuário
        :param id_grupo: id do grupo
        :param nome_grupo: nome do grupo
        :return: mensagem de boas vindas
        """
        groups_name = []

        all_groups = session.query(
            UserGroup
        ).filter_by(
            id_usuario=id_usuario
        ).all()

        for group in all_groups:
            groups_name.append(group.nome_grupo)

        new_user = len(all_groups) == 0

        if new_user:
            insert_user = UserGroup(
                id_grupo=id_grupo,
                id_usuario=id_usuario,
                nome_grupo=nome_grupo,
                nome_usuario=nome_usuario,
                user_usuario=user
            )
            session.add(insert_user)
            session.commit()

        if new_user:
            return 'Oii {} eu nunca te conheci.\nBora conversar'.format(nome_usuario)

        else:
            insert_user = UserGroup(
                id_grupo=id_grupo,
                id_usuario=id_usuario,
                nome_grupo=nome_grupo,
                nome_usuario=nome_usuario,
                user_usuario=user
            )
            session.add(insert_user)
            session.commit()
            groups_names = ' e '.join(groups_name)
            return 'Olá {}. Eu sempre te vejo no grupo {}.\nE ai, ta tudo bem ?'.format(nome_usuario, groups_names)

    def update_mood(self, user_id) -> None:
        """
        Update mood of user for me 
        param user_id: id of user
        """

        user = session.query(User).filter_by(id=user_id).first()
        points = user.pontos

        if points in [-5, -6, -7]:
            user.humor = 'Block'
        elif points in range(-4, 5):
            user.humor = 'Neutro'
        elif points in range(5, 20):
            user.humor = 'Fofa'
        elif points > 20:
            user.humor = 'Sexy'

        session.commit()
        return

    def remove_point(self, user_id: int, msg: str) -> None:
        """ 
        Remove point from user 

        :param user_id: id of user
        :param msg: message by trigger function
        """

        now = strftime("%Y%m%d%H%M", gmtime())
        user = session.query(User).filter_by(id=user_id).first()
        user.pontos -= 1

        new_history = History(
            user_id=user_id,
            frase=msg,
            humor="➖",
            pontos=user.pontos,
            tempo=now
        )
        session.add(new_history)
        session.commit()
        return

    def last_message(self, use_id: int, msg: str, username: str, name: str) -> bool:
        """
        Check if last message is equal to current message

        :param use_id: id of user
        :param msg: message send by user
        :param username: username of user
        :param name: name of user

        """
        tempo = strftime("%Y%m%d%H%M", gmtime())

        user = session.query(Conversation).filter_by(id=use_id).first()

        if user:
            last_msg = user.fala

            if last_msg == msg:
                self.remove_point(use_id, msg)
                return True
            else:
                user.fala = msg
                session.commit()
                return False
        else:
            new_user = Conversation(
                id=use_id,
                nome=name,
                user=username,
                fala=msg,
                tempo=tempo
            )
            session.add(new_user)
            session.commit()
            return False

    def server_active(self, groupId: int, groupName: str):
        """
        Users recently active in group

        :param groupId: id of group
        :param groupName: name of group

        """
        if groupId != None and groupName != None:
            tempo = strftime("%Y%m%d%H%M%S", gmtime())
            group = session.query(UserActive).filter_by(id=groupId).first()

            if group == None:
                insert_group = UserActive(
                    id=groupId,
                    nome=groupName,
                    tempo=tempo
                )
                session.add(insert_group)
                session.commit()

            else:
                group.tempo = tempo
                session.commit()
