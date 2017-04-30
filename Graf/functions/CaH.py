import discord
import asyncio
import requests
import yaml
import random
import os

from time import gmtime, time, sleep
from subprocess import Popen

from utils.utils import *


players = {}
running = False


async def voice_update(client, old, new):
	if not 

async def cah_menu(client, message):
	if message.split()[2] == "start" and running:
		await client.send_message(message.channel, "<@"+message.author.id+"> There is a CaH game running already.")
		return

	elif message.split()[2] == "start" and not running:
		await client.send_message(message.channel, "<@"+message.author.id+"> Starting a new CaH game.")


async def cah(client, message):

