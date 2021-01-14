from discord.ext import commands
from datetime import datetime
import aiohttp
import discord
import dateutil.parser #handle iso 8601 time codes
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
class COVID(commands.Cog):
    '''Command to display graphs and data for COVID.'''
    def __init__(self, bot):
        self.bot = bot
        self.http_session = aiohttp.ClientSession()

    @commands.command()
    @commands.cooldown(3, 15, commands.BucketType.user)
    async def spread(self, ctx, *, country): #https://discordpy.readthedocs.io/en/latest/faq.html?highlight=consume%20rest#why-do-my-arguments-require-quotes
        '''Shows a summary of the infection spread and a graph for a given country.'''
        async with self.http_session.get('https://api.covid19api.com/summary') as url:
            if url.status == 200:
                js = await url.json()
                try:
                    data = next({"Slug": countries["Slug"], "NewCases": countries["NewConfirmed"], "NewDeaths": countries["NewDeaths"], "TotalDeaths": countries["TotalDeaths"], "NewRecovered": countries["NewRecovered"], "TotalRecovered": countries["TotalRecovered"], "Date": dateutil.parser.parse(countries["Date"])} for countries in js["Countries"] if countries["Country"].lower() == country.lower())
                except StopIteration: #country not found in the json
                    embed = discord.Embed(description=f"Sorry, no such country is available or supported.", colour=discord.Color.dark_teal())
                    await ctx.send(embed=embed)
                    return

        async with self.http_session.get(f'https://api.covid19api.com/total/dayone/country/{data["Slug"]}') as url:
            if url.status == 200:
                js = await url.json()
                confirmedY = []
                deathsY = []
                recoveredY = []
                dateX = []
                for i in range(len(js)):
                    confirmedY.append(js[i]["Confirmed"])
                    deathsY.append(js[i]["Deaths"])
                    recoveredY.append(js[i]["Recovered"])
                    dateX.append(dateutil.parser.parse(js[i]["Date"]))

            fig, ax = plt.subplots()
            ax.xaxis.set_major_locator(mdates.MonthLocator())  # includes datetime tag at every month
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))  # format datetime string
            ax.xaxis.set_minor_locator(mdates.MonthLocator())  # splits up intervals by months
            ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
            ax.plot(dateX, confirmedY, label = 'Confirmed', color = "blue")
            ax.legend()
            fig.autofmt_xdate()  # rotates tags
            plt.show()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(COVID(bot))