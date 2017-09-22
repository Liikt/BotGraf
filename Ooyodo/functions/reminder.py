import discord
import asyncio
from time import gmtime, time, sleep

from utils.utils import get_channel_by_id


"""
This function reminds us every 12 hours to do our pvps

It takes the client as an argument to be able to send messages

never returns
"""
async def pvp(client):
    # Calculate the time difference and when to send the first message
    first = (17 - gmtime(time()).tm_hour) % 12

    # Find the channel where to send the reminder
    kancolle_stuff_id = '242858060224135168'
    channel = await get_channel_by_id(client, kancolle_stuff_id)

    # Check if the channel was found
    if channel is None:
        print("Couldn't find kancolle stuff!")
        return

    # Debug Print
    print("I should remind in:", first, 'hours and', (30-gmtime(time()).tm_min) % 60, 'minutes in', channel.name, 'for pvp.')

    # Wait a bit to get approximatly the right time to send
    while 25 < gmtime(time()).tm_min < 35 or (17 - gmtime(time()).tm_hour) % 12 != 0:
        await asyncio.sleep(30)

    # reset the variable so we always wait ~11.5 hours
    first = 12

    while True:
        # prevent timedrift due to different clocks also to prevent missing the time completly have
        # a +-5 minutes timewindow
        while 25 < gmtime(time()).tm_min < 35:
            await asyncio.sleep(10)

        # prepare and send the 30 minute before warning
        desc = ":exclamation: PvP will reset in about 30 minutes"
        embed = discord.Embed(description=desc, color=discord.Colour(0xb736b0))

        await client.send_message(channel, embed=embed)

        # wait the 30 minutes
        await asyncio.sleep(30*60)

        # prepare and send the reset message
        desc = ":exclamation: PvP is reseted"
        embed = discord.Embed(description=desc, color=discord.Colour(0xff0000))
        await client.send_message(channel, embed=embed)

        # wait 12 hours minus 30 minutes for the warning
        await asyncio.sleep((first*60*60) - 30*60)


"""
quests is a function that writes into a channel whenever the daily, weekly or monthly quests reset

It takes the client object as the argument

never returns
"""
async def quests(client):
    # Calculate the time difference and when to send the first message
    first = (19 - gmtime(time()).tm_hour) % 12

    # Find the channel where to send the reminder
    kancolle_stuff_id = '242858060224135168'
    channel = await get_channel_by_id(client, kancolle_stuff_id)

    # Check if the channel was found
    if channel is None:
        print("Couldn't find kancolle stuff!")
        return

    # Debug Print
    print("I should remind in:", first, 'hours and', (30-gmtime(time()).tm_min) % 60, 'minutes in', channel.name, 'for quests.')


    # Wait a bit to get approximatly the right time to send
    while 25 < gmtime(time()).tm_min < 35 or (19 - gmtime(time()).tm_hour) % 12 != 0:
        await asyncio.sleep(30)

    # reset the variable so we always wait ~23.5 hours
    first = 24

    while True:
        quests = 'daily'
        # prevent timedrift due to different clocks also to prevent missing the time completly have
        # a +-5 minutes timewindow
        while 25 < gmtime(time()).tm_min < 35:
            await asyncio.sleep(10)

        # Check if today is a monday and the weekly quests reset
        if gmtime(time()).tm_wday == 0:
            quests = 'weekly and ' + quests

        # Check if today is a first of a month and the monthly quests reset
        if gmtime(time()).tm_mday == 1:
            # Check if today is also a monday to make the print a bit prittier
            if quests == 'daily':
                quests = 'monthly and ' + quests
            else:
                quests = 'monthly, ' + quests


        # prepare and send the 30 minute before warning
        desc = ":exclamation: {} quests will reset in about 30 minutes".format(quests)
        embed = discord.Embed(description=desc, color=discord.Colour(0xb736b0))

        await client.send_message(channel, embed=embed)

        # wait the 30 minutes
        await asyncio.sleep(30*60)

        # prepare and send the reset message
        desc = ":exclamation: {} quests is reseted".format(quests)
        embed = discord.Embed(description=desc, color=discord.Colour(0xff0000))
        await client.send_message(channel, embed=embed)

        # wait 24 hours minus 30 minutes for the warning
        await asyncio.sleep((first*60*60) - 30*60)