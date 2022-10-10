#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import gmtime, strftime
from database.engine import session
from database.model.Conversation import Conversation
from database.model.History import History
from database.model.User import User
from database.model.UserActive import UserActive
from database.model.UserGroup import UserGroup


def checkExistUser(id: int, nome: str, user: str) -> bool:
    """
    Verifica se o usuário existe no banco de dados

    :param id: id do usuário
    :param nome: nome do usuário
    :param user: username do usuário
    :return: True se existir, False se não existir
    """

    exist = session.query(User).filter_by(id=id).first()
    if exist:
        print('Ja ta no banco de dados geral')
        return False

    print('Nao ta no banco de dados geral')
    new_user = User(id=id, nome=nome, user=user, humor='Neutro', pontos=0)
    session.add(new_user)
    session.commit()
    return True


def checkExistUserGroup(user_id, group_id) -> bool:
    """
    Verifica se o usuário existe no grupo

    :param user_id: id do usuário
    :param group_id: id do grupo
    :return: True se existir, False se não existir
    """

    exist = session.query(UserGroup).filter_by(
        id_grupo=group_id, id_usuario=user_id).first()
    return False if exist else True


def welcomeMessage(id_usuario, nome_usuario, user, id_grupo, nome_grupo):
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


def update_humor(id) -> None:
    ## ID -- NOME -- USER -- HUMOR -- PONTOS

    user = session.query(User).filter_by(id=id).first()
    pontos = user.pontos
    print(pontos)

    if pontos == -5 or pontos == -6 or pontos == -7:
        user.humor = 'Block'

    if pontos == -4 or pontos == -3 or pontos == -2 or pontos == -1 or pontos == 0 or pontos == 1 or pontos == 2 or pontos == 3 or pontos == 4:
        user.humor = "Neutro"

    if pontos == 5 or pontos == 6 or pontos == 7 or pontos == 8 or pontos == 9 or pontos == 10 or pontos == 11 or pontos == 12 or pontos == 13 or pontos == 14 or pontos == 15 or pontos == 16 or pontos == 17 or pontos == 18 or pontos == 19:
        user.humor = 'Fofa'

    if pontos > 20:
        user.humor = 'Sexy'

    session.commit()
    return


def ajuda_aiml(msg):
    add = '''
	<category>
    \t<pattern>{}</pattern>
    \t<template>
    \t\t-
    \t</template>
    </category>\n

	'''
    # Abra o arquivo (leitura)
    arquivo = open('aiml.xml', 'r')
    conteudo = arquivo.readlines()

    # insira seu conteúdo
    # obs: o método append() é proveniente de uma lista
    conteudo.append(add.format(msg))

    # Abre novamente o arquivo (escrita)
    # e escreva o conteúdo criado anteriormente nele.
    arquivo = open('aiml.xml', 'w')
    arquivo.writelines(conteudo)
    arquivo.close()


def removePoint(user_id, msg) -> None:
    tempo = strftime("%Y%m%d%H%M", gmtime())
    user = session.query(User).filter_by(id=user_id).first()
    user.pontos -= 1
    new_history = History(
        id=user_id,
        frase=msg,
        humor="➖",
        pontos=user.pontos,
        tempo=tempo
    )
    session.add(new_history)
    session.commit()
    return


def ultima_mensagem(use_id: int, msg: str, username: str, name: str) -> bool:
    ## ID -- NOME -- USER -- FALA
    # CONFERE SE A ULTIMA MENSAGEM É REPETIDA E TBM SALVA A ULTIMA MENSAGEM E SE A PESSOA NÃO TIVER NO BANDO DE DADOS ADD
    tempo = strftime("%Y%m%d%H%M", gmtime())
    # CONFERE PARA VE SE A PESSOA TA NO BANCO DE DADOS DE CONVERSAS

    user = session.query(Conversation).filter_by(id=use_id).first()

    if user:
        last_msg = user.fala
        if last_msg == msg:
            removePoint(use_id, msg)
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


def ativos(id_grupo, nome_grupo):
    if id_grupo != None and nome_grupo != None:
        tempo = strftime("%Y%m%d%H%M%S", gmtime())
        group = session.query(UserActive).filter_by(id=id_grupo).first()

        if group == None:
            insert_group = UserActive(
                id=id_grupo,
                nome=nome_grupo,
                tempo=tempo
            )
            session.add(insert_group)
            session.commit()

        else:
            group.tempo = tempo
            session.commit()
