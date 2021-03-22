import os

import discord
from discord.ext import commands
from login import token  # NOQA

os.chdir(os.path.dirname(__file__))

client = commands.Bot(command_prefix=',')
client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('To the MOOOOOON!!'))
    print("Bot is up and running baby!")


def start():
    import commands as bot_cmds  # NOQA
    client.run(token)
