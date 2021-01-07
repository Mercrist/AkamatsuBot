from discord.ext import commands
from datetime import datetime
import discord
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
            embed = discord.Embed(title=f"**Deleted Post by {message.author}**", timestamp=datetime.utcnow(), colour=discord.Color.blue())
            embed.add_field(name="Deleted Content:", value= message.content, inline=False)
            if self.archiveChannel is None and message.guild.system_channel is not None: #channel hasnt been set by user but the system channel is
                channel = message.guild.system_channel

            elif self.archiveChannel is not None: #channel has been set by user
                channel = self.bot.get_channel(self.archiveChannel)

            else: #any other scenario
                channel = message.channel
                embed = discord.Embed(description=f"Set a system channel or an archive channel!", colour=discord.Color.gold())
        await channel.send(embed=embed)

    @commands.command()
    async def setarchive(self, ctx, channel):
        '''Sets a channel to store deleted messages'''
        if ctx.author.guild_permissions.administrator:
            self.archiveChannel = int(channel.strip("<>#"))
            embed = discord.Embed(title=f"Archive channel set to #{self.bot.get_channel(self.archiveChannel)}.", timestamp=datetime.utcnow(), colour=discord.Color.gold())
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
    async def load(self, ctx, cogName):
        '''Loads a specified Cog.'''
        is_owner = await self.bot.is_owner(ctx.author)  #prevents other users from loading or unloading the bot
        if is_owner:
            self.bot.load_extension(f"cogs.{cogName}")  #loads the cog in /cogs/cogName.py
            embed = discord.Embed(description=f"{cogName} was loaded succesfully!", colour=discord.Color.dark_orange())
            await ctx.send(embed=embed)

    @commands.command()
    async def unload(self, ctx, cogName):  #by using cogs, you dont have to turn the bot offline, simply unload the cogs with the command
        '''Unloads a specified Cog.'''
        is_owner = await self.bot.is_owner(ctx.author)
        if is_owner:
            self.bot.unload_extension(f"cogs.{cogName}")
            embed = discord.Embed(description=f"{cogName} was loaded succesfully!", colour=discord.Color.dark_orange())
            await ctx.send(embed=embed)

    @commands.command()
    async def reload(self, ctx, cogName):
        '''Reloads the bot automatically.'''
        is_owner = await self.bot.is_owner(ctx.author)
        if is_owner:
            self.bot.unload_extension(f"cogs.{cogName}")
            self.bot.load_extension(f"cogs.{cogName}")
            embed = discord.Embed(description=f"{cogName} was loaded succesfully!", colour=discord.Color.dark_orange())
            await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx, time = None):
        '''Returns the bots invite link.'''
        embed = discord.Embed(description = f"", colour=discord.Color.dark_orange())
def setup(bot):
    bot.add_cog(Admin(bot))