# Discord bot that reads data from various APIs and returns it
# directly in chat to the caller.
import discord
import json
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
# let's take console input for some of these variables in the near future.
daddy = 'Kitime#9120'
dotaapi = 'https://api.opendota.com/api'
oauthtoken = ''

@bot.event
async def on_ready():
    print('------')
    print('Logged in - Ready.')
    print('USERNAME: ' + bot.user.name)
    print('UID     : ' + str(bot.user.id))
    print('Running on platform: ' + os.name)
    print('------')
    exit

@bot.listen()
async def on_message(message):
    print('called on_message')
    if message.author == bot.user:
        return
    elif message.content.startswith('?online'):
        print('called ?online')
        await message.channel.send('Yo, I\'m online. Feel that BDE.')
        exit

#Bot command events:
@bot.command()
async def online(ctx):
    weonline = 'Yo, I\'m online. Feel that BDE.'
    print('called bot event')
    await ctx.send(content=weonline)

@bot.command()
async def kill(message):
    killer = message.author
    if str(killer) == daddy:
            print('Killed by Daddy')
            await message.channel.send('Goodbye, Daddy!')
            await bot.logout()
            await bot.close()
            exit
    elif killer != daddy:
            await message.channel.send('Goodbye, Tien!')
            print('Killed by ' + str(killer))
            await message.channel.send('Nice try, ' + str(killer))
            await bot.logout()
            await bot.close()
            exit

@bot.command()
async def dotagetrank(ctx, steamid):
    await ctx.send()
    pass
    #    GET https://api.opendota.com/api/players/77002151 - sample of return:
    # https://docs.opendota.com/#tag/players%2Fpaths%2F~1players~1%7Baccount_id%7D%2Fget
    steamid
    #    message.content
    #    print('DEBUG: parsing dotagetrank call for ' + steamid)
    #    dotaid = message.content    
    # #get rank from OpenDota API:
    #    if message.content

#API JSON Handler:

bot.run(oauthtoken)