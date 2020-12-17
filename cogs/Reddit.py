from discord.ext import commands
class Reddit(commands.Cog):
    '''When the bot first joins the server.'''
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Reddit(bot))
