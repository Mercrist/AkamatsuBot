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
                             user_agent= config.agent)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(description=f"You're going too fast, slow down!", colour=discord.Color.gold())
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(5, 20, commands.BucketType.user) #can use this 4 times every 20 seconds per user
    async def sub(self, ctx, sub):
        '''Gets top hot posts from a specified subreddit. Displays four embeds at a time.'''
        sub = self.reddit.subreddit(sub)
        if sub.over18 and not ctx.channel.is_nsfw():
            embed = discord.Embed(description=f"Can't link NSFW subreddits in a non NSFW discord channel.", colour=discord.Color.gold())
            await ctx.send(embed=embed)
            raise TypeError
        reactions = {"left": "⬅️", "right": "➡️"}
        desc = f"🔥Currently displaying the hottest posts for /r/{sub}!"
        time = datetime.utcnow()
        color = discord.Color.dark_red()
        embed = discord.Embed(title = f"/r/{sub}", description = desc, url = f"https://www.reddit.com/r/{sub}", timestamp = time, colour = color)
        #subreddit fetching
        posts = sub.hot(limit=5)  #limit is the amount of requests we make/posts we're getting
        for post in posts:
            post_created = datetime.fromtimestamp(int(post.created_utc)).strftime('%m-%d-%Y at %H:%M:%S')
            embed.add_field(name = f":arrow_up: {post.score} upvotes! | Posted by /u/{post.author.name} on {post_created}", value = f"[{post.title}](https://www.reddit.com{post.permalink})", inline = False)
        embed.set_thumbnail(url = sub.icon_img)
        #emoji reaction events
        message = await ctx.send(embed = embed) #to be able to use reactions on the sent message
        await message.add_reaction(reactions["left"])
        await message.add_reaction(reactions["right"])

#ADD MESSAGES AND REACT EMOJIS TO SCROLL THROUGH SUB
def setup(bot):
    bot.add_cog(Reddit(bot))