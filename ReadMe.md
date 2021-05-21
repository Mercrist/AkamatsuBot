# AkamatsuBot

[![Python](https://img.shields.io/badge/python%20-3.8.1-blue)](https://www.python.org/downloads/) [![Discord](https://img.shields.io/badge/discord.py-1.5.1-%235d8aa8)](https://discordpy.readthedocs.io/en/latest/index.html)  [![PRAW/async](https://img.shields.io/badge/asyncpraw-7.1.0-red)](https://asyncpraw.readthedocs.io/en/latest/) [![Matplot](https://img.shields.io/badge/matplotlib-3.3.3-orange)](https://matplotlib.org/)   [![BeautySoup](https://img.shields.io/badge/beautifulsoup-4.9.3-lightgrey)](https://pypi.org/project/beautifulsoup4/) ![License][3] ![ID][6]

<img src="https://i.imgur.com/ktIpxg1.png" align="right"
     alt="AkamatsuBot Logo" width="250" height="250">
     
AkamatsuBot is a general purpose Discord bot built via [discord.py][1] featuring multimedia integration, admin commands, and a COVID statistics displayer.
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

## Running and more

The bot can be invited to a server via the [following link][2]. Alternatively, one could install and run the bot themselves.

### Running the bot locally

First, clone the repository on a computer and install the library requirements.
```bash
> git clone https://github.com/Mercrist/AkamatsuBot.git

> pip3 install -r requirements.txt
```

Secondly, a config file must be manually created. `config.py` must have the following format:

```bash
token= "Discord token from developer portal"
prefix = "a!"

#for PRAW
ID = "Bot's ID"
secret = "Snag from reddit's bot portal"
passwd = "The bot account's password"
username = "Avccount username"
agent = "The bot's unique identifier"
```
Refer to the documentation for both [PRAW][4] and [Discord's Developer Portal][5] for more info on how to fill out these fields.

[1]: https://discordpy.readthedocs.io/en/latest/index.html
[2]: https://discord.com/api/oauth2/authorize?client_id=788839179832262686&permissions=8&scope=bot
[3]: https://img.shields.io/badge/license-MIT-%23800000
[4]: https://asyncpraw.readthedocs.io/en/latest/
[5]: https://discord.com/developers/docs/intro
[6]: https://img.shields.io/badge/Discord%20ID-Mercrist%20%236784-%234e5d94