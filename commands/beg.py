import random

import discord
from discord.ext import commands

from bot import sql_client


@commands.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def beg(ctx):
    await ctx.bot.wait_until_ready()
    user = sql_client.get(ctx.author.id)

    coins_recieved = random.randint(15, 61)

    people_beg_list = [
        'John Cena',
        'Barack Obama',
        'George Bush',
        'Joe Mama',
        "Mr. Clark"]
    user.balance += coins_recieved
    coins_begged_embed = discord.Embed(
        title="You begged and " + random.choice(people_beg_list) + " gave you %s coins!" % coins_recieved,
        colour=discord.Colour.red()
    )
    coins_begged_embed.set_author(name=f"{ctx.author}'s command", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=coins_begged_embed)


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
    else:
        raise

def setup(bot):
    bot.add_command(beg)
