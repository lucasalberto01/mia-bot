import discord
from discord.ext import commands
import random

from cerebro import *
from info import *

description = '''An example bot to showcase the discord.ext.commands extension
module.


There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def start(ctx):
    """Adds two numbers together."""
    await ctx.send('Olá. Me chamo Mia e to aqui para conversar contigo :3')

#### HISTORICO ## COMANDO PUBLICO ####


@bot.command(pass_context=True)
async def historico(ctx,):
    """Adds two numbers together."""
    conn = sqlite3.connect('banco_de_dados.db')
    c = conn.cursor()
    id_usuario = int(ctx.message.author.id)
    li = ['📂 Historico de pontos 📂\n']

    for i in c.execute("SELECT frase, humor FROM historico WHERE id = '%s'" % id_usuario):
        li.append('🔖 {} - {} ponto'.format(i[0], i[1]))

    saida0 = '\n'.join(li)
    await ctx.send(saida0)
    conn.commit()


@bot.command(pass_context=True)
async def teste(ctx, member: discord.Member):
    print('id ->', member.id)

#### ZERO ### COMANDO SUDO ####


@bot.command(pass_context=True)
async def zero(ctx, member: discord.Member):
    """Adds two numbers together."""
    if int(ctx.message.author.id) == int(393814222452162562) or int(ctx.message.author.id) == int(434817433367347212):

        if member == None:
            await ctx.send('Esse comando tem q ser usando Marcando o Usuario')

        else:
            id_usuario = member.id
            nome_usuario = member.name
            frase = '🆕 Mudando dados do banco de dados do usuario {}'
            numero = 0

            conn = sqlite3.connect('banco_de_dados.db')
            c = conn.cursor()
            humor = 'Neutro'
            pontos = 1
            c.execute('UPDATE usuarios SET humor = ?, pontos = ? WHERE id = ?',
                      (humor, pontos, id_usuario))
            conn.commit()

            await ctx.send(frase.format(nome_usuario))

    else:
        print('no adm')

#### ZERO ### COMANDO SUDO ####


@bot.command(pass_context=True)
async def giff(ctx,):
    """Adds two numbers together."""
    if int(ctx.message.author.id) == int(393814222452162562) or int(ctx.message.author.id) == int(434817433367347212):
        file = discord.File("gif/1.gif", filename="file.gif")
        await ctx.send(file=file)
    else:
        print('no adm')

#### STATUS ### COMANDO PUBLICO ####


@bot.command(pass_context=True)
async def status(ctx,):
    ## ID -- NOME -- USER -- HUMOR -- PONTOS
    conn = sqlite3.connect('banco_de_dados.db')
    c = conn.cursor()
    id_usuario = int(ctx.message.author.id)

    for i in c.execute("SELECT * FROM usuarios WHERE id = '%s'" % id_usuario):

        pontos = i[4]
        humor = i[3]
        frase = '🌸 Pontos: {}\n🌸 Humor: {}'
        await ctx.send(frase.format(pontos, humor))

    conn.commit()


#### STATUS ### COMANDO PUBLICO ####
@bot.command(pass_context=True)
async def rank(ctx,):
    ## ID -- NOME -- USER -- HUMOR -- PONTOS
    if int(ctx.message.author.id) == int(393814222452162562) or int(ctx.message.author.id) == int(434817433367347212):
        conn = sqlite3.connect('banco_de_dados.db')
        c = conn.cursor()
        li = ['Rank de pontos\n']

        for i in c.execute("SELECT pontos, user FROM usuarios ORDER BY pontos DESC LIMIT 10"):
            li.append(':beginner: **{}** : {} pontos'.format(i[1], i[0]))

        saida0 = '\n'.join(li)
        await ctx.send(saida0)

        conn.commit()

#### STATUS ### COMANDO PUBLICO ####


@bot.command(pass_context=True)
async def unrank(ctx,):
    ## ID -- NOME -- USER -- HUMOR -- PONTOS
    if int(ctx.message.author.id) == int(393814222452162562) or int(ctx.message.author.id) == int(434817433367347212):
        conn = sqlite3.connect('banco_de_dados.db')
        c = conn.cursor()
        li = ['Rank de pontos\n']

        for i in c.execute("SELECT pontos, user FROM usuarios ORDER BY pontos ASC LIMIT 10"):
            li.append(':beginner: **{}** : {} pontos'.format(i[1], i[0]))

        saida0 = '\n'.join(li)
        await ctx.send(saida0)

        conn.commit()


def enviar(message, aa):
    message.channel.send(aa)


@bot.event
bot.run('NDI4MzMwMTY4NTAzODk0MDM4.DaFYHg.aEfh8h8JkoXljoVviUleGFVXdXk')
