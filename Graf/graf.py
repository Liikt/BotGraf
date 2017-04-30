#!/usr/bin/env python3

import discord
import asyncio
import requests
import yaml
import random
import os

from time import gmtime, time, sleep
from subprocess import Popen

from utils.utils import *
from utils.secret import key
from functions.other import *
#from functions.CaH import *
from functions.secretary import *


ROOT_DIR = os.getcwd()
name = "Graf Zeppelin"
game = "@{} help for help".format(name)
client = discord.Client()
secr, lines, admirals = {}, {}, {}
starttime = time()


def reloadsecr():
    global secr
    try:
        with open(ROOT_DIR + os.sep + "config" + os.sep + "secretary.yml", "r") as f:
            secr = yaml.load(f)
    except Exception as e:
        print(e)
        with open(ROOT_DIR + os.sep + "config" + os.sep + "secretary.yml", "w"):
            pass

def reloadlines():
    global lines
    try:
        with open(ROOT_DIR + os.sep + "config" + os.sep + "lines.yml", "r") as f:
            lines = yaml.load(f)
    except Exception as e:
        print(e)
        with open(ROOT_DIR + os.sep + "config" + os.sep + "lines.yml", "w"):
            pass

def reloadadmirals():
    global admirals
    try:
        with open(ROOT_DIR + os.sep + "config" + os.sep + "admirals.yml", "r") as f:
            admirals = yaml.load(f)
    except Exception as e:
        print(e)
        with open(ROOT_DIR + os.sep + "config" + os.sep + "admirals.yml", "w"):
            pass

def reloadall():
    global secr
    global admirals
    global lines
    reloadsecr()
    reloadlines()
    reloadadmirals()


@client.event
async def on_voice_state_update(old, new):
    await voice_update(client, old, new)

@client.event
async def on_ready():
    global secr
    global admirals
    global lines
    global starttime

    await client.edit_profile(username=name)
    reloadall()
    
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    
    while True:
        try:
            await client.change_presence(game=discord.Game(name=game))
            break
        except:
            sleep(1)

    print("Changed status to '" + game + "'")
    print('------')
    
    await send_hourlies(client)

@client.event
async def on_message(message):
    global secr
    global admirals
    global lines

    if not message.channel.is_private:
        if client.user in message.mentions:
            m = " ".join(message.content.split()[1:])
            
            if len(m) >= 1:
                if m.split()[0] == "eval":
                    await evaluate(client, message)
                
                elif m.split()[0] == "help":
                    await help(client, message)
                
                elif m.split()[0] == "xkcd":
                    await xkcd(client, message)
                
                elif m.split()[0].lower() == "secretary":
                    await menu(client, message, admirals, secr)
                    reloadall()
                
                # elif m.split()[0] == "CaH":
                #     found = False
                #     correct_role = False
                    
                #     for role in message.author.roles:
                #         if role.name in ["Card Master", "Senpai", "Overlord"]:
                #             correct_role = True
                #             break

                #     if not correct_role:
                #         await client.send_message(message.channel, "<@"+message.author.id+"> I'm sorry but you can't start a CaH game.")
                #         break

                #     for c in message.server.channels:
                #         if c.name == "CaH" and c.type == discord.ChannelType.voice:
                #             if len(c.voice_members) > 2:
                #                 await client.send_message(message.channel, "I found a good Channel")
                #                 found = True
                #             else:
                #                 await client.send_message(message.channel, "I found a good Channel but there are to few people in it")
                #         elif c.name == "CaH":
                #             await client.send_message(message.channel, "I found a CaH Chanel but that sadly isn't a voice Channel")
                    
                #     if found:
                #         await cah_menu(client, message)

                elif m.split()[0] == "uptime":
                    cur = time()
                    hour = str(gmtime(cur-starttime).tm_hour)
                    minute = str(gmtime(cur-starttime).tm_min)
                    await client.send_message(message.channel, "<@"+message.author.id+"> I have been alive for " \
                     + hour + " hours and " + minute + " minutes.")
                
                #elif m.split()[0] == "debug":
                #    await debug_secr(client, message)
                
                else:
                    await client.send_message(message.channel, random.choice(lines[name]))

client.run(key)
