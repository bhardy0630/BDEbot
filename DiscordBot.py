## basic Discord bot that reads data from various APIs and returns it to the caller.
## v0.5

import discord
import asyncio  ## discord.py is asynchronous event driven library, so we want to use nonblocking io operations.
import aiohttp  ## Async lib Used for HTTP GET requests to API services.
import json
import os       ## not really needed right now...
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
# let's take console input for some of these variables in the near future.
owner = 'Kitime#9120' 
## owner is our authorized user (in name#identifier format).

dotaapi = 'https://api.opendota.com/api'
## We are calling the opendota API.

oauthtoken = '' 
## oauth login token for the bot goes here. (Raises RuntimeError if no token is defined.)
## oauthtoken = input("Enter your oauth token: ")


@bot.event
async def on_ready():
    print('------')
    print('Logged in - Ready.')
    print('USERNAME: ' + bot.user.name)
    print('UID     : ' + str(bot.user.id))
    print('Running on platform: ' + os.name)
    print('------')

## !online command:
@bot.command()
async def online(ctx):
    weonline = 'Yo, I\'m online. Feel that BDE.'
    # functionize this next print call to print any command called to console, not just !online
    print('CONSOLE: User ' + str(ctx.author) + ' called ' + str(ctx.message.content) + ' in channel: ' + str(ctx.message.channel))
    await ctx.send(content=weonline)
    await ctx.send(content='DEBUG: We\'re online, we logged that call to console, and we\'re running on platform: ' + str(os.name) + '. Awaiting your orders, ' + str(ctx.author) + '!')
    pass

## !kill command:
@bot.command()
async def kill(message):
    killer = message.author
    if str(killer) == owner: ## owner is our authorized user defined earlier
            print('CONSOLE: Bot received !kill command from authorized user ' + str(killer) +', shutting down...')
            await message.channel.send('OK, shutting down...')
            await bot.logout()
            await bot.close()
            exit
    elif killer != owner:
            await message.channel.send(str(killer) + ' attempted to shut down' + str(bot.user.name) + '...')
            await asyncio.sleep(2.5)
            print('Attempted to be Killed by ' + str(killer))
            await message.channel.send('...but it failed!')
            await message.channel.send('Nice try, ' + str(killer))
            pass
            exit

## !dotagetrank command:
# needs to accept an actual SteamID instead of Account ID, or convert.
# Example Real SteamID for J.B.H. : 76561198037267879 (REF: https://steamid.io/lookup/76561198037267879)
@bot.command()
async def dotagetrank(ctx, steamid): ## needs exception handler to catch instances where no SteamID is input.
        await ctx.send('OK, getting ranking information for SteamID ' + str(steamid) + '...')
        async with aiohttp.ClientSession() as session: ## Create the session
            async with session.get(dotaapi + '/players/' + steamid) as response: ## Make the GET request to the opendota API
                dotajson = await response.text() ## API response saved, now we deserialize into a python object:
                dotaresponse = json.loads(dotajson) # JSON object data now deserialized to python object data (with dict type).
                try:
                    displayname = dotaresponse['profile'].get('personaname') ## returns nothing if expose public match data not enabled!!!
                except KeyError: # Raised if no dictionary key is returned - usually due to no data return from API.
                    await ctx.send('ERR: Hmm... I couldn\'t find any data for ' + steamid + ', do they have \'expose public data\' option enabled in Dota?')
                    await ctx.send('For more info, click here: https://plair.zendesk.com/hc/en-us/articles/360019111193-Enable-Expose-Public-Match-Data-Setting' + ' - You may also need to play at least one match once enabling. Ask matt about that.')
                    pass
                else:
                    solorank = str(dotaresponse.get('solo_competitive_rank'))
                    dotaplus = str(dotaresponse['profile'].get('plus'))
                    ranktier = dotaresponse.get('rank_tier')
                    await ctx.send(displayname + '\'s MMR Estimate is ' + str(dotaresponse['mmr_estimate']['estimate'])) # values seem to not mean much for now... Test these estimates.
                    await ctx.send('Solo MMR Rank: ' + solorank)
                    await ctx.send(':moneybag::money_mouth: Dota Plus Subscriber? :money_mouth::moneybag: = ' + dotaplus)
                    await ctx.send('Rank Tier: ' + str(ranktier))
                    pass

## @bot.command()
## async def steamrecentlyplayed(ctx, steamid):
#### Use Steam Web API command as follows to return JSON 
#### (example: https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=BC92F2D1D7570507DA6249FF5C21E80C&steamid=76561198037267879&format=json)

bot.run(oauthtoken)