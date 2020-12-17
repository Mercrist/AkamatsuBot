from config import token, prefix
from discord.ext import commands
import discord
import asyncio
import os

bot = commands.Bot(command_prefix = prefix)

@bot.command()
async def load(ctx, cogName):
    '''Loads a cog onto the bot.'''
    bot.load_extension(f"cogs.{cogName}") #loads the cog in /cogs/cogName.py
    print(f"{cogName} was loaded succesfully!")

@bot.command()
async def unload(ctx, cogName):
    bot.unload_extension(f"cogs.{cogName}")
    print(f"{cogName} was loaded succesfully!")

if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f"cogs.{filename[:-3]}") #removes the .py from CogName.py
    bot.run(token)