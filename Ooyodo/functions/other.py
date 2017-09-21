import discord
import asyncio
import requests
import yaml
import random
import os
import syslog
from time import gmtime, time, sleep

name = "Ram"

async def debug(client, message):
    m = "\u0411\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e\u0435 \u0418\u0437\u0432\u043b\u0435\u0447\u0435\u043d\u0438\u0435"
    await client.send_message(message.channel, m)


async def help(client, message):
    await client.send_message(message.channel, "<@"+message.author.id+"> \n```To use my commands you have to ping me and give me an order. \
        \nCurrent things I can do:\n\tzalgo <cancerlevel> <mode>-> This zalgofies a given string. Cancerlevels are 1,2,3 and modes are (u)p,(d)own,(m)iddle \n\t\t(@{} zalgo 2 udm foobarbaz)```".format(name, name, name, name))