import discord

from utils import get_bank_data, open_account
from ..bot import client


@client.command()
async def stats(ctx):
    await open_account(ctx.author)

    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["Coins"]
    jingcoin_amt = users[str(user.id)]["Jingcoins"]

    bal_embed = discord.Embed(
        title=f"{ctx.author.name}'s balance",
        colour=discord.Colour.dark_red()
    )
    bal_embed.add_field(name="__" + "Coins" + "__", value=wallet_amt)
    bal_embed.add_field(name="__" + "Jingcoins" + "__", value=jingcoin_amt, inline=False)
    await ctx.send(embed=bal_embed)
