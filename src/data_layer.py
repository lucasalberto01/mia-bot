#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import gmtime, strftime
from src.database.connect import session
from src.database.model.Conversation import Conversation
from src.database.model.History import History
from src.database.model.User import User
from src.database.model.UserActive import UserActive
from src.database.model.UserGroup import UserGroup
from src.utils.typings import IUser, IChannel


class DataLayer:
    """ Layer of connection to database"""

    def __init__(self) -> None:
        self.session = session

    def get_user(self, id: int):
        """
        Get user by id

        :param id: id of user
        :return: user
        """
        user = self.session.query(User).filter_by(id=id).first()
        if not user:
            raise Exception('User not found')
        return user

    def get_time_by_conversation(self, id: int) -> int:
        """
        Get time by conversation

        :param id: id of user
        :return: time of last message
        """
        conversation = session.query(Conversation).filter_by(id=id).first()
        return int(conversation.tempo) + 10 if conversation else 0

    def set_point(self, msg: str, id: int, point: int, emoji: str) -> None:
        """
        Set point of user

        :param msg: message send by user
        :param id: id of user
        :param point: point of user
        :param emoji: emoji of user
        """

        time_now: int = int(strftime("%Y%m%d%H%M", gmtime()))
        user = session.query(User).filter_by(id=id).first()
        user.pontos += point

        new_history = History(
            user_id=id,
            frase=msg,
            humor=emoji,
            pontos=user.pontos,
            tempo=time_now
        )
        session.add(new_history)
        session.commit()
        return

    def check_exist_user(self, user: IUser) -> bool:
        """
        Verifica se o usuário existe no banco de dados

        :param id: id do usuário
        :param nome: nome do usuário
        :param user: username do usuário
        :return: True se existir, False se não existir
        """
        id = user.user_id
        nome = user.user_nome
        username = user.user_username

        exist = self.session.query(User).filter_by(id=id).first()
        if exist:
            print('Ja ta no banco de dados geral')
            return False

        print('Nao ta no banco de dados geral')
        new_user = User(id=id, nome=nome, user=username, humor='Neutro', pontos=0)
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

    def welcome_message(self, user: IUser, server: IChannel) -> str:
        """
        Gera mensagem de boas vindas para o usuário depenando dos grupos que ele esta

        :param id_usuario: id do usuário
        :param nome_usuario: nome do usuário
        :param user: username do usuário
        :param id_grupo: id do grupo
        :param nome_grupo: nome do grupo
        :return: mensagem de boas vindas
        """

        user_id = user.user_id
        name = user.user_nome
        username = user.user_username

        id_grupo = server.serve_id
        nome_grupo = server.serve_nome

        groups_name = []

        all_groups = session.query(
            UserGroup
        ).filter_by(
            id_usuario=user_id
        ).all()

        for group in all_groups:
            groups_name.append(group.nome_grupo)

        new_user = len(all_groups) == 0

        if new_user:
            insert_user = UserGroup(
                id_grupo=id_grupo,
                id_usuario=user_id,
                nome_grupo=nome_grupo,
                nome_usuario=name,
                user_usuario=username
            )
            session.add(insert_user)
            session.commit()

        if new_user:
            return 'Oii {} eu nunca te conheci.\nBora conversar'.format(name)

        else:
            insert_user = UserGroup(
                id_grupo=id_grupo,
                id_usuario=user_id,
                nome_grupo=nome_grupo,
                nome_usuario=name,
                user_usuario=username
            )
            session.add(insert_user)
            session.commit()
            groups_names = ' e '.join(groups_name)
            return 'Olá {}. Eu sempre te vejo no grupo {}.\nE ai, ta tudo bem ?'.format(name, groups_names)

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

    def last_message(self, user: IUser, msg: str) -> bool:
        """
        Check if last message is equal to current message

        :param use_id: id of user
        :param msg: message send by user
        :param username: username of user
        :param name: name of user

        """
        tempo = strftime("%Y%m%d%H%M", gmtime())
        user_id = user.user_id
        username = user.user_username
        name = user.user_nome

        user = session.query(Conversation).filter_by(id=user_id).first()

        if user:
            last_msg = user.fala

            if last_msg == msg:
                self.remove_point(user_id, msg)
                return True
            else:
                user.fala = msg
                session.commit()
                return False
        else:
            new_user = Conversation(
                id=user_id,
                nome=name,
                user=username,
                fala=msg,
                tempo=tempo
            )
            session.add(new_user)
            session.commit()
            return False

    def server_active(self, server: IChannel) -> None:
        """
        Users recently active in group

        :param groupId: id of group
        :param groupName: name of group

        """
        groupId = server.serve_id
        groupName = server.serve_nome

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

    def get_status(self, user: IUser) -> tuple[int, str]:
        """
        Get status of user

        :param user: user
        :return: points and mood of user
        """
        user = session.query(User).filter_by(id=user.user_id).first()
        return user.pontos, user.humor

    def get_history(self, user: IUser) -> list[History]:
        """
        Get history of user

        :param user: user
        :return: history of user
        """
        user = session.query(History).filter_by(user_id=user.user_id).all()
        return user
