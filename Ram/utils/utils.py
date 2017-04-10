import discord
import asyncio
import requests
import yaml
import random
import os
from time import gmtime, time, sleep
                    

async def delete_last_message(client, message, string=""):
    async for mes in client.logs_from(message.channel):
        if mes.content.startswith("<@"+message.author.id+">") and mes.author == client.user:
            await client.delete_message(mes)
            if len(string) > 0:
                await client.send_message(message.channel, string)
            break

def check(string):
    try:
        int(string)
        return True
    except:
        return False