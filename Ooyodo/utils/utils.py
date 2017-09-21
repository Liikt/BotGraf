import discord
import asyncio
import requests
import yaml
import random
import os
from time import gmtime, time, sleep
                    

async def get_channel_by_id(client, id):
    for s in client.servers:
        for c in s.channels:
            if c.id == id:
                return c
    return None