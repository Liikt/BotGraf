#!/usr/bin/env python3

import discord
import asyncio
import requests
import yaml
import random
import os
from utils.utils import *
from utils.secret import key
from functions.other import *
from functions.zalgo import *
from time import gmtime, time, sleep
from subprocess import Popen


ROOT_DIR = os.getcwd()
name = "Ram"
game = "@{} help for help".format(name)
client = discord.Client()

@client.event
async def on_ready():
    await client.edit_profile(username=name)
    reloadall()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=discord.Game(name=game))
    print("Changed status to '" + game + "'")
    print('------')

@client.event
async def on_message(message):
    if not message.channel.is_private:
        if client.user in message.mentions:
            m = " ".join(message.content.split()[1:])
            if len(m) >= 1:
                if m.split()[0] == "help":
                    await help(client, message)
                #elif m.split()[0] == "debug":
                #    await debug(client, message)
                elif m.split()[0] == "zalgo":
                    await zalgo(client, message)
                else:
                    await client.send_message(message.channel, "I AM LIVING CANCER!")
        if "friendship is magic" in message.content.lower():
            embeded = discord.Embed(description="AND MAGIC IS HERESY!", color=discord.Colour(0x8958A7))
            embeded.set_image(url="https://cdn.discordapp.com/attachments/285537911414325249/291701362218237962/MagicIsHeresy.jpg")
            await client.send_message(message.channel, embed=embeded)
        if "nuu" inmessage.content.lower():
            await client.send_message(message.channel, ":flag_de:") 
        if "MURICA" in message.content:
            await client.send_message(message.channel, ":flag_us:")
        if "FUCK YEAH" in message.content:
            await client.send_message(message.channel, ":eagle:")
        if "gib" in message.content.lower():
            await client.send_message(message.channel, ":flag_gr:")

client.run(key)
