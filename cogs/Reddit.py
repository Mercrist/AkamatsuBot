from discord.ext import commands
import config #parent directory is a module so we can import from it (https://stackoverflow.com/questions/8951255/import-script-from-a-parent-directory/8951269)
import praw
import discord
class Reddit(commands.Cog):
    '''When the bot first joins the server.'''
    def __init__(self, bot):
        self.bot = bot
        reddit = praw.Reddit(client_id=config.ID,
                             client_secret=config.secret,
                             user_agent=config.agent,) #read only bot
def setup(bot):
    bot.add_cog(Reddit(bot))