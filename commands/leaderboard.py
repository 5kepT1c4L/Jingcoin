import discord
from discord.ext import commands

from bot import sql_client


class PageOverflowException(commands.CommandError, OverflowError, ValueError):

    def __init__(self, page: int, max_pages: int):
        super().__init__("The page requested is more than the maximum amount of pages.")
        self.page = page
        self.max = max_pages


@commands.command(aliases=["lb", "top"])
async def leaderboard(ctx, page: int = 1):
    await ctx.bot.wait_until_ready()
    total = sorted(sql_client.users)
    pages = len(total) // 10 + 1
    if page > pages:
        raise PageOverflowException(page, pages)
    embed = discord.Embed(title="Leaderboard", colour=discord.Colour.green())
    embed.set_footer(text=f"Page {page} out of {pages}")
    for num, user in enumerate(total[(page - 1) * 10:page * 10], (page - 1) * 10 + 1):
        embed.add_field(name=f"#{num}", value=ctx.bot.get_user(user.id).mention + f": **{user.stock}** stocks, **{user.balance}** coins",
                        inline=False)
    await ctx.send(embed=embed)


@leaderboard.error
async def on_leaderboard_error(ctx, error):
    if isinstance(error, PageOverflowException):
        embed = discord.Embed(title="Page Overflow", description=error.args[0])
        embed.add_field(name="Max Pages", value=str(error.max)).add_field(name="Page Requested", value=str(error.page))
        return await ctx.send(embed=embed)
