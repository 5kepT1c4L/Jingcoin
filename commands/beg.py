import json
import random

import discord
from discord.ext import commands

from utils import get_bank_data, open_account
from ..bot import client


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    coins_recieved = random.randint(15, 61)

    people_beg_list = [
        'John Cena',
        'Barack Obama',
        'George Bush',
        'Joe Mama',
        "Mr. Clark"]
    users[str(user.id)]["Coins"] += coins_recieved
    coins_begged_embed = discord.Embed(
        title="You begged and " + random.choice(people_beg_list) + " gave you %s coins!" % coins_recieved,
        colour=discord.Colour.red(),
        description=None
    )
    coins_begged_embed.set_author(name=f"{ctx.author}'s command", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=coins_begged_embed)
    with open("jingcoin.json", "w") as f:
        json.dump(users, f)
    return True

@beg.error
async def on_beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        beg_too_fast = discord.Embed(
            title="WOAH calm your horse mate! You can use the command in {:.2f} seconds".format(error.retry_after),
            colour=discord.Colour.dark_red(),
            description=None
        )
        beg_too_fast.set_author(name=f"{ctx.author}'s command", icon_url=ctx.author.avatar_url)
        return await ctx.send(embed=beg_too_fast)
