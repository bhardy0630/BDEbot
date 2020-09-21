## basic Discord bot that reads data from various APIs and returns it to the caller.
## v0.5

import discord
import asyncio  ## discord.py is asynchronous event driven library, so we want to use nonblocking io operations.
import aiohttp  ## Used for HTTP GET requests to API services.
import json
import os       ## not really needed right now...
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
# let's take console input for some of these variables in the near future.
daddy = 'Kitime#9120' 
## daddy is our list of authorized users (in name+identifier format) - probably the person running the bot.

dotaapi = 'https://api.opendota.com/api'
## We are calling the opendota API.

oauthtoken = '' 
## oauth login token for the bot goes here.

@bot.event
async def on_ready():
    print('------')
    print('Logged in - Ready.')
    print('USERNAME: ' + bot.user.name)
    print('UID     : ' + str(bot.user.id))
    print('Running on platform: ' + os.name)
    print('------')

## Old way to do it.
#@bot.listen()
#async def on_message(message):
#    print('called on_message')
#    if message.author == bot.user:
#        return
#    elif message.content.startswith('?online'):
#        print('called ?online')
#        await message.channel.send('Yo, I\'m online. Feel that BDE.')
#        exit

#Bot command events (new way we do it):

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
    if str(killer) == daddy: ## daddy is our authorized user defined earlier.4
            print('CONSOLE: Bot received !kill command from authorized user ' + str(killer) +', shutting down...')
            await message.channel.send('OK, shutting down...')
            await bot.logout()
            await bot.close()
            exit
    elif killer != daddy:
            await message.channel.send(str(killer) + ' attempted to shut down' + str(bot.user.name) + '...')
            await asyncio.sleep(2.5)
            print('Attempted to be Killed by ' + str(killer))
            await message.channel.send('...but it failed!')
            await message.channel.send('Nice try, ' + str(killer))
            pass
            exit

## !dotagetrank command:
# needs to accept an actual SteamID instead of Account ID, or convert.
# Real SteamID for J.B.H. : 76561198037267879 (REF: https://steamid.io/lookup/76561198037267879)
@bot.command()
async def dotagetrank(ctx, steamid): ## needs exception handler to catch instances where no SteamID is input.
        await ctx.send('OK, getting ranking information for SteamID ' + str(steamid) + '...')
        ## aiohttp is pretty verbose to give the event loop opportunities to switch context:
        async with aiohttp.ClientSession() as session: ## Create the session
            async with session.get(dotaapi + '/players/' + steamid) as response: ## Make the GET request to the opendota API
                dotajson = await response.text() # OK, we have the API response saved, now we deserialize into a python object:
                await ctx.send('DEBUG: Now stepping into deserialization of API response...')
                # ... Which python makes as easy as this:
                dotaresponse = json.loads(dotajson) # JSON object data now deserialized to python object data (with dict type).
                await ctx.send(str(dotaresponse['profile']['personaname']) + '\'s MMR Estimate is ' + str(dotaresponse['mmr_estimate']['estimate'])) # dotaresponse is now a python dict containing the JSON object we got from the API request.
                await ctx.send('Hopefully, we just printed the solo MMR rank subobject to chat...')
                # that value seems to not mean much for now...
                pass

        # HTTP GET dotaapi + /players/ + steamid

    #    GET https://api.opendota.com/api/players/77002151 (requires steam "account ID")- sample of return:
    # https://docs.opendota.com/#tag/players%2Fpaths%2F~1players~1%7Baccount_id%7D%2Fget
    #    message.content
    #    print('DEBUG: parsing dotagetrank call for ' + steamid)
    #    dotaid = message.content    
    # #get rank from OpenDota API:
    #    if message.content

## @bot.command()
## async def recentlyplayed(ctx, steamid):
#### Use Steam Web API command as follows to return JSON 
#### (example: https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=&steamid=76561198037267879&format=json)
##
##
##

#API JSON Handler:
# API return = apijsondata
# apijsondata['rank']
# 'value_of_rank'

bot.run(oauthtoken)