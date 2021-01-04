from discord.ext import commands
import discord
class Admin(commands.Cog):
    '''Commands and events to be used or triggered for administrative purposes.'''
    def __init__(self, bot):
        self.bot = bot