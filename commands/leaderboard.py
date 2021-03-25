import discord
from discord.ext import commands

from bot import sql_client


@commands.command(aliases=["lb", "top"])
async def leaderboard(ctx, page: int = 1):
    await ctx.bot.wait_until_ready()
    total = sorted(sql_client.users)
    pages = len(total) // 10 + 1
    if page > pages:
        raise ValueError("Page is more than the max pages.")
    embed = discord.Embed(title="Leaderboard", colour=discord.Colour.green())
    embed.set_footer(text=f"Page {page} out of {pages}")
    for num, user in enumerate(total[(page - 1) * 10:page * 10], (page - 1) * 10 + 1):
        embed.add_field(name=f"#{num}", value=ctx.bot.get_user(user.id).mention + f": **{user.stock}** stocks, **{user.balance}** coins",
                        inline=False)
    await ctx.send(embed=embed)
