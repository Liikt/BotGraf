import discord
import asyncio
import requests
import yaml
import random
import os
from syslog import syslog
from utils.utils import *
from time import gmtime, time, sleep


name = "Graf Zeppelin"
ROOT_DIR = os.getcwd()
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

async def send_hourlies(client):
    global secr
    global admirals
    global lines

    first = 60-gmtime(time()).tm_min
    t = gmtime(time()).tm_hour

    syslog("I'm going to send the first batch in " + str(first) + " minutes!")
    print("Sending in", first, "minutes") 
    await asyncio.sleep(first*60)
    
    while t == gmtime(time()).tm_hour:
        await asyncio.sleep(1)
    
    while True:
        reloadall()
        visited = []
        
        for admiral in admirals.keys():
            for s in client.servers:
                m = s.get_member(admiral)
    
                if admiral not in visited and admirals[admiral]["Enabled"] == True and not m is None \
                    and (m.status == discord.Status.online or m.status == discord.Status.idle):
                    
                    visited.append(admiral)
                    t = (int(admirals[admiral]["Offset"].split(":")[0])+gmtime(time()).tm_hour)%24
                    user = s.get_member(admiral)

                    if t == 0:
                        await clear_daily_chat(client, user.id)

                    if admirals[admiral]["Secretary"] != "":
                        embeded = discord.Embed(color=discord.Colour(0xe67e22))
                        embeded.set_image(url=admirals[admiral]["Secretary"])
    
                        try:
                            await client.send_message(user, embed=embeded)
                        except:
                            embeded = discord.Embed(description="I somehow couldn't load your picture!", color=discord.Colour(0xFF0000))
                            await client.send_message(user, embed=embeded)

                    embeded = discord.Embed(description=secr[admirals[admiral]["Shipfu"]][t], color=discord.Colour(0xe67e22))
                    await client.send_message(user, embed=embeded)

                    syslog(str(m) +  " -> " + admirals[admiral]["Shipfu"] + " at " + str(t) + " => " + secr[admirals[admiral]["Shipfu"]][t])
    
        await asyncio.sleep(60*60)

async def addsecretary(client, message, admirals, secr):
    if message.author.id in list(admirals.keys()):
        await client.send_message(message.channel, "<@"+message.author.id+"> You currently have a secretary assigned!")
        return

    client_id = message.author.id
    
    await delete_last_message(client, message, "<@"+message.author.id+"> \n```What is your current time?\nThis is needed to determine what hourly notification is appropiate.\
    \n(Please use the format hh:mm so i.e. 7:07pm => 19:07)\
    \n\nType abort to exit```")

    msg = await client.wait_for_message(channel=message.channel,author=message.author)

    if msg.content.lower() == "abort":
        await delete_last_message(client, message)
        return 

    while len(msg.content) != 5 or ":" not in msg.content or len(msg.content.split(":")) != 2 or not check(msg.content.split(":")[0]) or not check(msg.content.split(":")[1]) \
        or int(msg.content.split(":")[0]) not in range(24) or int(msg.content.split(":")[1]) not in range(60):

        await delete_last_message(client, message, "<@"+message.author.id+"> \n```Please use a real time or/or the format hh:mm (5:05pm => 15:05)\
            \n\nType abort to exit```")
        msg = await client.wait_for_message(channel=message.channel,author=message.author)
            
        if msg.content.lower() == "abort":
            await delete_last_message(client, message)
            return

    cur_time = gmtime(time())
        
    #their - mine = offset -> 06:00 - 00:00 = 06:00 ahead
    offset = ":".join([str(int(msg.content.split(":")[0])-cur_time.tm_hour), str(int(msg.content.split(":")[1])-cur_time.tm_min)])
    list_count = 0
    shiplist = sorted(secr.keys())
    found = False
    tmp_list = []

    while not found:
        start = list_count*10
        end = min(len(shiplist[start:])+start, start+10)
        tmp_list = shiplist[start:end]
        pagination = ""

        if end != len(shiplist[start:])+start:
            pagination += "\n\tN. Next Page"
        if start != 0:
            pagination += "\n\tB. Page Back"

        await delete_last_message(client, message, "<@"+message.author.id+"> \n```Please choose one of the following shipfus:\n\t" \
            + "\n\t".join([str(x+1) + ". " + y for x,y in enumerate(tmp_list)]) + \
            pagination + "\n\nType abort to exit```")

        msg = await client.wait_for_message(channel=message.channel,author=message.author)

        if msg.content.lower() == "abort":
            await delete_last_message(client, message)
            return

        while msg.content.upper() != "N" and msg.content.upper() != "B" and not check(msg.content) and int(msg.content) - 1 not in range(len(tmp_list)):

            await delete_last_message(client, message, "<@"+message.author.id+"> \n```Please choose one of the following shipfus:\n\t" \
                + "\n\t".join([str(x+1) + ". " + y for x,y in enumerate(tmp_list)]) + "\
                \n\t9. Next Page\n\t10. Page Back\n\nType abort to exit```")

            msg = await client.wait_for_message(channel=message.channel,author=message.author)

            if msg.content.lower() == "abort":
                await delete_last_message(client, message)
                return 
        
        if msg.content.upper() == "N":
            list_count += 1
        elif msg.content.upper() == "B":
            list_count -= 1
        elif int(msg.content)-1 in range(10):
            found = True
        else:
            await client.send_message(message.channel, "<@"+message.author.id+"> You just fucked up! :C")
            print(list_count, tmp_list, shiplist, msg.content)
            
    
    await client.send_message(message.channel, "<@"+message.author.id+"> ```If you want to set (or change in the future) a picture for your secretary message @Liikt.\nType anything to continue.```")
    
    try:
        await client.wait_for_message(timeout=5, channel=message.channel,author=message.author)
    except asyncio.TimeoutError:
        pass

    shipfu = tmp_list[int(msg.content)-1]
    admirals[client_id] = dict()
    admirals[client_id]["Offset"] = offset
    admirals[client_id]["Shipfu"] = shipfu
    admirals[client_id]["Enabled"] = True
    admirals[client_id]["Secretary"] = ""

    admirals_file = open(ROOT_DIR + os.sep + "config" + os.sep + "admirals.yml", "w")
    yaml.dump(admirals, admirals_file, default_flow_style=False)
    admirals_file.close()

    await delete_last_message(client, message)
    await client.send_message(message.channel, "<@"+message.author.id+"> I assigned " + shipfu + " as your secretary ship.")

    return

async def changesettings(client, message, admirals, secr):
    client_id = message.author.id
    if not message.author.id in list(admirals.keys()):
        await client.send_message(message.channel, "<@"+message.author.id+"> You currently don't have a secretary assigned!")
        return
    
    info = admirals[message.author.id]
    enabled = "Enable notifcations" if info["Enabled"] == False else "Disable notifications"

    await client.send_message(message.channel, "<@"+message.author.id+"> \n```What do you want to change?\
        \n\t1. Change the secretary\
        \n\t2. Change the current time\
        \n\t3. " + enabled + "```")
    msg = await client.wait_for_message(channel=message.channel,author=message.author)

    while not check(msg.content) and int(msg.content)-1 not in range(3):
        await client.send_message(message.channel, "<@"+message.author.id+"> \n```Please choose one of these options:\
            \n\t1. Change the secretary\
            \n\t2. Change the current time\
            \n\t3. " + enabled + "```")

        msg = await client.wait_for_message(channel=message.channel,author=message.author)            

    await delete_last_message(client, message)
    
    if int(msg.content) == 1:
        list_count = 0
        shiplist = sorted(secr.keys())
        found = False
        tmp_list = []

        while not found:
            start = list_count*10
            end = min(len(shiplist[start:])+start, start+10)
            tmp_list = shiplist[start:end]
            pagination = ""

            if end != len(shiplist[start:])+start:
                pagination += "\n\tN. Next Page"
            if start != 0:
                pagination += "\n\tB. Page Back"

            await delete_last_message(client, message, "<@"+message.author.id+"> \n```Please choose one of the following shipfus:\n\t" \
                + "\n\t".join([str(x+1) + ". " + y for x,y in enumerate(tmp_list)]) + \
                pagination + "\n\nType abort to exit```")

            msg = await client.wait_for_message(channel=message.channel,author=message.author)

            if msg.content.lower() == "abort":
                await delete_last_message(client, message)
                return

            while msg.content.upper() != "N" and msg.content.upper() != "B" and not check(msg.content) and int(msg.content) - 1 not in range(len(tmp_list)):

                await delete_last_message(client, message, "<@"+message.author.id+"> \n```Please choose one of the following shipfus:\n\t" \
                    + "\n\t".join([str(x+1) + ". " + y for x,y in enumerate(tmp_list)]) + "\
                    \n\t9. Next Page\n\t10. Page Back\n\nType abort to exit```")

                msg = await client.wait_for_message(channel=message.channel,author=message.author)

                if msg.content.lower() == "abort":
                    await delete_last_message(client, message)
                    return 
            
            if msg.content.upper() == "N":
                list_count += 1
            elif msg.content.upper() == "B":
                list_count -= 1
            elif int(msg.content)-1 in range(10):
                found = True
            else:
                await client.send_message(message.channel, "<@"+message.author.id+"> You just fucked up! :C")
                print(list_count, tmp_list, shiplist, msg.content)

        shipfu = tmp_list[int(msg.content)-1]
        admirals[client_id]["Shipfu"] = shipfu
        admirals[client_id]["Secretary"] = ''

        admirals_file = open(ROOT_DIR + os.sep + "config" + os.sep + "admirals.yml", "w")
        yaml.dump(admirals, admirals_file, default_flow_style=False)
        admirals_file.close()

        await client.send_message(message.channel, "<@"+message.author.id+"> I assigned " + shipfu + " as your secretary ship.")

    elif int(msg.content) == 2:
        await delete_last_message(client, message, "<@"+message.author.id+"> \n```What is your current time?\nThis is needed to determine what hourly notification is appropiate.\
        \n(Please use the format hh:mm so i.e. 7:07pm => 19:07)\
        \n\nType abort to exit```")

        msg = await client.wait_for_message(channel=message.channel,author=message.author)

        if msg.content.lower() == "abort":
            await delete_last_message(client, message)
            return 

        while len(msg.content) != 5 or ":" not in msg.content or len(msg.content.split(":")) != 2 or not check(msg.content.split(":")[0]) or not check(msg.content.split(":")[1]) \
            or int(msg.content.split(":")[0]) not in range(24) or int(msg.content.split(":")[1]) not in range(60):

            await delete_last_message(client, message, "<@"+message.author.id+"> \n```Please use a real time or/or the format hh:mm (5:05pm => 15:05)\
                \n\nType abort to exit```")
            msg = await client.wait_for_message(channel=message.channel,author=message.author)
                
            if msg.content.lower() == "abort":
                await delete_last_message(client, message)
                return

        #their - mine = offset -> 06:00 - 00:00 = 06:00 ahead
        cur_time = gmtime(time())
        offset = ":".join([str(int(msg.content.split(":")[0])-cur_time.tm_hour), str(int(msg.content.split(":")[1])-cur_time.tm_min)])
        admirals[client_id]["Offset"] = offset

        admirals_file = open(ROOT_DIR + os.sep + "config" + os.sep + "admirals.yml", "w")
        yaml.dump(admirals, admirals_file, default_flow_style=False)
        admirals_file.close()

        t = (int(offset.split(":")[0])+gmtime(time()).tm_hour+1)%24
        nextline = str(t)+"00" if t > 9 else "0" + str(t) + "00"
        await client.send_message(message.channel, "<@"+message.author.id+"> You will recieve the next line at " + nextline)

    elif int(msg.content) == 3:
        admirals[client_id]["Enabled"] = admirals[client_id]["Enabled"] == False
        admirals_file = open(ROOT_DIR + os.sep + "config" + os.sep + "admirals.yml", "w")
        yaml.dump(admirals, admirals_file, default_flow_style=False)
        admirals_file.close()
        enabled = "" if admirals[client_id]["Enabled"] == True else "not "
        await client.send_message(message.channel, "<@"+message.author.id+"> You are " + enabled + "recieving notifications now.")

async def getinfo(client, message, admirals):
    if not message.author.id in list(admirals.keys()):
        await client.send_message(message.channel, "<@"+message.author.id+"> You currently don't have a secretary assigned!")
        return

    info = admirals[message.author.id]
    t = (int(info["Offset"].split(":")[0])+gmtime(time()).tm_hour+1)%24
    nextline = str(t)+"00" if t > 9 else "0" + str(t) + "00"
    enabled = "" if info["Enabled"] == True else "not "
    
    await client.send_message(message.channel, "<@"+message.author.id+"> \n```Your current information:\
        \n\tNext notification: " + nextline + ".\
        \n\tCurrent secretaryship: " + info["Shipfu"] + ".\
        \n\tYou currently are " + enabled + "recieving notifications.```")

    return

async def removesecretary(client, message, admirals):
    if not message.author.id in list(admirals.keys()):
        await client.send_message(message.channel, "<@"+message.author.id+"> You currently don't have a secretary assigned!")
        return

    try:
        del(admirals[message.author.id])
        await client.send_message(message.channel, "<@"+message.author.id+"> I successfully deassigned your secretary.")
    except:
        await client.send_message(message.channel, "<@"+message.author.id+"> I couldn't deassign your secretary. Please message @Liikt for help.")
    
    admirals_file = open(ROOT_DIR + os.sep + "config" + os.sep + "admirals.yml", "w")
    yaml.dump(admirals, admirals_file, default_flow_style=False)

    return

async def menu(client, message, admirals, secr):
    if admirals is None:
        admirals = {}

    if secr is None:
        secr = {}

    await client.send_message(message.channel, "<@"+message.author.id+"> \n```What do you want to do?\
        \n\t1. Get a new secretary\
        \n\t2. Change settings\
        \n\t3. Get info\
        \n\t4. Remove secretary\
        \n\nType abort to exit```")

    msg = await client.wait_for_message(channel=message.channel,author=message.author)
    
    if msg.content.lower() == "abort":
        await delete_last_message(client, message)
        return

    while not check(msg.content) or int(msg.content) not in range(1,5):

        await delete_last_message(client, message, "<@"+message.author.id+"> \n```You have to choose one of these options:\
            \n\t1. Get a new secretary\
            \n\t2. Change settings\
            \n\t3. Get info\
            \n\t4. Remove secretary\
            \n\nType abort to exit```")

        msg = await client.wait_for_message(channel=message.channel, author=message.author)

        if msg.content.lower() == "abort":
            await delete_last_message(client, message)
            return

    if int(msg.content) == 1:
        await addsecretary(client, message, admirals, secr)
    elif int(msg.content) == 2:
        await changesettings(client, message, admirals, secr)
    elif int(msg.content) == 3:
        await getinfo(client, message, admirals)
    elif int(msg.content) == 4:
        await removesecretary(client, message, admirals)

    return
