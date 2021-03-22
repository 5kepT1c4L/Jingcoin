import discord
import os
import json
from discord.ext import commands
import random
from login import token

os.chdir(r"C:\Users\jinge\OneDrive\Desktop\Coding\Discord Bot\Jingcoin")

client = commands.Bot(command_prefix = ',')
client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('To the MOOOOOON!!'))
    print("Bot is up and running baby!")


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
    bal_embed.add_field(name="__" + "Jingcoins" + "__", value=jingcoin_amt,inline=False)
    await ctx.send(embed=bal_embed)




async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["Coins"] = 0
        users[str(user.id)]["Jingcoins"] = 0

    with open("jingcoin.json", "w") as f:
        json.dump(users, f)
    return True

async def get_bank_data():
    with open("jingcoin.json", "r") as f:
        users = json.load(f)
    return users



@client.command()
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
    title= "You begged and " + random.choice(people_beg_list) + " gave you %s coins!" % (coins_recieved),
    colour = discord.Colour.red(),
    description=None
    )
    coins_begged_embed.set_author(name=f"{ctx.author}'s command", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=coins_begged_embed)
    with open("jingcoin.json", "w") as f:
        json.dump(users, f)
    return True



@client.command()
async def rob(ctx, member:discord.Member):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    chances_of_robbed = random.randint(1,21)
    if chances_of_robbed <= 9 and users[str(member.id)]["Coins"] >= 500:
        amt_robbed = random.randint(300, users[str(member.id)]["Coins"])
        users[str(user.id)]["Coins"] += amt_robbed
        users[str(member.id)]["Coins"] -= amt_robbed

        robbed_embed = discord.Embed(
            title=f"NICE! You managed to rob %s coins from {member}!" % (amt_robbed),
            colour=discord.Colour.green(),
            description=None
        )
        robbed_embed.set_author(name=f"{ctx.author}'s command", icon_url=ctx.author.avatar_url)
        robbed_embed.set_image(url="https://cdn.discordapp.com/attachments/822980593137614918/823565142297411584/Armed-Robbery-Charge.png")
        await ctx.send(embed=robbed_embed)
        with open("jingcoin.json", "w") as f:
            json.dump(users, f)
        return True

    elif chances_of_robbed > 9 and users[str(member.id)]["Coins"] >= 500:












client.run(token)
