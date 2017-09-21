#!/usr/bin/env python3

import discord
import asyncio
import os
from utils.secret import key


ROOT_DIR = os.getcwd()
name = "Ooyodo"
game = "@{} help for help".format(name)
client = discord.Client()
starttime = 0


@client.event
async def on_ready():
    global starttime
    await client.edit_profile(username=name)
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=discord.Game(name=game))
    print("Changed status to '" + game + "'")
    print('------')

@client.event
async def on_message(message):
    pass

client.run(key)
