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
from functions.shitpost import *
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
                elif m.split()[0] == "uptime":
                    cur = time()
                    hour = str(gmtime(cur-starttime).tm_hour)
                    minute = str(gmtime(cur-starttime).tm_min)
                    await client.send_message(message.channel, "<@"+message.author.id+"> I have been alive for " \
                     + hour + " hours and " + minute + " minutes.")
                else:
                    await client.send_message(message.channel, "I AM LIVING CANCER!")
        await check_shitpost(client, message)
    # elif message.author.id == '194178693113839618':
    #     if message.content == "delete":
    #         async for mes in client.logs_from(message.channel):
    #             try:
    #                 await client.delete_message(mes)
    #             except:
    #                 pass
    #     else:
    #         print("\n".join([x["url"] for x in message.attachments]))
client.run(key)
