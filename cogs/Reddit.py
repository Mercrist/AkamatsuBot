from datetime import datetime
from discord.ext import commands
import config #parent directory is a module so we can import from it (https://stackoverflow.com/questions/8951255/import-script-from-a-parent-directory/8951269)
import praw
import discord
import urllib.request, json
class Reddit(commands.Cog):
    '''When the bot first joins the server.'''
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id = config.ID,
                             client_secret = config.secret,
                             username = config.username,
                             password = config.passwd,
                             user_agent= config.agent)

    @commands.command(pass_context = True)
    @commands.cooldown(5, 30, commands.BucketType.user) #can use this 4 times every thirty seconds per user
    async def sub(self, ctx, sub):
        '''Gets top hot posts from a specified subreddit. Displays four embeds at a time.'''
        desc = f"🔥Currently displaying the top five hottest posts for r/{sub}!"
        time = datetime.utcnow()
        color = discord.Color.dark_red()
        embed = discord.Embed(title = f"/r/{sub}", description = desc, url = f"https://www.reddit.com/r/{sub}", timestamp = time, colour = color)
        #subreddit fetching
        sub = self.reddit.subreddit(sub)
        posts = sub.hot(limit=5)  #limit is the amount of requests we make
        embed.set_thumbnail(url = sub.icon_img)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Reddit(bot))