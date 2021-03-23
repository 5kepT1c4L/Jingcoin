import random

import discord
from discord.ext import commands

from bot import client, sql_client


@client.command()
async def rob(ctx, member: discord.Member):
    await client.wait_until_ready()
    user_robbing = sql_client.get(ctx.author.id)
    user_robbed = sql_client.get(member.id)

    chances_of_robbed = random.randint(1, 21)
    if chances_of_robbed <= 9 and user_robbed.balance >= 500:
        amt_robbed = random.randint(300, user_robbed.balance)
        user_robbing.balance += amt_robbed
        user_robbed.balance -= amt_robbed

        robbed_embed = discord.Embed(
            title=f"NICE! You managed to rob %s coins from {member}!" % (amt_robbed),
            colour=discord.Colour.green(),
            description=None
        )
        robbed_embed.set_author(name=f"{ctx.author}'s command", icon_url=ctx.author.avatar_url)
        robbed_embed.set_image(url="https://cdn.discordapp.com/attachments/822980593137614918/823565142297411584/Armed-Robbery-Charge.png")
        await ctx.send(embed=robbed_embed)

    if chances_of_robbed > 9 and user_robbed.balance >= 500:
        failed_rob_embed = discord.Embed(
            title=f"You failed to rob {member} and had to pay 300 coins!",
            colour=discord.Colour.red()
        )
        failed_rob_embed.set_author(name=f"{ctx.author}'s command", icon_url=ctx.author.avatar_url)
        failed_rob_embed.set_image(url="https://cdn.discordapp.com/attachments/749087782890373194/823603794247942184/notforme.PNG")
        user_robbed.balance += 300
        user_robbing.balance -= 300
        await ctx.send(embed=failed_rob_embed)

    if user_robbed.balance < 500:
        victim_poor_embed = discord.Embed(
            title="Aye no robbing from the unfortunate!",
            colour=discord.Colour.teal()
        )
        victim_poor_embed.set_author(name=f"{ctx.author}'s command", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=victim_poor_embed)


@rob.error
async def on_rob_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        rob_too_fast = discord.Embed(
            title="Woah woah, chill with the constant robbing! You can rob again in {:.2f} seconds".format(error.retry_after),
            colour=discord.Colour.magenta()
        )
        rob_too_fast.set_author(name=f"{ctx.author}'s command", icon_url=ctx.author.avatar_url)

        return await ctx.send(embed=rob_too_fast)
