import discord
import asyncio
import requests
import yaml
import random
import os
import syslog
from utils.utils import *
from time import gmtime, time, sleep

name = "Graf Zeppelin"

async def debug(client, message):
    await client.send_message(message.channel, " ".join(message.content.split()[2:]))

async def evaluate(client, message):
    org = "".join(message.content.split()[2:])
    tog = True
    mes = org.replace("^", "**")
    for x in mes:
        if x not in "01234567890*+-/.":
            await client.send_message(message.channel, "<@"+message.author.id+"> Please enter a valid equation!")
            tog = False
            break
    if tog:
        res = ""
        try:
            res = org + " = " + str(eval(mes))
        except Exception as e:
            res = str(e)
        syslog.syslog("Eval: " + res)
        await client.send_message(message.channel, "<@"+message.author.id+"> "+res)

async def help(client, message):
    await client.send_message(message.channel, "<@"+message.author.id+"> \n```To use my commands you have to ping me and give me an order. \
        \nCurrent things I can do:\n\teval <calculations> -> Calculate the problem! (@{} eval 9.1*5/6.5*6)\
        \n\txkcd [number] -> This will fetch a xkcd comic for you. You can choose one by providing a number. (@{} xkcd 60)\
        \n\tsecretary -> This opens the secretary menu for assigning secretaryships, etc. (@{} secretary)\
        \n\tzalgo <cancerlevel> <mode>-> This zalgofies a given string. Cancerlevels are 1,2,3 and modes are (u)p,(d)own,(m)iddle \n\t\t(@{} zalgo 2 udm foobarbaz)```".format(name, name, name, name))

async def xkcd(client, message):
    await client.send_typing(message.channel)
    addr = ""
    num = -2
    r = None
    if len(message.content.split()) > 2:
        try:
            num = max(int(message.content.split()[2]), -1)
        except:
            num = 9999999999999999999
    if num == -1:
        r = requests.get("https://xkcd.com/")
    elif num == -2:
        r = requests.get("https://c.xkcd.com/random/comic/")
    else:
        r = requests.get("https://xkcd.com/"+str(num))
    if r.status_code == 200:
        addr = r.text.split("(for hotlinking/embedding): ")[1].split("\n")[0]
    if len(addr) > 0:
        embeded = discord.Embed(description="<@"+message.author.id+">", color=discord.Colour(0x00FF00)).set_image(url=addr)
        await client.send_message(message.channel, embed=embeded)
    else:
        embeded = discord.Embed(description="<@"+message.author.id+"> I couldn't with any pictures :X", color=discord.Colour(0xFF0000))
        await client.send_message(message.channel, embed=embeded)
