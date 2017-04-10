import random
import discord

zalgo_up = [
    '\u030d', '\u030e', '\u0304', '\u0305',
    '\u033f', '\u0311', '\u0306', '\u0310',
    '\u0352', '\u0357', '\u0351', '\u0307',
    '\u0308', '\u030a', '\u0342', '\u0343',
    '\u0344', '\u034a', '\u034b', '\u034c',
    '\u0303', '\u0302', '\u030c', '\u0350',
    '\u0300', '\u0301', '\u030b', '\u030f',
    '\u0312', '\u0313', '\u0314', '\u033d',
    '\u0309', '\u0363', '\u0364', '\u0365',
    '\u0366', '\u0367', '\u0368', '\u0369',
    '\u036a', '\u036b', '\u036c', '\u036d',
    '\u036e', '\u036f', '\u033e', '\u035b',
    '\u0346', '\u031a'
]

zalgo_down = [
    '\u0316', '\u0317', '\u0318', '\u0319',
    '\u031c', '\u031d', '\u031e', '\u031f',
    '\u0320', '\u0324', '\u0325', '\u0326',
    '\u0329', '\u032a', '\u032b', '\u032c',
    '\u032d', '\u032e', '\u032f', '\u0330',
    '\u0331', '\u0332', '\u0333', '\u0339',
    '\u033a', '\u033b', '\u033c', '\u0345',
    '\u0347', '\u0348', '\u0349', '\u034d',
    '\u034e', '\u0353', '\u0354', '\u0355',
    '\u0356', '\u0359', '\u035a', '\u0323'
]
    
zalgo_mid = [
    '\u0315', '\u031b', '\u0340', '\u0341',
    '\u0358', '\u0321', '\u0322', '\u0327',
    '\u0328', '\u0334', '\u0335', '\u0336',
    '\u034f', '\u035c', '\u035d', '\u035e',
    '\u035f', '\u0360', '\u0362', '\u0338',
    '\u0337', '\u0361', '\u0489' 
]

def zalgo_char(c):
    return c in zalgo_mid or c in zalgo_down or c in zalgo_up

async def zalgo(client, message):
    new_text = ""
    text = " ".join(message.content.split()[4:])
    up = False
    down = False
    mid = False
    high = 0
    low = 0

    if len(message.content.split()[2]) != 1 or message.content.split()[2] not in "123":
        await client.send_message(message.channel, "<@"+message.author.id+"> Please use 1 for few, 2 for more and 3 for a lot of symbols.")
        return

    cancer_level = int(message.content.split()[2])
    modes = message.content.split()[3]
    if len(modes) not in range(1,4) or len(modes.replace("u", "").replace("d", "").replace("m", "")) != 0:
        await client.send_message(message.channel, "<@"+message.author.id+"> Please use 'u' to add on top, 'd' to add on the bottom and 'm' to add in the middle.")
        return    

    if 'u' in modes:
        up = True
    if 'd' in modes:
        down = True
    if 'm' in modes:
        mid = True

    for x in text:

        if zalgo_char(x):
            continue
        new_text += x

        if cancer_level == 1:
            num_up = random.randint(0,8)
            num_mid = random.randint(0,2)
            num_down = random.randint(0,8)
        elif cancer_level == 2:
            num_up = random.randint(0,16)//2+1
            num_mid = random.randint(0,6)//2
            num_down = random.randint(0,16)//2+1
        elif cancer_level == 3:
            num_up = random.randint(0,64)//4+3
            num_mid = random.randint(0,16)//4+3
            num_down = random.randint(0,64)//4+3

        if down:
            for y in range(num_down):
                new_text += random.choice(zalgo_down)
        if mid:
            for y in range(num_mid):
                new_text += random.choice(zalgo_mid)
        if up:
            for y in range(num_up):
                new_text += random.choice(zalgo_down)

        if len(new_text) >= 2000:
            new_text = new_text[:2000]
            break
    await client.send_message(message.channel, "<@"+message.author.id+"> "+ new_text)
