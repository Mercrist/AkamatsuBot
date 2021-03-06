from datetime import datetime
from discord.ext import commands
from disputils import BotEmbedPaginator
from random import randint
from urllib.parse import urlparse
import os
import config #parent directory is a module so we can import from it (https://stackoverflow.com/questions/8951255/import-script-from-a-parent-directory/8951269)
import praw #asyncpraw doesnt support some attributes like .over18
import discord
class Reddit(commands.Cog):
    '''List of commands which fetch posts from specific subreddits.'''
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id = config.ID,
                             client_secret = config.secret,
                             user_agent= config.agent)
    @commands.command()
    @commands.cooldown(3, 15, commands.BucketType.user) #can use this 3 times every 15 seconds per user
    async def sub(self, ctx, sub):
        '''Gets top hot posts from a specified subreddit. Displays five embeds at a time.'''
        sub = self.reddit.subreddit(sub)
        if sub.over18 and not ctx.channel.is_nsfw():
            embed = discord.Embed(description=f"Can't link NSFW subreddits in a non NSFW discord channel.", colour=discord.Color.gold())
            await ctx.send(embed=embed)
            return

        desc = f"🔥 Currently displaying the hottest posts for /r/{sub}!"
        time = datetime.utcnow()
        color = discord.Color.dark_red()
        embeds = []
        posts = sub.hot(limit=15)  #limit is the amount of requests we make/posts we're getting, page*number is the amt we want to request
        postList = [items for items in posts]
        if sub.community_icon != "":
            icon = sub.community_icon
        elif sub.icon_img != "":
            icon = sub.icon_img
        else:
            icon = "https://logodownload.org/wp-content/uploads/2018/02/reddit-logo-16.png"

        for i in range(3): #3 pages
            embed = discord.Embed(title = f"/r/{sub}", description = desc, url = f"https://www.reddit.com/r/{sub}", timestamp = time, colour = color)
            #subreddit fetching
            for post in postList[:5]:
                post_created = datetime.fromtimestamp(int(post.created_utc)).strftime('%m-%d-%Y at %H:%M:%S')
                embed.add_field(name = f":arrow_up: {post.score} upvotes and {post.num_comments} comments! | Posted by /u/{post.author.name} on {post_created} UTC", value = f"[{post.title}](https://www.reddit.com{post.permalink})", inline = False)
                embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
                embed.set_thumbnail(url= icon)
            del postList[:5]  #removes first 5 elements since these have been added to the field already
            embeds.append(embed)

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()

    @commands.command()
    @commands.cooldown(3, 15, commands.BucketType.user)
    async def subpost(self, ctx, sub):
        '''Gets a random hot post from a subreddit.'''
        sub = self.reddit.subreddit(sub)
        if sub.over18 and not ctx.channel.is_nsfw():
            embed = discord.Embed(description=f"Can't link NSFW subreddits in a non NSFW discord channel.", colour=discord.Color.gold())
            await ctx.send(embed=embed)
            return

        submissions = [posts for posts in sub.hot(limit=30)]
        submission = submissions[randint(0, 29)]
        if sub.community_icon != "":
            thumbnail = sub.community_icon
        elif sub.icon_img != "":
            thumbnail = sub.icon_img
        else:
            thumbnail = "https://logodownload.org/wp-content/uploads/2018/02/reddit-logo-16.png"

        valids = [".png", ".jpg", ".jpeg", ".gif"]
        path = urlparse(submission.url).path
        ext = os.path.splitext(path)[1]

        if ext in valids: #image post
            embed = discord.Embed(title=f"/u/{submission.author.name}", description=f"[{submission.title}](https://www.reddit.com{submission.permalink})",
                                  url=f"https://www.reddit.com/user/{submission.author.name}",
                                  timestamp=datetime.utcnow(), colour=discord.Color.dark_red())

            if submission.over_18 and not ctx.channel.is_nsfw():
                embed.add_field(name="Post Content:", value=f"[Image submission is NSFW, click here to access the thread.](https://www.reddit.com{submission.permalink})", inline=False)
                embed.set_thumbnail(url="https://external-preview.redd.it/aCO4aR1tWeeF_KiMIPzzxYZ3O6Uq8l-5gZ2e14z80kQ.png?auto=webp&s=cad678498dc98098484a09dbc2df1fb9cc528cf0")
            else:
                embed.set_image(url= submission.url)

        elif submission.domain == 'v.redd.it': #video post
            embed = discord.Embed(title=f"/u/{submission.author.name}", description=f"**{submission.title}**",
                                  url=f"https://www.reddit.com/user/{submission.author.name}",
                                  timestamp=datetime.utcnow(), colour=discord.Color.dark_red())

            if submission.over_18 and not ctx.channel.is_nsfw():
                embed.add_field(name="Post Content:", value=f"[Video submission is NSFW, click here to access the thread.](https://www.reddit.com{submission.permalink})", inline=False)
                embed.set_thumbnail(url="https://external-preview.redd.it/aCO4aR1tWeeF_KiMIPzzxYZ3O6Uq8l-5gZ2e14z80kQ.png?auto=webp&s=cad678498dc98098484a09dbc2df1fb9cc528cf0")

            else:
                embed.set_thumbnail(url = submission.preview['images'][0]['source']['url'])
                embed.add_field(name="Post Content:", value=f"[Submission is a video, click here to access the thread.](https://www.reddit.com{submission.permalink})", inline=False)

        elif submission.is_self:  #is a text post
            embed = discord.Embed(title=f"/u/{submission.author.name}", description=f"**{submission.title}**",
                                  url=f"https://www.reddit.com/user/{submission.author.name}",
                                  timestamp=datetime.utcnow(), colour=discord.Color.dark_red())

            if submission.thumbnail == "nsfw" or (submission.over_18 and not ctx.channel.is_nsfw()):
                thumbnail = "https://external-preview.redd.it/aCO4aR1tWeeF_KiMIPzzxYZ3O6Uq8l-5gZ2e14z80kQ.png?auto=webp&s=cad678498dc98098484a09dbc2df1fb9cc528cf0"
            embed.set_thumbnail(url=thumbnail)

            text = submission.selftext
            if text == "":
                text = "Post content is empty, click here to access the thread!" #so that threads like the ones on AskReddit can click on text to be redirected
            #check for embed max text field length
            elif len(text) > 850:  #bottom calculation is amount of characters it went over by
                text = text[:850 - len(text)] + "..."
            embed.add_field(name="Post content:", value=f"[{text}](https://www.reddit.com{submission.permalink})", inline=False)

        else: #submission is just a link from a third party website
            embed = discord.Embed(title=f"/u/{submission.author.name}", description=f"**{submission.title}**", url=f"https://www.reddit.com/user/{submission.author.name}", timestamp=datetime.utcnow(), colour=discord.Color.dark_red())
            embed.add_field(name="Post content:", value=f"[{submission.url}](https://www.reddit.com{submission.permalink})", inline=False)

            if submission.thumbnail == "nsfw":
                thumbnail = "https://external-preview.redd.it/aCO4aR1tWeeF_KiMIPzzxYZ3O6Uq8l-5gZ2e14z80kQ.png?auto=webp&s=cad678498dc98098484a09dbc2df1fb9cc528cf0"
            embed.set_thumbnail(url=thumbnail)

        embed.set_footer(text=f"Requested by {ctx.message.author} | 👍{submission.score} 💬{submission.num_comments}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.cooldown(5, 15, commands.BucketType.user)
    @commands.command()
    async def meme(self, ctx):
        '''Posts a random meme from a random meme subreddit'''
        subs = ["memes", "dankmemes", "greentext", "me_irl", "historymemes", "wholesomememes"]
        sub = self.reddit.subreddit(subs[randint(0,5)])
        submissions = [posts for posts in sub.hot(limit=30)]
        submission = submissions[randint(0, 29)]
        while submission.domain != 'i.redd.it' and submission.author.is_mod: #dont want mod posts
            submission = submissions[randint(0, 29)]

        embed = discord.Embed(title=f"/u/{submission.author.name}",
                                  description=f"[{submission.title}](https://www.reddit.com{submission.permalink})",
                                  url=f"https://www.reddit.com/user/{submission.author.name}",
                                  timestamp=datetime.utcnow(), colour=discord.Color.green())
        embed.set_image(url=submission.url)
        embed.set_footer(text=f"Requested by {ctx.message.author} | 👍{submission.score} 💬{submission.num_comments}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Reddit(bot))