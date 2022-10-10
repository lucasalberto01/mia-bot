import random
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from sqlalchemy import update as sql_update
from database.engine import session
from database.model.User import User
from database.model.UserGroup import UserGroup

from info import *
from cerebro import *

load_dotenv()

TOKEN = os.getenv("TOKEN")
brain = Brain()
SUDO = [199915939, 138662736, 174512760, 337730276]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.chat.send_message("Oii, Meu nome é Mia e eu estou aqui para conversar! Bora bater um papo cabeça")


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # PEGAR DADOS
    chat = update.message.chat.type
    chat_titulo = update.message.chat.title
    nome_usuario = update.message.from_user.first_name
    user_usuario = update.message.from_user.username
    id_usuario = update.message.from_user.id
    id_chat = update.message.chat_id

    frase = 'Olá {}.\nAqui vai algumas informações sobre vc!\n\n👤 Nome: {}\n👤 User: @{}\n👤 Id: {}\n👥 Id do Grupo: {}\n👥 Chat do tipo: {}\n👥 Nome do grupo: {}\n'
    await update.message.reply_text(frase.format(nome_usuario, nome_usuario, user_usuario, id_usuario, id_chat, chat, chat_titulo))


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = int(update.message.from_user.id)
    user = session.query(User).filter_by(id=user_id).first()
    pontos = user.pontos
    humor = user.humor
    frase = '🌸 Pontos: {}\n🌸 Humor: {}'
    await update.message.reply_html(frase.format(pontos, humor))


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = context.bot
    if update.message.from_user.id in SUDO:
        li = []
        lo = ['Verificando Nome dos grupos\n']
        i = 0
        o = 0
        all_groups = session.query(
            UserGroup.id_grupo.distinct().label("id_grupo"),
            UserGroup.nome_grupo
        ).all()
        for row in all_groups:
            try:
                id_grupo = row.id_grupo
                chat = await bot.getChat(id_grupo)
                nome_grupo = chat.title
                user_grupo = chat.username
                li.append([nome_grupo, id_grupo])
                lo.append('{} - {} User: @{}'.format(i, nome_grupo, user_grupo))
                print('Grupos -->', nome_grupo, '\tId - ', id_grupo)
            except:
                lo.append(
                    'Sem dados de {} - {}'.format(row.nome_grupo, row.id_grupo))

            o = o + 1
            i = i + 1

            if o == 51:
                msg = '\n'.join(lo)
                await bot.send_message(update.message.chat_id, msg)
                del lo[:]
                lo = []
                o = 1

        for group in li:
            print('Mudando -->', group[0], group[1])
            sql_update(UserGroup).where(
                UserGroup.id_grupo == [1]
            ).values(nome_grupo=group[0])

        msg = '\n'.join(lo)
        session.commit()
        await bot.send_message(update.message.chat_id, msg)
        await bot.send_message(update.message.chat_id, '🔰 Checagem concluída 🔰')


async def publicar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id in SUDO:
        bot = context.bot
        msg = update.message.text
        msg = msg.replace('/publicar ', '')
        all_groups = session.query(
            UserGroup.id_grupo.distinct().label("id_grupo"),
            UserGroup.nome_grupo
        ).all()
        for row in all_groups:
            try:
                id_grupo = row.id_grupo
                await bot.send_message(id_grupo, msg)
            except:
                print('Erro ao enviar mensagem para o grupo',
                      row.nome_grupo, row.id_grupo)
                pass


async def thinking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = context.bot
    ## CHAT ##
    message = update.message

    # PARAMENTOS INTERNOS
    primeira = True

    # MINERA INFORMAÇÕES
    usuario_id = int(message.from_user.id)
    usuario_nome = str(message.from_user.full_name)
    usuario_user = str(message.from_user.username)

    print(usuario_id)
    print(message.chat.id)

    is_reply_of_me = message.reply_to_message and message.reply_to_message.from_user.id == bot.id

    try:
        serve_id = int(message.chat.id)
        serve_nome = str(message.chat.title)
    except:
        serve_id = None
        serve_nome = None

    print('Recebi ->', str(usuario_nome))
    print('Recebi ->', str(serve_nome))
    print('Recebi ->', str(message.text))
    # CRIA A TABELA DE PONTOS E HUMOR PARA O USUÁRIO NOVO
    checkExistUser(usuario_id, usuario_nome, usuario_user)

    if (serve_id != None):
        if checkExistUserGroup(usuario_id, serve_id):
            # VIU Q É UMA PESSOA NOVA NAQUELE GRUPO, TENTA ACHAR INFORMAÇÕES SOBRE ELA
            print('Reconheceu uma pessoa nova')

            # VAI LÁ E PERGUNTA SE TEM ALGO DELA NO BANCO DE DADOS
            response = welcomeMessage(
                usuario_id, usuario_nome, usuario_user, serve_id, serve_nome)

            # MANDA A MENSAGEM
            await update.message.chat.send_message(response)

    # MUDA DE HUMOR DE ACORDO COM A PONTUAÇÃO
    # update_humor(usuario_id)
    entrada = str(message.text)
    print('Usuário ->', usuario_id)
    arr = entrada.split(' ')
    for b in arr:
        if is_reply_of_me or b in ["mia", "Mia", "mia.", ",mia" "Mia,", "mia?", "Mia?"]:
            await bot.send_chat_action(message.chat.id, 'typing')
            ativos(serve_id, serve_nome)
            if ultima_mensagem(usuario_id, entrada, usuario_user, usuario_nome) == True:
                await update.message.chat.send_message('Para de me manda a mesma mensagem😡 Perdeu um ponto cmg')
                return

            else:
                txt = brain.chat(entrada, usuario_id)
                print('Respondi ->', txt)
                for i in txt.split('#'):
                    if i == 'sendimg':
                        img = random.randint(1, 29)
                        file = open('assets/img/{}.jpg'.format(img), 'rb')
                        await context.bot.send_photo(serve_id, file)

                    elif i == 'sendimg-sexy':
                        img = random.randint(1, 8)
                        file = open('assets/img-sexy/{}.jpg'.format(img), 'rb')
                        await context.bot.send_photo(serve_id, file)

                    elif i == 'sendimg-dlc':
                        file = open('assets/img-especifica/1.jpg', 'rb')
                        await context.bot.send_photo(serve_id, file)

                    elif i == 'sendimg-gamer':
                        file = open('assets/img-especifica/2.jpg', 'rb')
                        await context.bot.send_photo(serve_id, file)

                    elif i == 'sendimg-sexyplus':
                        file = open('assets/img-sexyplus/1.jpg', 'rb')
                        await context.bot.send_photo(serve_id, file)

                    elif i == 'sendimg-vida':
                        file = open('assets/img-especifica/7.jpg', 'rb')
                        await context.bot.send_photo(serve_id, file)

                    elif i == 'sendimg-normal':
                        await bot.send_file(message.channel, 'AgADAQADuacxG7k8kEbFWluhXn2dkzuB3i8ABC0Q9YqWNbv7dIcBAAEC')

                    elif i == 'sendimg-minhacara':
                        await bot.send_file(message.channel, 'AgADAQADuqcxG7k8kEYJ5fl-BC5KZDGD3i8ABBBq7ktLrUN7qoABAAEC')

                    elif i == 'sendimg-tetas':
                        await bot.send_file(message.channel, 'AgADAQADu6cxG7k8kEZ_oTQhe3CUQHZc9y8ABKDiw_0aTld518YAAgI')

                    elif i == 'sendimg-gatinha':
                        await bot.send_file(message.channel, 'AgADAQADvKcxG7k8kEYLIJt_f-M7U2uf3i8ABFY5mZcB2PtEiC8BAAEC')

                    elif i == 'sendimg-nerd':
                        await bot.send_file(message.channel, 'AgADAQADvacxG7k8kEb98e8T7incuu2X3i8ABGtWWxXUvoyqGzEBAAEC')

                    elif i == 'meme-piada':
                        file = open('assets/meme/1.png', 'rb')
                        await context.bot.send_photo(serve_id, file)

                    elif i == 'sendimg-nude':
                        img = random.randint(1, 7)
                        await update.message.from_user.send_message("Toma seu nude amor")
                        file = open(
                            'assets/img-sexyplus/{}.jpg'.format(img), 'rb')
                        await update.message.from_user.send_photo(serve_id, file)

                    else:
                        if primeira:
                            await update.message.reply_text(i)
                            primeira = False
                        else:
                            await update.message.chat.send_message(i)
            break


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id in SUDO:
        bot = context.bot

        i = 1
        o = 1
        li = []
        lo = []

        await bot.send_message(update.message.chat_id,
                               'Limpando banco de dados de Grupos q ela não está')
        all_groups = session.query(
            UserGroup.id_grupo.distinct().label("id_grupo"),
            UserGroup.nome_grupo
        ).all()

        for row in all_groups:
            tr
            try:
                id_grupo = row.id_grupo
                chat = await bot.getChat(id_grupo)
                nome_grupo = chat.title
                txt = '{} - ✅ Grupo: {}'.format(i, nome_grupo)
                li.append(txt)

            except:
                print(e)
                print('Não consegui enviar para o ', row.id_grupo)
                txt = '{} - ❌ Grupo: {}\nDELETANDO DO DB'.format(
                    i, row.id_grupo)
                li.append(txt)
                lo.append(row.id_grupo)

            o = o + 1
            i = i + 1

            if o == 51:
                msg = '\n'.join(li)
                await bot.send_message(update.message.chat_id, msg)
                del li[:]
                li = []
                o = 1

        for row2 in lo:
            session.query(UserGroup).filter_by(id_grupo=row2).delete()
            print('Apagando ', row2)

        session.commit()
        msg = '\n'.join(li)
        left = len(all_groups) - len(lo)
        await bot.send_message(update.message.chat_id, msg)
        await bot.send_message(update.message.chat_id, '🔰 Limpeza concutida 🔰, sobrou {} grupos'.format(left))


def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("check", check))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(CommandHandler(
        "publicar", publicar))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, thinking))
    application.run_polling()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        session.close()
        exit()
