# DnDbot - Discord bot that reads data from https://open5e.com/ and returns it
# directly in chat.
import discord
import json
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

daddy = 'Kitime#9120'
dotaapi = 'https://api.opendota.com/api'
dndapi = 'https://api.open5e.com'
oauthtoken = 'Insert Token Here'

@bot.event
async def on_ready():
    print('------')
    print('Logged in - Ready.')
    print('USERNAME: ' + bot.user.name)
    print('UID     : ' + str(bot.user.id))
    print('Running on platform: ' + os.name)
    print('------')

#does not currently work
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.content.startswith('?online'):
        await message.channel.send('Yo, I\'m online. Feel that BDE.')
    elif message.content.startswith('?kill'):
        if str(message.author) == daddy:
            print('Killed by Daddy')
            await message.channel.send('Goodbye, Daddy!')
            await bot.logout()
            exit
        elif message.author != daddy:
            await message.channel.send('Goodbye, Tien!')
            print('Killed by ' + str(message.author))
            await bot.logout()
            exit
# end nonworking event code

#Bot command events:
@bot.command()
async def online(ctx):
    weonline = 'Yo, I\'m online. Feel that BDE.'
    print('called bot event')
    await ctx.send(content=weonline)
    
#    if message.content.startswith('bye'):
#        await message.channel.send("CHIAOTZU, NOOOOOO!")

#API JSON Handlers:
#@bot.event
#async def onmessage(message):
    #if message starts with ?dota apirequest
    #if message.content.startswith('?dotagetrank'):
    #    #parse the message:
    #    message.content
    #    print('DEBUG: parsing dotagetrank call for ' + steamid)
    #    dotaid = message.content    
    # #get rank from OpenDota API:
    #    if message.content

#@bot.command()
#async def dotagetrank(rank, steamid):
#    rank.send('DoTA 2 rank goes here after parsing, Steam ID is passed as' + steamid)

    

        #then we get and parse the JSON the OpenDota API gives us.
    #or, if message starts with ?dnd apirequest
        #then, we get and parse the JSON the OpenDND API gives us...

bot.run(oauthtoken)