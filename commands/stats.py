import discord
from discord.ext import commands

from bot import sql_client


@commands.command()
async def stats(ctx):
    await ctx.bot.wait_until_ready()
    user = sql_client.get(ctx.author.id)

    wallet_amt = user.balance
    stock_amt = user.stock

    bal_embed = discord.Embed(
        title=f"{ctx.author.name}'s balance",
        colour=discord.Colour.dark_red()
    )
    bal_embed.add_field(name="__" + "Coins" + "__", value=wallet_amt)
    bal_embed.add_field(name="__" + "Stock Owned" + "__", value=stock_amt, inline=False)
    await ctx.send(embed=bal_embed)

def setup(bot):
    bot.add_command(stats)
