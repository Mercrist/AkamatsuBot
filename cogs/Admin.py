from discord.ext import commands
import discord
from datetime import datetime
class Admin(commands.Cog):
    '''Commands and events to be used or triggered for administrative purposes.'''
    def __init__(self, bot):
        self.bot = bot
        self.archive = True
        self.archiveChannel = None

    @commands.Cog.listener()  #only need one on_error commands listener for the whole thing for slowdowns
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(description=f"You're going too fast, slow down!", colour=discord.Color.gold())
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        '''Archives and sends a message whenever it's deleted'''
        if self.archive: #only archives deleted messages if it's been enabled in said server
            embed = discord.Embed(title=f"**Deleted Post**", description = f"By @{message.author} in {message.channel.mention}", timestamp=datetime.utcnow(), colour=discord.Color.blue())
            embed.add_field(name="Deleted Content:", value=message.content, inline=False)
            if self.archiveChannel is None and message.guild.system_channel is not None: #channel hasnt been set by user but the system channel is
                channel = message.guild.system_channel

            elif self.archiveChannel is not None: #channel has been set by user
                channel = self.bot.get_channel(self.archiveChannel)

            elif self.archive and message.guild.system_channel is None: #any other scenario
                channel = message.channel
                embed = discord.Embed(description=f"Set a system channel or an archive channel!", colour=discord.Color.gold())
            await channel.send(embed=embed)

    @commands.command()
    async def setarchive(self, ctx, channel):
        '''Sets a channel to store deleted messages'''
        if ctx.author.guild_permissions.administrator:
            self.archiveChannel = int(channel.strip("<>#"))
            embed = discord.Embed(description=f"Archive channel set to {self.bot.get_channel(self.archiveChannel).mention}.", timestamp=datetime.utcnow(), colour=discord.Color.gold())
            await ctx.channel.send(embed = embed)

    @commands.command()
    async def togglearchive(self, ctx):
        '''Toggles the function to store deleted messages'''
        if ctx.author.guild_permissions.administrator:
            if not self.archive:
                embed = discord.Embed(description=f"Deleted messages archiving has been enabled.", timestamp=datetime.utcnow(), colour=discord.Color.gold())
                self.archive = True
            else:
                embed = discord.Embed(description=f"Deleted messages archiving has been disabled.", timestamp=datetime.utcnow(), colour=discord.Color.gold())
                self.archive = False
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cogName):
        '''Loads a specified Cog.'''
        self.bot.load_extension(f"cogs.{cogName}")  #loads the cog in /cogs/cogName.py
        embed = discord.Embed(description=f"{cogName} was loaded succesfully!", colour=discord.Color.dark_orange())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cogName):  #by using cogs, you dont have to turn the bot offline, simply unload the cogs with the command
        '''Unloads a specified Cog.'''
        self.bot.unload_extension(f"cogs.{cogName}")
        embed = discord.Embed(description=f"{cogName} was unloaded succesfully!", colour=discord.Color.dark_orange())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cogName):
        '''Reloads the bot automatically.'''
        self.bot.unload_extension(f"cogs.{cogName}")
        self.bot.load_extension(f"cogs.{cogName}")
        embed = discord.Embed(description=f"{cogName} was reloaded succesfully!", colour=discord.Color.dark_orange())
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx, time = 0):
        '''Returns the bots invite link. Time is set in minutes'''
        if ctx.author.guild_permissions.administrator:
            time = time*60 #converts minutes to seconds
            link = await ctx.channel.create_invite(max_age = time)
            if time == 0:
                desc = f"An invite for {ctx.guild.name} has been generated! This link has been set to never expire: {link}"
            else:
                desc = f"An invite for {ctx.guild.name} has been generated! Share the link for the next {time//60} minutes: {link} "
            embed = discord.Embed(description = desc, timestamp= datetime.utcnow(), colour=discord.Color.blurple())
            await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Admin(bot))