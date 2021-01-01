from discord.ext import commands
import discord
import os
import logging
import config
logging.basicConfig(level=logging.INFO)
class AkaBot(commands.AutoShardedBot):
    def __init__(self):
        intents = discord.Intents.default()  #https://discordpy.readthedocs.io/en/latest/intents.html, needed for member specific events
        intents.members = True
        super().__init__(command_prefix = config.prefix, intents = intents) #uses the commands.Bot init and replaces self.bot with self
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
                print(f"Loading... cogs.{filename[:-3]}")
                self.load_extension(f"cogs.{filename[:-3]}")  #removes the .py from CogName.py

    #not using self for the bottom commands, it gets passed as a Context argument; using ctx.bot as self instead
    @commands.command()
    async def load(ctx, cogName): #ctx/context gets all kinds of stuff like the user that wrote it, the message contents, etc
        '''Loads a specified Cog.'''
        is_owner = await ctx.bot.is_owner(ctx.author) #prevents other users from loading or unloading the bot
        if is_owner:
            ctx.bot.load_extension(f"cogs.{cogName}") #loads the cog in /cogs/cogName.py
            embed = discord.Embed(description= f"{cogName} was loaded succesfully!", colour= discord.Color.dark_orange())
            await ctx.send(embed = embed)

    @commands.command()
    async def unload(ctx, cogName): #by using cogs, you dont have to turn the bot offline, simply unload the cogs with the command
        '''Unloads a specified Cog.'''
        is_owner = await ctx.bot.is_owner(ctx.author)
        if is_owner:
            ctx.bot.unload_extension(f"cogs.{cogName}")
            embed = discord.Embed(description=f"{cogName} was loaded succesfully!", colour=discord.Color.dark_orange())
            await ctx.send(embed=embed)

    @commands.command()
    async def reload(ctx, cogName):
        '''Reloads the bot automatically.'''
        is_owner = await ctx.bot.is_owner(ctx.author)
        if is_owner:
            ctx.bot.unload_extension(f"cogs.{cogName}")
            ctx.bot.load_extension(f"cogs.{cogName}")
            embed = discord.Embed(description=f"{cogName} was loaded succesfully!", colour=discord.Color.dark_orange())
            await ctx.send(embed=embed)

if __name__ == '__main__':
    bot = AkaBot()
    bot.run(config.token)