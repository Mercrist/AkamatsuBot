from config import token, prefix
from discord.ext import commands
import discord
import asyncio
import os
class AkaBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = prefix) #uses the commands.Bot init and replaces self.bot with self

    def load_cogs(self):
        '''Loads all available cogs in the cogs directory.'''
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.load_extension(f"cogs.{filename[:-3]}")  #removes the .py from CogName.py

    @commands.command()
    async def load(self, ctx, cogName): #ctx/context is required for commands
        '''Loads all available cogs in the cogs directory.'''
        self.load_extension(f"cogs.{cogName}") #loads the cog in /cogs/cogName.py
        print(f"{cogName} was loaded succesfully!")

    @commands.command()
    async def unload(self, ctx, cogName):
        '''Unloads all available cogs in the cogs directory.'''
        self.unload_extension(f"cogs.{cogName}")
        print(f"{cogName} was unloaded succesfully!")

if __name__ == '__main__':
    bot = AkaBot()
    bot.load_cogs()
    bot.run(token)