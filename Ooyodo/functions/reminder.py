import discord
import asyncio
import os
from time import gmtime, time, sleep

from utils.utils import get_channel_by_id


"""
This function reminds us every 12 hours to do our pvps
It takes the client as an argument to be able to send messages
"""
async def pvp(client):
    first = (17 - gmtime(time()).tm_hour) % 12
    kancolle_stuff_id = '242858060224135168'
    channel = await get_channel_by_id(client, kancolle_stuff_id)

    if channel is None:
        print('Couldn\'t find kancolle stuff!')
        return

    # Debug Print
    print("I should remind in:", first, 'hours and', 30 - gmtime(time()).tm_min % 60, 'minutes in', channel.name, 'for pvp.')



    # Convert the hours into seconds and subtract 30*60 seconds, so half an hour
    # for advanced warning

    while gmtime(time()).tm_min != 30 or (17 - gmtime(time()).tm_hour) % 12 != 0:
        #print('Sleeping for another', (17 - gmtime(time()).tm_hour) % 12, 'hours and', (30 - gmtime(time()).tm_min) % 60, 'minutes')
        await asyncio.sleep(60)

    first = 12

    while True:
        # prevent timedrift due to different clocks
        while gmtime(time()).tm_min != 30:
            await asyncio.sleep(10)

        # prepare and send the 30 minute before warning
        embed = discord.Embed(description=":exclamation: PvP will reset in about 30 minutes", color=discord.Colour(0xb736b0))
        await client.send_message(channel, embed=embed)

        # wait the 30 minutes 
        await asyncio.sleep(30*60)

        # prepare and send the reset message
        embed = discord.Embed(description=":exclamation: PvP is reseted", color=discord.Colour(0xff0000))
        await client.send_message(channel, embed=embed)

        # wait 12 hours minus 30 minutes for the warning
        await asyncio.sleep((first*60*60)-30*60)
