import discord

from bot import client, sql_client


@client.command()
async def stats(ctx):
    await client.wait_until_ready()
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
