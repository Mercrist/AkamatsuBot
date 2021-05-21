# AkamatsuBot

![Python][1] ![Discord][2] ![PRAW][3] ![Matplot][4] ![Soup][5]

<img src="https://i.imgur.com/ktIpxg1.png" align="right"
     alt="AkamatsuBot Logo" width="250" height="250">
     
AkamatsuBot is a general purpose Discord bot built via [discord.py][6] featuring multimedia integration, admin commands, and a COVID statistics displayer.
A list of available commands, along with screenshots and an invite link, is shown below. The bot currently runs on a Raspberry Pi 3.

## Commands
### General

* The bot's prefix is `a!`. Every command must be prefixed by this.
* `a!help` brings up a list of available commands!
* <img align="center" style="float: centrer; margin: 0 10px 0 0;" src="https://i.imgur.com/Ntf4Z0Z.png" height="494" width="504"/>

### Animal Commands

* `a!<animal>` displays a random image of a supported animal.
* <img align="center" style="float: centrer; margin: 0 10px 0 0;" src="https://i.imgur.com/HC6BA7T.png" height="412" width="567"/>

### Reddit Commands

* `a!sub <subreddit>` displays the top posts for the given subreddit. Navigate with the paginator reaction arrows!
`a!meme` and `a!sub` each display a single post.

* <img align="center" style="float: centrer; margin: 0 10px 0 0;" src="https://i.imgur.com/yt5R2to.png" height="587" width="645"/>

### COVID Commands

* Use `a!countries` to view the countries supported!
* `a!spread` will demonstrate that countries current statistics. Sift through the supported countries with the paginators arrows.
* <img align="center" style="float: centrer; margin: 0 10px 0 0;" src="https://i.imgur.com/Tv1h7v6.png" height="614" width="524"/>


[1]: https://img.shields.io/badge/python%20-3.8.1-blue
[2]: https://img.shields.io/badge/discord.py-1.5.1-%235d8aa8
[3]: https://img.shields.io/badge/asyncpraw-7.1.0-red
[4]: https://img.shields.io/badge/matplotlib-3.3.3-orange
[5]: https://img.shields.io/badge/beautifulsoup-4.9.3-lightgrey
[6]: https://discordpy.readthedocs.io/en/latest/index.html