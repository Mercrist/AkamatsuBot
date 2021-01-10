from discord.ext import commands
from random import randint
class Greetings(commands.Cog):
    '''Contains the listener for when a user first joins a server the bot is in.'''
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member): #context only passed for commands
        with open("greetings.txt", "r") as msg:
            msg = [elem.strip() for elem in msg.readlines()]
            msg = msg[randint(0, len(msg) - 1)]  # picks a random greeting message
            channel = member.guild.system_channel  #gets system channel for when user joins (found in server settings under overview)
            if channel is not None:
                try:
                    await channel.send(msg.format(member.mention)) #messages won't work without format
                except IndexError:
                    await channel.send(msg.format(member.guild.name, member.mention))
def setup(bot):
    bot.add_cog(Greetings(bot)) #passes an instance of the Class to the bot to use his commands