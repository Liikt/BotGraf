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

    # Find the channels where to send the reminder
    channel_ids = ['242858060224135168']
    channels = await get_channel_by_ids(client, channel_ids)

    # Check if the all the channels were found
    if len(channels) != len(channel_ids):
        for channelname, _, id in channels:
            if id not in channel_ids:
                log('WARN', 'pvp', "Couldn't find channel with channelname: and id: {}"\
                    .format(channelname, id))

    # Debug log
    log('INFO', 'pvp', 'I should remind in: {} hours and {} minutes for pvp.'\
            .format(first, (30-gmtime(time()).tm_min) % 60))

    # Wait a bit to get approximatly the right time to send
    while not 28 < gmtime(time()).tm_min < 31 or (17 - gmtime(time()).tm_hour) % 12 != 0:
        await asyncio.sleep(30)

    while True:
        # prevent timedrift due to different clocks also to prevent missing the time completly have
        # a +-1 minute timewindow
        while 21 < gmtime(time()).tm_min < 31:
            await asyncio.sleep(10)

        # prepare and send the 30 minute before warning
        for _, channel, _ in channels:
            desc = ":exclamation: Admiral, PvP's will reset in about 30 minutes"
            embed = discord.Embed(description=desc, color=discord.Colour(0xffff00))

            await client.send_message(channel, embed=embed)

        # wait the 30 minutes
        await asyncio.sleep(30*60)

        # prepare and send the reset message
        for channelname, channel, _ in channels:
            desc = ":exclamation: Admiral, PvP's have reset."
            embed = discord.Embed(description=desc, color=discord.Colour(0x00ff00))
            await client.send_message(channel, embed=embed)
            log('INFO', 'pvp', 'Sending reminder for pvp in {}'.format(channelname))

        # wait 12 hours minus 30 minutes for the warning
        await asyncio.sleep((12*60*60) - 30*60)


"""
quests is a function that writes into a channel whenever the daily, weekly or monthly quests reset

It takes the client object as the argument

never returns
"""
async def quests(client):
    # Calculate the time difference and when to send the first message
    first = (5 + gmtime(time()).tm_hour) % 24

    # Find the channels where to send the reminder
    channel_ids = ['242858060224135168']
    channels = await get_channel_by_ids(client, channel_ids)

    # Check if the all the channels were found
    if len(channels) != len(channel_ids):
        for channelname, _, id in channels:
            if id not in channel_ids:
                log('WARN', 'quests', "Couldn't find channel with channelname: and id: {}"\
                    .format(channelname, id))

    # Debug log
    log('INFO', 'quests', 'I should remind in: {} hours and {} minutes for quests.'\
            .format(first, (30-gmtime(time()).tm_min) % 60))

    # Wait a bit to get approximatly the right time to send
    while not 28 < gmtime(time()).tm_min < 32 or (5 + gmtime(time()).tm_hour) % 24 != 0:
        await asyncio.sleep(30)

    while True:
        quests = 'daily'
        # prevent timedrift due to different clocks also to prevent missing the time completly have
        # a +-1 minute timewindow
        while 28 < gmtime(time()).tm_min < 32:
            await asyncio.sleep(10)

        # Check if today is a monday and the weekly quests reset
        if gmtime(time()).tm_wday == 6:
            quests = 'weekly and ' + quests

        # Check if today the last day of a month with 31 days or the last day of a month with 30 days
        if (gmtime(time()).tm_mon in [1, 3, 5, 7, 8, 10, 12] and gmtime(time()).tm_mday == 31) or\
           (gmtime(time()).tm_mon not in [1, 3, 5, 7, 8, 10, 12] and gmtime(time()).tm_mday == 30):
            # Check if today is also a monday to make the print a bit prittier
            if quests == 'daily':
                quests = 'monthly and ' + quests
            else:
                quests = 'monthly, ' + quests

            # Check if the quarterly quests are also resetting
            if gmtime(time()).tm_mon in [3, 6, 9, 12]:
                quests = 'quarterly, ' + quests

        # TODO: Handle february and leap years
        # Check if it's the last day of the month or a week before
        if gmtime(time()).tm_mday in [23, 29]:
            # Set the placeholders
            temp = 'monthly'
            remaining = 'week'

            # Check if the quarterlys also are resetting soon
            if gmtime(time()).tm_mon in [2, 5, 8, 11]:
                # Add quarterlies to the placeholder
                temp = 'quarterly and ' + temp

            # Check if it's actually the last day of the month
            if gmtime(time()).tm_mday == 29:
                # If so change the placeholder
                remaining = 'or two days'

            # Send the message for the week or day before warning
            for channelname, channel, _ in channels:
                desc = ":exclamation:  Admiral, {} quests will reset in about one {}".format(temp, remaining)
                embed = discord.Embed(description=desc, color=discord.Colour(0xffff00))
                await client.send_message(channel, embed=embed)
                log('INFO', 'quests', 'Sending reminder for {} in one {} in {}'\
                    .format(temp, remaining, channelname))

        # prepare and send the 30 minute before warning
        for _, channel, _ in channels:
            desc = ":exclamation:  Admiral, {} quests will reset in about 30 minutes".format(quests)
            embed = discord.Embed(description=desc, color=discord.Colour(0xffff00))
            await client.send_message(channel, embed=embed)

        # wait the 30 minutes
        await asyncio.sleep(30*60)

        # prepare and send the reset message
        for channelname, channel, _ in channels:
            desc = ":exclamation:  Admiral, {} quests have reset".format(quests)
            embed = discord.Embed(description=desc, color=discord.Colour(0x00ff00))
            await client.send_message(channel, embed=embed)
            log('INFO', 'quests', 'Sending reminder for {} quests in {}'.format(quests, channelname))


        # wait 24 hours minus 30 minutes for the warning
        await asyncio.sleep((24*60*60) - 30*60)
