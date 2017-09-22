import discord
import asyncio
from time import gmtime, time, sleep

from utils.logger import log
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
    channel_id = '242858060224135168'
    channel = await get_channel_by_id(client, channel_id)

    # Check if the channel was found
    if channel is None:
        log('WARN', 'pvp', "Couldn't channel with id {}".format(channel_id))
        return

    # Debug log
    log('INFO', 'pvp', 'I should remind in: {} hours and {} minutes in {} for pvp.'\
            .format(first, (30-gmtime(time()).tm_min) % 60, channel.name))

    # Wait a bit to get approximatly the right time to send
    while not 21 < gmtime(time()).tm_min < 31 or (17 - gmtime(time()).tm_hour) % 12 != 0:
        await asyncio.sleep(30)

    # reset the variable so we always wait ~11.5 hours
    first = 12

    while True:
        # prevent timedrift due to different clocks also to prevent missing the time completly have
        # a +-5 minutes timewindow
        while 21 < gmtime(time()).tm_min < 31:
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
    channel_id = '242858060224135168'
    channel = await get_channel_by_id(client, channel_id)

    # Check if the channel was found
    if channel is None:
        log('WARN', 'quests', "Couldn't channel with id {}".format(channel_id))
        return

    # Debug log
    log('INFO', 'quests', 'I should remind in: {} hours and {} minutes in {} for quests.'\
            .format(first, (30-gmtime(time()).tm_min) % 60, channel.name))

    # Wait a bit to get approximatly the right time to send
    while not 21 < gmtime(time()).tm_min < 31 or (19 - gmtime(time()).tm_hour) % 12 != 0:
        await asyncio.sleep(30)

    # reset the variable so we always wait ~23.5 hours
    first = 24

    while True:
        quests = 'daily'
        # prevent timedrift due to different clocks also to prevent missing the time completly have
        # a +-5 minutes timewindow
        while 21 < gmtime(time()).tm_min < 31:
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

            # Check if the quarterly quests are also resetting
            if gmtime(time()).tm_mon in [3, 6, 9, 12]:
                quests = 'quarterly, ' + quests

        # Check if it's the last day of the month or a week before
        if gmtime(time()).tm_mday in [24, 30]:
            # Set the placeholders
            desc = 'monthly'
            remaining = 'week'

            # Check if the quarterlys also are resetting soon
            if gmtime(time()).tm_mon in [3, 6, 9, 12]:
                # Add quarterlies to the placeholder
                desc = 'quarterly and ' + desc

            # Check if it's actually the last day of the month
            if gmtime(time()).tm_mday == 30:
                # If so change the placeholder
                remaining = 'or two days'

            # Send the message for the week or day before warning
            desc = ":exclamation: {} quests will reset in about one {}".format(desc, remaining)
            embed = discord.Embed(description=desc, color=discord.Colour(0xb736b0))

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