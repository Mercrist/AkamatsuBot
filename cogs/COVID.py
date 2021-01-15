from discord.ext import commands
from datetime import datetime
from dateutil import relativedelta
from disputils import BotEmbedPaginator
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import aiohttp
import discord
import dateutil.parser #handle iso 8601 time codes
import io
class COVID(commands.Cog):
    '''Command to display graphs and data for COVID.'''
    def __init__(self, bot):
        self.bot = bot
        self.http_session = aiohttp.ClientSession()

    @staticmethod
    def _y_fmt(tick_val, pos):
        '''Format y tick values'''
        if tick_val > 1000000:
            val = int(tick_val) / 1000000
            return f'{val:.1f}M'
        elif tick_val > 1000:
            val = int(tick_val) // 1000
            return f'{val:d}k'
        else:
            return int(tick_val)

    @commands.command()
    @commands.cooldown(3, 15, commands.BucketType.user)
    async def countries(self, ctx):
        '''Returns a list of all valid countries.'''
        async with self.http_session.get('https://api.covid19api.com/summary') as url:
            if url.status == 200:
                js = await url.json()
                countries = [countries["Country"] for countries in js["Countries"]]
                embeds = []
                i = 1
                while len(countries) >= 15:
                    embed = discord.Embed(timestamp=datetime.utcnow(), colour=discord.Color.from_rgb(107, 202, 226))
                    embed.set_author(name=f"List of all available countries whose graph can be retrieved: ", icon_url="https://i.pinimg.com/originals/2c/f3/0f/2cf30ffdbfa3db621d303e9575ff9e47.gif")
                    for country in countries[:15]:
                        if len(country) > 20:
                            country = country[:20] + "..."
                        embed.add_field(name=f"{i}) {country}", value = "\u200b")
                        embed.set_footer(text=f"Requested by {ctx.message.author}.", icon_url=ctx.message.author.avatar_url)
                        i += 1

                    embeds.append(embed)
                    del countries[:15]
                #final page
                embed = discord.Embed(timestamp=datetime.utcnow(), colour=discord.Color.from_rgb(107, 202, 226))
                embed.set_author(name=f"List of all available countries whose graph can be retrieved: ", icon_url="https://i.pinimg.com/originals/2c/f3/0f/2cf30ffdbfa3db621d303e9575ff9e47.gif")
                embed.set_footer(text=f"Requested by {ctx.message.author}.", icon_url=ctx.message.author.avatar_url)
                for country in countries[:len(countries)]: #final page
                    if len(country) > 20:
                        country = country[:20] + "..."
                    embed.add_field(name=f"{i}) {country}", value = "\u200b")
                    i += 1
                embeds.append(embed)
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()


    @commands.command()
    @commands.cooldown(3, 15, commands.BucketType.user)
    async def spread(self, ctx, *, country): #https://discordpy.readthedocs.io/en/latest/faq.html?highlight=consume%20rest#why-do-my-arguments-require-quotes
        '''Shows a summary of the infection spread and a graph for a given country.'''
        async with self.http_session.get('https://api.covid19api.com/summary') as url:
            if url.status == 200:
                js = await url.json()
                try:
                    data = next({"Slug": countries["Slug"], "NewCases": countries["NewConfirmed"], "NewDeaths": countries["NewDeaths"], "TotalDeaths": countries["TotalDeaths"], "NewRecovered": countries["NewRecovered"], "TotalRecovered": countries["TotalRecovered"], "Date": dateutil.parser.parse(countries["Date"])} for countries in js["Countries"] if countries["Country"].lower() == country.lower() or countries["Slug"].replace("-", " ") == country.lower())
                except StopIteration: #country not found in the json
                    embed = discord.Embed(description=f"Sorry, no such country is available or supported.", colour=discord.Color.dark_teal())
                    await ctx.send(embed=embed)
                    return

        async with self.http_session.get(f'https://api.covid19api.com/total/dayone/country/{data["Slug"]}') as url:
            if url.status == 200:
                js = await url.json()
                recoveredY = []
                confirmedY = []
                deathsY = []
                dateX = []
                for i in range(len(js)):
                    recoveredY.append(js[i]["Recovered"])
                    confirmedY.append(js[i]["Confirmed"])
                    deathsY.append(js[i]["Deaths"])
                    dateX.append(dateutil.parser.parse(js[i]["Date"]))

                r = relativedelta.relativedelta(dateX[-1], dateX[0])
                elapsedDesc = f"**{r.months} months and {r.days} days**" if r.years == 0 else f"**{r.years} years, {r.months} months, and {r.days} days**"
                lastDate = f"COVID graph data updated as of {dateX[-1].month}/{dateX[-1].day}/{dateX[-1].year}"

                embed = discord.Embed(description = "**Coronavirus infection stats:** ", timestamp = datetime.utcnow(), colour = discord.Color.from_rgb(191, 255, 0))
                embed.set_author(name = f"Displaying COVID-19 infection graph for: {country.title()}", icon_url= "https://www.wnpr.org/sites/wnpr/files/styles/x_large/public/202004/SARS-CoV-2_without_background.png")
                embed.add_field(name = ":white_check_mark: __Confirmed Infections__ ", value = f"**{max(confirmedY):,}** (+{data['NewCases']:,})")
                embed.add_field(name = ":skull_crossbones: __Recent Deaths__ ", value = f"**{data['TotalDeaths']:,}** (+{data['NewDeaths']:,})")
                embed.add_field(name = ":health_worker: __Recent Recovered__ ", value = f"**{data['TotalRecovered']:,}** (+{data['NewRecovered']:,})")
                embed.add_field(name = ":chart_with_downwards_trend: __Mortality Rate__ ", value = f"**{round((data['TotalDeaths']/max(confirmedY))*100, 2):,}%**")
                embed.add_field(name = ":chart_with_upwards_trend: __Recovery Rate__ ", value = f"**{round((data['NewRecovered']/max(confirmedY))*100, 2):,}%**")
                embed.add_field(name = ":calendar: __Time Elapsed__ ", value = elapsedDesc)
                embed.set_footer(text=f"Requested by {ctx.message.author} | {lastDate}", icon_url=ctx.message.author.avatar_url)

                #setting up plots
                plt.style.use('dark_background')
                fig, ax = plt.subplots()
                ax.xaxis.set_major_locator(mdates.MonthLocator())  # includes datetime tag at every month
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))  # format datetime string
                ax.xaxis.set_minor_locator(mdates.MonthLocator())  # splits up intervals by months
                ax.yaxis.set_major_formatter(FuncFormatter(self._y_fmt)) #format y values
                ax.yaxis.grid()
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)

                #plot confirmed cases line
                ax.plot(dateX, confirmedY, label = 'Confirmed', color = "c", marker = ".")
                ax.legend(loc='upper left', fancybox=True, facecolor='0.2')
                #plot deaths line
                ax.plot(dateX, deathsY, label='Deaths', color="red", marker = ".")
                ax.legend(loc='upper left', fancybox=True, facecolor='0.2')
                #plot recoveries
                ax.plot(dateX, recoveredY, label='Recoveries', color="orange", marker=".")
                ax.legend(loc='upper left', fancybox=True, facecolor='0.2')

                ax.set_ylim(0)
                fig.autofmt_xdate()  #rotates and formats tags
                plt.savefig('cogs/graphs/graph.png', transparent=True)
                plt.close(fig)

                with open('cogs/graphs/graph.png', 'rb') as binary: #needs to be read as a binary for discord
                    file = io.BytesIO(binary.read())
                image = discord.File(file, filename='graph.png')
                embed.set_image(url='attachment://graph.png')
            await ctx.send(file = image, embed=embed)

def setup(bot):
    bot.add_cog(COVID(bot))