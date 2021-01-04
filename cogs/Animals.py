from discord.ext import commands
from datetime import datetime
from random import randint
from bs4 import BeautifulSoup
import discord
import aiohttp #https://discordpy.readthedocs.io/en/latest/faq.html#what-does-blocking-mean
import asyncpraw, config
class Animals(commands.Cog):
    '''List of commands which display images for certain animals.'''
    def __init__(self, bot):
        self.bot = bot
        self.http_session = aiohttp.ClientSession()
        self.reddit = asyncpraw.Reddit(client_id=config.ID,
                             client_secret=config.secret,
                             user_agent=config.agent)

    @commands.command()
    @commands.cooldown(5, 15, commands.BucketType.user)
    async def dog(self, ctx):
        '''Fetches a random image of a dog.'''
        async with self.http_session.get('https://api.thedogapi.com/v1/images/search?size=med&mime_types=jpg&format=json&has_breeds=true&order=RANDOM&page=0&limit=1') as url:
            if url.status == 200:
                js = await url.json()
                dogName = js[0].get("breeds")[0].get("name") #json is a list, 0th index of breeds section contains the name of the dog
                url = js[0].get("url")

        embed = discord.Embed(title = dogName, timestamp = datetime.utcnow(), colour = discord.Color.light_grey())
        embed.set_image(url = url)
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(5, 15, commands.BucketType.user)
    async def cat(self, ctx):
        '''Fetches a random image of a cat.'''
        async with self.http_session.get('https://api.thecatapi.com/v1/breeds/') as url: #gets random cat breed ID
            if url.status == 200:
                js = await url.json()
                catID = js[randint(0, len(js)-1)]['id']

        async with self.http_session.get(f"https://api.thecatapi.com/v1/images/search?breed_ids={catID}&include_breeds=true") as url: #gets random cat breed ID
            if url.status == 200:
                js = await url.json()
                catName = js[0].get("breeds")[0].get("name")
                url = js[0].get("url")

        embed = discord.Embed(title=catName, timestamp=datetime.utcnow(), colour=discord.Color.from_rgb(255,192,203))
        embed.set_image(url = url)
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(5, 15, commands.BucketType.user)
    async def buns(self, ctx):
        '''Fetches a random image of a rabbit/bunny.'''
        sub = await self.reddit.subreddit("rabbits")
        postTypes = [sub.hot(limit=65), sub.new(limit = 65), sub.top("year", limit = 65)] #65 requests makes repeated images less frequent but not as slow as 100
        submissions = []
        async for posts in postTypes[randint(0,2)]:
            submissions.append(posts)
        submission = submissions[randint(0, 64)]
        while submission.domain != 'i.redd.it':
            submission = submissions[randint(0, 64)]

        embed = discord.Embed(title= "Lootbox Bun!", timestamp=datetime.utcnow(), colour=discord.Color.from_rgb(128,0,0))
        embed.set_image(url=submission.url)
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(5, 15, commands.BucketType.user)
    async def otters(self, ctx):
        '''Fetches a random image of an otter.'''
        sub = await self.reddit.subreddit("otters")
        postTypes = [sub.hot(limit= 65), sub.new(limit=65), sub.top("year", limit=65)]
        submissions = []
        async for posts in postTypes[randint(0, 2)]:
            submissions.append(posts)
        submission = submissions[randint(0, 64)]
        while submission.domain != 'i.redd.it':
            submission = submissions[randint(0, 64)]

        embed = discord.Embed(title="Lootbox Otter!", timestamp=datetime.utcnow(), colour=discord.Color.from_rgb(139,69,19))
        embed.set_image(url=submission.url)
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(5, 15, commands.BucketType.user)
    async def ferret(self, ctx):
        '''Fetches a random image of a ferret.'''
        sub = await self.reddit.subreddit("ferrets")
        postTypes = [sub.hot(limit=65), sub.new(limit=65), sub.top("year", limit=65)]
        submissions = []
        async for posts in postTypes[randint(0,2)]:
            submissions.append(posts)
        submission = submissions[randint(0, 64)]
        while submission.domain != 'i.redd.it':
            submission = submissions[randint(0, 64)]

        embed = discord.Embed(title="Lootbox Ferret!", timestamp=datetime.utcnow(), colour=discord.Color.from_rgb(222,184,135))
        embed.set_image(url=submission.url)
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(5, 15, commands.BucketType.user)
    async def panda(self, ctx):
        '''Fetches a random image of a panda.'''
        sub = await self.reddit.subreddit("panda")
        postTypes = [sub.hot(limit=65), sub.new(limit=65), sub.top("year", limit=65)]
        submissions = []
        async for posts in postTypes[randint(0, 2)]:
            submissions.append(posts)
        submission = submissions[randint(0, 64)]
        while submission.domain != 'i.redd.it':
            submission = submissions[randint(0, 64)]

        embed = discord.Embed(title="Lootbox Panda!", timestamp=datetime.utcnow(), colour=discord.Color.from_rgb(255,255,255))
        embed.set_image(url=submission.url)
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(5, 15, commands.BucketType.user)
    async def fox(self, ctx):
        '''Fetches a random image of a fox.'''
        async with self.http_session.get("https://randomfox.ca/floof/") as url: #HTTP Error 403: Forbidden with urrlib.request
            if url.status == 200:
                js = await url.json()

        embed = discord.Embed(title="Lootbox Fox!", timestamp=datetime.utcnow(), colour=discord.Color.from_rgb(255, 69,0))
        embed.set_image(url = js["image"])
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(5, 15, commands.BucketType.user)
    async def hamster(self, ctx):
        '''Fetches a random image of a hamster.'''
        sub = await self.reddit.subreddit("hamsters")
        postTypes = [sub.hot(limit=65), sub.new(limit=65), sub.top("year", limit=65)]
        submissions = []
        async for posts in postTypes[randint(0, 2)]:
            submissions.append(posts)
        submission = submissions[randint(0, 64)]
        while submission.domain != 'i.redd.it':
            submission = submissions[randint(0, 64)]

        embed = discord.Embed(title="Lootbox Hamster!", timestamp=datetime.utcnow(), colour=discord.Color.gold())
        embed.set_image(url=submission.url)
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def quokka(self, ctx):
        '''Fetches a random image of a quokka.'''
        picUrls = []
        for i in range(5):
            async with self.http_session.get(f"https://www.gettyimages.com/photos/quokka?page={i+1}&phrase=quokka&sort=mostpopular") as url:
                if url.status == 200:
                    get_soup = await url.text()
                    soup = BeautifulSoup(get_soup, "lxml")
                    pics = soup.findAll("img", {"class": "gallery-asset__thumb gallery-mosaic-asset__thumb"})
                    for tags in range(len(pics)):
                        pics[tags] = pics[tags].get("src")
                        picUrls.extend(pics)

        embed = discord.Embed(title="Lootbox Quokka!", timestamp=datetime.utcnow(), colour=discord.Color.from_rgb(153, 101, 21))
        embed.set_image(url=picUrls[randint(0, len(picUrls)-1)])
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Animals(bot))