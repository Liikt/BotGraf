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
from functions.secretary import *
from functions.zalgo import *
from time import gmtime, time, sleep
from subprocess import Popen


ROOT_DIR = os.getcwd()
name = "Graf Zeppelin"
game = "@{} help for help".format(name)
client = discord.Client()
secr, lines, admirals = {}, {}, {}


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
async def on_ready():
    global secr
    global admirals
    global lines
    await client.edit_profile(username=name)
    reloadall()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=discord.Game(name=game))
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
                #elif m.split()[0] == "debug":
                #    await debug(client, message)
                elif m.split()[0] == "xkcd":
                    await xkcd(client, message)
                elif m.split()[0] == "zalgo":
                    await zalgo(client, message)
                elif m.split()[0] == "secretary":
                    await menu(client, message, admirals, secr)
                    reloadall()
                else:
                    await client.send_message(message.channel, random.choice(lines[name]))
        if "friendship is magic" in message.content.lower():
            embeded = discord.Embed(description="AND MAGIC IS HERESY!", color=discord.Colour(0x8958A7))
            embeded.set_image(url="https://cdn.discordapp.com/attachments/285537911414325249/291701362218237962/MagicIsHeresy.jpg")
            await client.send_message(message.channel, embed=embeded)
        if "gib" in message.content.lower():
            await client.send_message(message.channel, ":flag_gr:")
        if "MURICA" in message.content:
            await client.send_message(message.channel, ":flag_us:")

client.run(key)
