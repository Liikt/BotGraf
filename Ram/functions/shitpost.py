import discord
import yaml
from random import choice

def load_desire():
    g = {}
    
    with open("Pictures/desire.yml") as f:
        g = yaml.load(f)
    
    return g

async def check_shitpost(client, message):
    desire = load_desire()

    if "friendship is magic" in message.content.lower():
        embeded = discord.Embed(description="AND MAGIC IS HERESY!", color=discord.Colour(0x8958A7))
        embeded.set_image(url="https://cdn.discordapp.com/attachments/285537911414325249/291701362218237962/MagicIsHeresy.jpg")
        await client.send_message(message.channel, embed=embeded)

    if "reee" in message.content.lower():
        embeded = discord.Embed(description="REEEEEEEEE", color=discord.Colour(0xFF0000))
        embeded.set_image(url="http://i1.kym-cdn.com/entries/icons/original/000/017/318/angry_pepe.jpg")
        await client.send_message(message.channel, embed=embeded)    
    
    if "dew it" in message.content.lower() or "do it" in message.content.lower():
        embeded = discord.Embed()
        embeded.set_image(url="https://cdn.discordapp.com/attachments/302709996041273344/302713643106304000/dew_it.jpg")
        await client.send_message(message.channel, embed=embeded) 

    if "nuu" in message.content.lower():
        await client.send_message(message.channel, ":flag_de:") 
    
    if "MURICA" in message.content:
        await client.send_message(message.channel, ":flag_us:")
    
    if "FUCK YEAH" in message.content:
        await client.send_message(message.channel, ":eagle:")
    
    if "gib" in message.content.lower():
        await client.send_message(message.channel, ":flag_gr:")
    
    if "balans" in message.content.lower():
        await client.send_message(message.channel, ":flag_ru:")
    
    if "your mom" in message.content.lower():
        await client.send_message(message.channel, "NO YOUR MOM!") 

    if "dumb" in message.content.lower():
        await client.send_message(message.channel, "NO YOU'RE DUMB!")

    if "desire" in message.content.lower():
        link = choice(desire)
        embeded = discord.Embed(description="OH DESIRE", color=discord.Colour(0xEB8D43))
        embeded.set_image(url=link)
        await client.send_message(message.channel, embed=embeded)