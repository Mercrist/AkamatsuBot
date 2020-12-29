from discord.ext import commands
from datetime import datetime
import discord
import urllib.request
import json
import pathlib
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

        path = urllib.parse.urlparse(link).path #get the url/link path, ex. everthing from /breeds/ onwards: /breeds/hound-walker/n02089867_1471.jpg
        dogName = pathlib.Path(path).parts[2] #treat the link's path as a directory path, pathlib.Path(path).parts returns a tuple containing each part of the path
                                             #elaborating on the above stated with an example: ('/', 'breeds', 'hound-walker', 'n02089867_1471.jpg')

        if dogName.find("-") != -1:
            dogName = dogName.split("-")
            dogName = dogName[1][0].upper()+dogName[1][1:] + " " + dogName[0][0].upper()+dogName[0][1:] #dog API has two word breed names reversed and uncapitalized
        else:
            dogName = dogName[0][0].upper() + dogName[1:]

        embed = discord.Embed(title = dogName, timestamp = datetime.utcnow(), colour = discord.Color.light_grey())
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