import os

import discord
from discord.ext import commands, tasks
from login import token  # NOQA

from sql.client import AsyncSQLiteClient

os.chdir(os.path.dirname(__file__))

client = commands.Bot(command_prefix=',')
client.remove_command('help')

sql_client = AsyncSQLiteClient()


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('To the MOOOOOON!!'))
    await sql_client.create()
    await sql_client.load()
    print("Bot is up and running baby!")


@tasks.loop(minutes=1)
async def save_sql():
    await sql_client.save()


def start():
    import commands as bot_cmds  # NOQA
    client.run(token)
