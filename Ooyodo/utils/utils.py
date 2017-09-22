import discord
import asyncio
import requests
import yaml
import random
import os
from time import gmtime, time, sleep


"""
setup is a function that sets up the client and changes the given information.

It takes the object of the client that just started, the name and the game which have to be applied
as an argument

returns nothing
"""
async def setup(client, name, game):
    # Change the information for the client
    await client.edit_profile(username=name)
    await client.change_presence(game=discord.Game(name=game))

    # Log the current state
    # TODO: write an actual logger
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print("Changed status to '" + game + "'")
    print('------')


"""
async_concurrent takes an asyncronous function and executes it concurrently. It
also yields the exceptions and starts the function again.

It takes the function that has to be executed concurrently and the client object
as a parameter

never returns
"""
@asyncio.coroutine
def async_concurrent(function, client):

    # Infinite loop to restart a function that threw an error
    while True:
        try:
            # Yield from the function in case an error was thrown
            yield from function(client)
        except Exception as e:
            # Catch the error and log it
            # TODO: write an actual logger that logs into a file
            print('Got an exception in', function.__name__)


"""
get_channel_by_id will search through every channel in every server to find the
channel with the given id.

It takes the client object and the id for the channel to search for

It returns either the channelobject or None if no channel was found
"""
async def get_channel_by_id(client, id):

    # Iterate over every Server the client is in (for now just Arlios' server)
    for s in client.servers:

        # Iterate over every channel in the current server
        for c in s.channels:

            # Find the channel with the given id
            if c.id == id:
                return c

    # Return None if no channel was found with that id
    return None