from discord.ext import commands
from datetime import datetime
import discord
import urllib.request
import json
class Animals(commands.Cog):
    '''List of commands which display images for certain animals.'''
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(description=f"You're going too fast, slow down!", colour=discord.Color.gold())
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(10, 15, commands.BucketType.user)
    async def dog(self, ctx):
        '''Fetches a random image of a dog.'''
        with urllib.request.urlopen("https://dog.ceo/api/breeds/image/random") as url: #cleans up code after reading, even if errors are thrown
            data = json.loads(url.read().decode()) #uses urllib to read and deocde the link, then loads it with the json library
            link = data["message"]

        embed = discord.Embed(title = "Dog", timestamp = datetime.utcnow(), colour = discord.Color.light_grey())
        embed.set_image(url = link)
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def cat(self, ctx):
        '''Fetches a random image of a cat.'''
        pass

    @commands.command()
    @commands.cooldown(10, 15, commands.BucketType.user)
    async def buns(self, ctx):
        '''Fetches a random image of a rabbit/bunny.'''
        pass

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