from config import token, prefix
from discord.ext import commands
import discord
import asyncio
import os
class AkaBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = prefix) #uses the commands.Bot init and replaces self.bot with self
        self.load_cogs()
        self.add_command(self.load) #to be able to make load and unload commands without putting those in a Cog
        self.add_command(self.unload) #an easier way would be to declare these with @bot.event outside of the Class
        self.add_command(self.reload)

    async def on_ready(self): #https://i.imgur.com/pSnob7p.png
        print("Bot's online!")

    def load_cogs(self):
        '''Loads all available cogs in the cogs directory.'''
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.load_extension(f"cogs.{filename[:-3]}")  #removes the .py from CogName.py

    #not using self for the bottom commands, it gets passed as a Context argument; using ctx.bot as self instead
    @commands.command()
    async def load(ctx, cogName): #ctx/context gets all kinds of stuff like the user that wrote it, the message contents, etc
        '''Loads a specified Cog.'''
        is_owner = await ctx.bot.is_owner(ctx.author) #prevents other users from loading or unloading the bot
        if is_owner:
            ctx.bot.load_extension(f"cogs.{cogName}") #loads the cog in /cogs/cogName.py
            await ctx.send(f"{cogName} was loaded succesfully!")

    @commands.command()
    async def unload(ctx, cogName): #by using cogs, you dont have to turn the bot offline, simply unload the cogs with the command
        '''Unloads a specified Cog.'''
        is_owner = await ctx.bot.is_owner(ctx.author)
        if is_owner:
            ctx.bot.unload_extension(f"cogs.{cogName}")
            await ctx.send(f"{cogName} was unloaded succesfully!")

    @commands.command()
    async def reload(ctx, cogName):
        '''Reloads the bot automatically.'''
        is_owner = await ctx.bot.is_owner(ctx.author)
        if is_owner:
            ctx.bot.unload_extension(f"cogs.{cogName}")
            ctx.bot.load_extension(f"cogs.{cogName}")
            await ctx.send(f"{cogName} was reloaded succesfully!")

if __name__ == '__main__':
    bot = AkaBot()
    bot.run(token)