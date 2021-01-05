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
        super().__init__(command_prefix = config.prefix, intents = intents) #uses the commands.AuotoShardedBot init and replaces self.bot with self
        self.load_cogs()

    async def on_ready(self):
        print("Bot's online!")

    def load_cogs(self):
        '''Loads all available cogs in the cogs directory.'''
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                print(f"Loading... cogs.{filename[:-3]}")
                self.load_extension(f"cogs.{filename[:-3]}")  #removes the .py from CogName.py

if __name__ == '__main__':
    bot = AkaBot()
    bot.run(config.token)