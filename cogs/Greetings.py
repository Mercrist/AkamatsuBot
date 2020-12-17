from discord.ext import commands
class Greetings(commands.Cog):
    '''When the bot first joins the server.'''
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Yes")

    @commands.command()
    async def greet(self, ctx):
        await ctx.send("Hai hai")


def setup(bot):
    bot.add_cog(Greetings(bot)) #passes an instance of the Class to the bot to use his commands
