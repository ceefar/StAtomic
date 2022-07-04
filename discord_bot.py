import discord
from discord.ext import commands


bot = commands.Bot(command_prefix="!", description="The description")

@bot.event
async def  on_ready():
    print("Ready !")

@bot.command()
async def ping(ctx):
    await ctx.send('**pong**')

bot.run("OTcyODEzNDc3ODg4NTM2NTc2.G957k9.AMPi4JjyhFKzA5FRu9vEti0IDdPcM3UK0A9fJ4")
