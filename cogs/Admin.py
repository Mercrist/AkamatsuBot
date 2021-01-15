from datetime import datetime
from discord.ext import commands
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

    @commands.command()
    async def source(self, ctx):
        '''Links the bots GitHub page.'''
        link = "https://github.com/Mercrist/AkamatsuBot"
        embed = discord.Embed(description= f":newspaper: Access the bots repository [here]({link})!", timestamp=datetime.utcnow(), colour=discord.Color.from_rgb(105,105,105))
        embed.set_author(name="Bot Repository Link", icon_url="https://image.flaticon.com/icons/png/512/25/25231.png")
        await ctx.send(embed = embed)

    @commands.command()
    async def help(self, ctx):
        '''Returns an embed with list of all available commands.'''
        adminDesc = "**a!setarchive <channel>:** If no system channel has been set, records deleted messages on this channel.\n\n"\
                    "**a!togglearchive:** On by default. Disables message archiving if it's enabled and vice versa.\n\n" \
                    "**a!invite <time>:** Creates an invite for the server. If no time is specified, creates a permament invite. For timed invites, time should be passed in minutes.\n\n"\
                    "**a!source:** View the bot's GitHub repository, bot invite link can be found here."

        animalDesc = "**a!<animal>:** Returns a random image of an animal. Supported animal commands: `dog`, `cat`, `buns`, `otters`, `ferret`, `panda`, `fox`, `hamster`, `quokka`."

        redDesc = "**a!sub <subreddit>:** Returns the top 15 hottest posts from a specified subreddit.\n\n"\
                  "**a!subpost <subreddit>:** Retrieves a random hot post from a specified subreddit. NSFW subs can only be linked in NSFW channels.\n\n"\
                  "**a!meme:** Displays a random meme."

        covidDesc = "**a!countries:** Displays a list of all available countries whose COVID spread can be visualized.\n\n"\
                    "**a!spread <country>:** Embeds a graph visualizing the COVID-19 spread for a given country and displays relevent statistics."

        embed = discord.Embed(timestamp=datetime.utcnow(), colour= discord.Color.from_rgb(255, 255, 255))
        embed.set_author(name="List of all avaliable bot commands! Bot prefix is a![command]", icon_url="https://lh3.googleusercontent.com/proxy/TkGKCrBTpKJo-nuS0hlhDA9t_gfVQ18tcmhuarEXQBOGH7BDoTE5N4zu1F8wIkvhB1EjdeWHnL2AywctMxWpLUyFYhalSKOsAidy3W0g7LCCKlkhoJcMMZFtVOsxpbdPvS4")
        embed.set_footer(text=f"Requested by {ctx.message.author}.", icon_url=ctx.message.author.avatar_url)
        embed.add_field(name=":gear: **__Admin__** ", value= adminDesc, inline= False)
        embed.add_field(name=":dog: **__Animals__** ", value= animalDesc, inline= False)
        embed.add_field(name=":globe_with_meridians: **__Reddit__** ", value= redDesc, inline= False)
        embed.add_field(name=":earth_americas: **__COVID__** ", value= covidDesc, inline= False)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Admin(bot))