from datetime import datetime
from discord.ext import commands
from disputils import BotEmbedPaginator
from random import randint
import config #parent directory is a module so we can import from it (https://stackoverflow.com/questions/8951255/import-script-from-a-parent-directory/8951269)
import praw
import discord
class Reddit(commands.Cog):
    '''List of commands which fetch posts from specific subreddits.'''
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
    @commands.cooldown(5, 10, commands.BucketType.user) #can use this 5 times every 10 seconds per user
    async def sub(self, ctx, sub):
        '''Gets top hot posts from a specified subreddit. Displays five embeds at a time.'''
        sub = self.reddit.subreddit(sub)
        if sub.over18 and not ctx.channel.is_nsfw():
            embed = discord.Embed(description=f"Can't link NSFW subreddits in a non NSFW discord channel.", colour=discord.Color.gold())
            await ctx.send(embed=embed)
            raise TypeError

        desc = f"🔥 Currently displaying the hottest posts for /r/{sub}!"
        time = datetime.utcnow()
        color = discord.Color.dark_red()
        embeds = []
        posts = sub.hot(limit=15)  #limit is the amount of requests we make/posts we're getting, page*number is the amt we want to request
        postList = [items for items in posts]
        if sub.community_icon != "":
            icon = sub.community_icon
        else:
            icon = sub.icon_img

        for i in range(3): #3 pages
            embed = discord.Embed(title = f"/r/{sub}", description = desc, url = f"https://www.reddit.com/r/{sub}", timestamp = time, colour = color)
            #subreddit fetching
            for post in postList[:5]:
                post_created = datetime.fromtimestamp(int(post.created_utc)).strftime('%m-%d-%Y at %H:%M:%S')
                embed.add_field(name = f":arrow_up: {post.score} upvotes and {post.num_comments} comments! | Posted by /u/{post.author.name} on {post_created} UTC", value = f"[{post.title}](https://www.reddit.com{post.permalink})", inline = False)
                embed.set_footer(text=f"Requested by {ctx.message.author}. Viewing page {i+1} out of 3.", icon_url=ctx.message.author.avatar_url)
                embed.set_thumbnail(url= icon)
            del postList[:5]  #removes first 5 elements since these have been added to the field already
            embeds.append(embed)

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()

    @commands.command()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def subpost(self, ctx, sub):
        '''Gets a random hot post from a subreddit.'''
        sub = self.reddit.subreddit(sub)
        if sub.over18 and not ctx.channel.is_nsfw():
            embed = discord.Embed(description=f"Can't link NSFW subreddits in a non NSFW discord channel.", colour=discord.Color.gold())
            await ctx.send(embed=embed)
            raise TypeError

        submissions = [posts for posts in sub.hot(limit=20)]
        submission = submissions[randint(0, 19)]

        if submission.thumbnail == "nsfw":
            thumbnail = "https://external-preview.redd.it/aCO4aR1tWeeF_KiMIPzzxYZ3O6Uq8l-5gZ2e14z80kQ.png?auto=webp&s=cad678498dc98098484a09dbc2df1fb9cc528cf0"
        elif submission.thumbnail == "" or submission.thumbnail.isalpha(): #sometimes the thumbnail is "self" or "default"
            thumbnail = "https://logodownload.org/wp-content/uploads/2018/02/reddit-logo-16.png"
        else:
            thumbnail = submission.thumbnail

        embed = discord.Embed(title=f"/u/{submission.author.name}", description=f"**{submission.title}**", url=f"https://www.reddit.com/user/{submission.author.name}", timestamp=datetime.utcnow(), colour=discord.Color.dark_red())
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        embed.set_thumbnail(url= thumbnail)

        if submission.is_self:  #is a text post
            text = submission.selftext
            if text == "":
                text = "Post content is empty, click here to access the thread!" #so that threads like the ones on AskReddit can click on text to be redirected
            #check for embed max text field length
            elif len(text) > 850:  #bottom calculation is amount of characters it went over by
                text = text[:850 - len(text)] + "..."
            embed.add_field(name="Post content:",
                            value=f"[{text}](https://www.reddit.com{submission.permalink})\n:arrow_up: **{submission.score} upvotes and {submission.num_comments} comments!**",
                            inline=False)

        else: #images, links, or videos
            embed.add_field(name="Post content:",
                            value=f"[{submission.url}](https://www.reddit.com{submission.permalink})\n:arrow_up: **{submission.score} upvotes and {submission.num_comments} comments!**",
                            inline=False)
        #embed.add_field(name= f":arrow_up: {submission.score} upvotes and {submission.num_comments} comments!", value= None ,inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Reddit(bot))