from discord.ext import commands
from datetime import datetime
from random import randint
import discord
import urllib.request
import json
import praw, config
class Animals(commands.Cog):
    '''List of commands which display images for certain animals.'''
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id=config.ID,
                             client_secret=config.secret,
                             user_agent=config.agent)

    @commands.command()
    @commands.cooldown(10, 15, commands.BucketType.user)
    async def dog(self, ctx):
        '''Fetches a random image of a dog.'''
        with urllib.request.urlopen("https://api.thedogapi.com/v1/images/search?size=med&mime_types=jpg&format=json&has_breeds=true&order=RANDOM&page=0&limit=1") as url:  # gets random cat breed ID
            data = json.loads(url.read().decode())

        dogName = data[0].get("breeds")[0].get("name") #json is a list, 0th index of breeds section contains the name of the dog
        url = data[0].get("url")

        embed = discord.Embed(title = dogName, timestamp = datetime.utcnow(), colour = discord.Color.light_grey())
        embed.set_image(url = url)
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(10, 15, commands.BucketType.user)
    async def cat(self, ctx):
        '''Fetches a random image of a cat.'''
        with urllib.request.urlopen("https://api.thecatapi.com/v1/breeds/") as url: #gets random cat breed ID
            data = json.loads(url.read().decode())
        catID = data[randint(0, len(data)-1)]['id']

        with urllib.request.urlopen(f"https://api.thecatapi.com/v1/images/search?breed_ids={catID}&include_breeds=true") as url:
            data = json.loads(url.read().decode())

        catName = data[0].get("breeds")[0].get("name")
        url = data[0].get("url")

        embed = discord.Embed(title=catName, timestamp=datetime.utcnow(), colour=discord.Color.from_rgb(255,192,203))
        embed.set_image(url = url)
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(10, 15, commands.BucketType.user)
    async def buns(self, ctx):
        '''Fetches a random image of a rabbit/bunny.'''
        sub = self.reddit.subreddit("rabbits")
        postTypes = [sub.hot(limit=20), sub.new(limit = 20), sub.top("year", limit = 20)] #makes repeated images less frequent
        submissions = [posts for posts in postTypes[randint(0,2)]]
        submission = submissions[randint(0, 19)]
        while submission.domain != 'i.redd.it':
            submission = submissions[randint(0, 19)]

        embed = discord.Embed(title= "Lootbox Bun!", timestamp=datetime.utcnow(), colour=discord.Color.dark_orange())
        embed.set_image(url=submission.url)
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(10, 15, commands.BucketType.user)
    async def otters(self, ctx):
        '''Fetches a random image of an otter.'''
        pass

    @commands.command()
    @commands.cooldown(10, 15, commands.BucketType.user)
    async def ferret(self, ctx):
        '''Fetches a random image of a ferret.'''
        pass

    @commands.command()
    @commands.cooldown(10, 15, commands.BucketType.user)
    async def redpanda(self, ctx):
        '''Fetches a random image of a red panda.'''
        pass

    @commands.command()
    @commands.cooldown(10, 15, commands.BucketType.user)
    async def panda(self, ctx):
        '''Fetches a random image of a panda.'''
        pass

    @commands.command()
    @commands.cooldown(10, 15, commands.BucketType.user)
    async def fox(self, ctx):
        '''Fetches a random image of a fox.'''
        pass

def setup(bot):
    bot.add_cog(Animals(bot))