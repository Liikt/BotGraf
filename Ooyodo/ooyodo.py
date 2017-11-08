#!/usr/bin/env python3

import discord
import asyncio
import os

from utils.secret import key
from utils.utils import async_concurrent, setup
from functions.reminder import pvp, quests


# Global vars
name = "Ooyodo"
game = "Nothing"
client = discord.Client()


"""
on_ready is a function that get's called, when the client has logged in and is ready. Then it set's
up the client by chaning the name and changing the current "game". At the end it starts all the
functions that have to run concurrent.

Doesn't take any parameters
"""
@client.event
async def on_ready():
    # Run the setup function
    await setup(client, name, game)

    # Start the reminder functions
    asyncio.ensure_future(async_concurrent(quests, client))
    asyncio.ensure_future(async_concurrent(pvp, client))


"""
on_message is a function that will be used to handle commands. Currently there are none so this
function does nothing.

Takes the current message as a parameter
"""
@client.event
async def on_message(message):
    pass

client.run(key)
