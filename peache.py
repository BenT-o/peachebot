# Work with Python 3.7
import discord
import re
import random

TOKEN = 'NDY2NjYzNjI0MjM3MzgzNjgw.W0ZEXg.wwljGcx0KuQBfEyiWxhTRf_OO-g'

client = discord.Client()

global svmode
svmode = False

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
# <editor-fold desc="On Message...">
async def on_message(message):
    global svmode
    # <editor-fold desc="we do not want the bot to reply to itself">
    if message.author == client.user:
        return
    # </editor-fold>

    # <editor-fold desc="Hello Command">
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
    # </editor-fold>

    # <editor-fold desc="svmode Command">
    elif message.content.startswith('!svmode'):
        if svmode:
            svmode = False
            await message.channel.send("Scum & Villainy mode is now **OFF**.")
        else:
            svmode = True
            await message.channel.send("Scum & Villainy mode is now **ON**.")
    # </editor-fold>

    # <editor-fold desc="Rolling">
    elif message.content.startswith('!roll'):
        # Remove leading command and any whitespace
        fullroll = message.content.replace('!roll', '')
        fullroll = fullroll.replace(' ', '')
        if svmode and 'd6' in fullroll:
            await svroll(fullroll, message)
        # Is this a pool roll or a regular roll?
        elif ">" in fullroll or "<" in fullroll:
            await pool(fullroll, message)
        else:
            await roll(fullroll, message)
    # </editor-fold>

    # <editor-fold desc="SV Roll">
    elif message.content.startswith('!sv'):
        # Remove leading command and any whitespace
        fullroll = message.content.replace('!sv', '')
        fullroll = fullroll.replace(' ', '')
        await svroll(fullroll, message)
    # </editor-fold>

    # <editor-fold desc="Kill Command">
    elif message.content.startswith('!kill'):
        message.content = message.content.replace('!kill', '')
        message.content = message.content.replace('<', '')
        message.content = message.content.replace('@', '')
        message.content = message.content.replace('!', '')
        message.content = message.content.replace('>', '')
        userid = message.content.replace(' ', '')
        print(userid)
        user = await client.fetch_user(userid)
        await message.channel.send(user.mention, file=discord.File('funnies/grugun.png'))
    # </editor-fold>
# </editor-fold>


async def roll(fullroll, message):
    # Split into parts to be subtracted from each other
    negrollparts = re.split("[-]", fullroll)
    # Create empty array to collect all values
    fullsplit = []
    i = 0
    # For each component of negative parts, split on + and add to fullsplit array
    for x in negrollparts:
        # Need to add a '-' to the FIRST split of every rollpart other than the first
        rollpart = re.split("[+]", x)
        if i > 0:
            rollpart[0] = '-' + rollpart[0]
        for p in rollpart:
            fullsplit.append(p)
        print(fullsplit)
        i = i+1

    print(fullsplit)

    # Initialise an array to hold the rolled values
    rolledarray = []
    # Initialise rolled total
    total = 0
    mod = 0
    for x in range(fullsplit.__len__()):
        rollpart = re.split("[d]", fullsplit[x])
        print(rollpart)
        if rollpart.__len__() == 2:
            if rollpart[0].__len__() == 0:
                rollpart[0] = '1'
            if rollpart[0].startswith('-'):
                if rollpart[0].__len__() == 1:
                    rollpart[0] = '-1'
                elif int(rollpart[0]) >= 50:
                    await message.channel.send('Too many dice! My head hurts!! :weary:')
                    break
                for i in range(abs(int(rollpart[0]))):
                    roll = (random.randint(1, int(rollpart[1])))
                    rolledarray.append(roll)
                    total = total+(roll*-1)
            else:
                if int(rollpart[0]) >= 50:
                    await message.channel.send('Too many dice! My head hurts!! :weary:')
                    break
                for i in range(abs(int(rollpart[0]))):
                    roll = (random.randint(1, int(rollpart[1])))
                    rolledarray.append(roll)
                    total = total+roll
        elif rollpart.__len__() == 1:
            total = total + int(fullsplit[x])
            mod = mod + int(fullsplit[x])
        else:
            msg = 'Uh oh, something went wrong! Check your syntax and try again.'
            await message.channel.send(msg)
            break

    print(rolledarray)
    print('MOD: ' + str(mod))
    print('TOTAL: ' + str(total))
    print("-------")

    prettystring = '['
    for i in range(rolledarray.__len__()):
        if i == 0:
            prettystring = prettystring + str(rolledarray[i])
        else:
            prettystring = prettystring + ', ' + str(rolledarray[i])
    prettystring = prettystring + '] '
    if mod < 0:
        prettystring = prettystring + '- ' + str(abs(mod))
    elif mod > 0:
        prettystring = prettystring + '+ ' + str(mod)
    output = message.author.mention + ' rolled **' + str(total) + '**!\n' + prettystring
    await message.channel.send(output)


async def pool(fullroll, message):
    # split roll into parts
    targetparts = re.split("[<>]", fullroll)
    diceparts = re.split("d", targetparts[0])

    # assign parts to function
    dicecount = int(diceparts[0])
    dicesize = int(diceparts[1])
    target = int(targetparts[1])

    # create array for rolls and number of successes
    rolledarray = []
    succ = 0

    for i in range(abs(int(dicecount))):
        roll = (random.randint(1, dicesize))
        rolledarray.append(roll)

    if ">" in fullroll:
        for r in rolledarray:
            if r >= target:
                succ = succ+1
    elif "<" in fullroll:
        for r in rolledarray:
            if r <= target:
                succ = succ+1

    print(rolledarray)
    print('TARGET: ' + str(target))
    print('SUCC: ' + str(succ))
    print("-------")

    prettystring = '['
    for i in range(rolledarray.__len__()):
        if i == 0:
            prettystring = prettystring + str(rolledarray[i])
        else:
            prettystring = prettystring + ', ' + str(rolledarray[i])
    prettystring = prettystring + '] '
    output = message.author.mention + ' rolled **' + str(succ) + '** successes!\n' + prettystring
    await message.channel.send(output)


async def svroll(fullroll, message):
    # split roll into parts
    diceparts = re.split("d", fullroll)

    # assign parts to function
    dicecount = int(diceparts[0])

    # create array for rolls and number of successes
    rolledarray = []
    succ = 0
    partial = 0

    for i in range(abs(int(dicecount))):
        roll = (random.randint(1, 6))
        rolledarray.append(roll)
        if roll == 6:
            succ = succ+1
        elif roll == 4 or roll == 5:
            partial = partial+1

    rolledarray.sort(reverse=True)

    print(rolledarray)
    print("-------")

    if succ > 1:
        result = "Crit"
    elif succ == 1:
        result = "Succ"
    elif partial > 0:
        result = "Partial"
    elif partial == 0:
        result = "Fail"

    prettystring = '['
    for i in range(rolledarray.__len__()):
        if i == 0:
            if rolledarray[i] == 6:
                prettystring = prettystring + '**' + str(rolledarray[i]) + '**'
            else:
                prettystring = prettystring + str(rolledarray[i])
        else:
            if rolledarray[i] == 6:
                prettystring = prettystring + ', **' + str(rolledarray[i]) + '**'
            else:
                prettystring = prettystring + ', ' + str(rolledarray[i])

    prettystring = prettystring + ']'

#    if result == "Crit":
#        output = message.author.mention + ' rolled **A CRIT**!\n' + prettystring
#    elif result == "Succ":
#        output = message.author.mention + ' rolled a **full success**!\n' + prettystring
#    elif result == "Partial":
#        output = message.author.mention + ' rolled a **partial success**.\n' + prettystring
#    elif result == "Fail":
#        output = message.author.mention + ' *FAILED**!\n' + prettystring
    output = message.author.mention + 'rolled: \n' + prettystring
    await message.channel.send(output)



client.run(TOKEN)
