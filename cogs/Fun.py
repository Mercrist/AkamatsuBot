from discord.ext import commands
from datetime import datetime
import discord
class Fun(commands.Cog):
    '''Fun/Game type commands.'''
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def dadbot(self, message):
        '''Replies to a user whenever "I'm" or "I am" is used.'''
        print(message)


def setup(bot):
    bot.add_cog(Fun(bot))