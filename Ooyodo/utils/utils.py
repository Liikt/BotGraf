import discord
import asyncio

from utils.logger import log


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
    log('INFO', 'setup', 'Logged in as {} with id {}'.format(client.user.name, client.user.id))
    log('INFO', 'setup', "Changed status to '{}'".format(game))


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
            log('ERROR', function.__name__, str(e).split('\n')[-1])


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