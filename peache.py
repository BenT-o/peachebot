# Work with Python 3.7
import discord
import re
import random
import math

TOKEN = 'NDY2NjYzNjI0MjM3MzgzNjgw.W0ZEXg.wwljGcx0KuQBfEyiWxhTRf_OO-g'

intents = discord.Intents.all()
intents.messages = True
client = discord.Client(intents=intents)

global svmode
global chart
global gagfred
global users
svmode = False
chart = 0
gagfred = False
users = []

global regex_any_roll
global regex_roll
global regex_with_text
regex_any_roll = re.compile('\d* *#? *\d* *d *\d+ *( *[\+\-\<\>]+ *)?(?(1)\d+|) *([kd]+[hl]+)?(?(2) *\d+|)')
regex_roll = re.compile('([+-]? *\d* *d *\d+)( *[kd][hl]? *\d+)?')
regex_mod = re.compile('[\+\-] *\d+')
regex_adv = re.compile(' *[kd][hl] *\d*')

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
    global chart
    global gagfred
    global users
    global regex_any_roll
    global regex_roll
    global regex_mod

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # <editor-fold desc="Gag Fred">
    elif message.author.id == 201040951211327488 and gagfred:
        await message.delete()
    # </editor-fold>

    # <editor-fold desc="gagfred command">
    elif message.content.startswith('!gagfred'):
        if gagfred:
            gagfred = False
            print("gagfred was: ", gagfred)
            await message.channel.send("The Worm Is Unleashed. Fred no longer being gagged.")
            print("gagfred is now: ", gagfred)
        else:
            print("gagfred was: ", gagfred)
            gagfred = True
            await message.channel.send("Begone, Worm! Fred is now being gagged.")
            print("gagfred is now: ", gagfred)
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

    # <editor-fold desc="Rolling Command">
    elif message.content.startswith('!roll'):
        # Remove leading command (and any whitespace)
        fullroll = message.content.replace('!roll', '')
        # Separate roll from any trailing text
        # roll_text_split = re.split(regex_any_roll, fullroll)
        # trailing_text = roll_text_split.pop()
        # if trailing_text.__len__() <= 3:
        #     trailing_text = ''
        # fullroll = re.search(regex_any_roll, fullroll)[0]
        # fullroll = fullroll.replace(' ','')

        # How many times do we want to do this?
        if "#" in fullroll:
            # Need to make sure new fullroll doesn't include the x#
            count = int(re.split('#', fullroll)[0])
            fullroll = re.split('#', fullroll)[1]
        else:
            count = 1

        if count < 0:
            await message.channel.send('guh? I can\'t roll dice negative amount of times!')

        # Is Scum & Villainy mode on?
        elif svmode and 'd6' in fullroll:
            while count > 0:
                await svroll(fullroll, message)
                count = count-1

        # Is this a Dark Heresy roll?
        elif "<" in fullroll and "d100" in fullroll:
            while count > 0:
                await dhroll(fullroll, message)
                count = count-1

        # Is this a pool roll or a regular roll?
        elif ">" in fullroll or "<" in fullroll:
            while count > 0:
                await pool(fullroll, message)
                count = count-1
        else:
            while count > 0:
                await roll(fullroll, message)
                count = count-1
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

    # <editor-fold desc="Chart Command">
    elif message.content.startswith('!chart reset'):
        chart = 0
        print("Chart value is now: " + str(chart))

    elif message.content.startswith('!chart'):
        if chart == 0:
            await message.channel.send(file=discord.File('funnies/the_chart.png'))
        elif chart == 1:
            await message.channel.send(file=discord.File('funnies/the_chart_2.jpg'))
        elif chart == 2:
            await message.channel.send(file=discord.File('funnies/the_chart_3.gif'))
        else:
            await message.channel.send(file=discord.File('funnies/the_chart_4.jpg'))
        chart = chart+1
        print("Chart value is now: " + str(chart))
    # </editor-fold>

    elif message.content.startswith('!luck'):
        await postluck(message)

# </editor-fold>


async def roll(fullroll, message):
    # Separate components of the roll
    #print("FULLROLL = " + fullroll)
    roll_dice = re.findall(regex_roll, fullroll)
    #print("ROLL_DICE = ")
    #print(roll_dice)
    fullroll = re.sub(regex_roll, '', fullroll)
    #print("FULLROLL = " + fullroll)
    # Extract mods
    roll_mod = re.findall(regex_mod, fullroll)
    #print("ROLL MODS = ")
    #print(roll_mod)
    fullroll = re.sub(regex_mod, '', fullroll)
    #print("FULLROLL = " + fullroll)

    # Initialise the final array & total
    rolledarray = []
    total = 0
    # Prep logging of rolls for stats
    roller = message.author
    userlist = []
    for i in users:
        userlist.append(i[0])
    if roller in userlist:
        userid = userlist.index(roller)
    else:
        users.append([roller])
        userid = len(users)-1

    # Prep rolled array
    for roll in roll_dice:
        splitroll = re.split(r'd', roll[0])
        c_temp = re.sub(r' *', '', splitroll[0])
        if c_temp == '' or c_temp == '+':
            die_c = 1
        elif c_temp == '-':
            die_c = 1
        elif c_temp.startswith('+'):
            die_c = int(c_temp[1:])
        else:
            die_c = int(c_temp)
        die_s = re.sub(r' *', '', splitroll[1])
        die_s = int(die_s)

        rolls = []
        if die_c < 0:
            is_neg = True
        else:
            is_neg = False
        die_c = abs(die_c)

        # Perform Rolls
        while die_c > 0:
            if is_neg:
                x = -random.randint(1, die_s)
                total = total + x
                if x == die_s:
                    rolls.append(f'__{x}__')
                else:
                    rolls.append(x)
                users[userid].append([x, die_s])
            else:
                x = random.randint(1, die_s)
                total = total + x
                if x == die_s:
                    rolls.append(f'__{x}__')
                else:
                    rolls.append(x)
                users[userid].append([x, die_s])
            die_c = die_c - 1
        print(rolls)

        if roll[1] == "":
            rolledarray.append(str(rolls))
        else:
            advrollmod_type = roll[1][:2]
            print("advrollmod_type = " + advrollmod_type)
            advrollmod_count = int(roll[1][2:])
            print("advrollmod_count = " + str(advrollmod_count))
            sortedrolledarray = sorted(rolls)
            if advrollmod_type == 'kh':
                keep = sortedrolledarray[-advrollmod_count:]
                drop = sortedrolledarray[:-advrollmod_count]
            elif advrollmod_type == 'kl':
                keep = sortedrolledarray[:advrollmod_count]
                drop = sortedrolledarray[advrollmod_count:]
            elif advrollmod_type == 'dh':
                keep = sortedrolledarray[:-advrollmod_count]
                drop = sortedrolledarray[-advrollmod_count:]
            elif advrollmod_type == 'dl':
                keep = sortedrolledarray[advrollmod_count:]
                drop = sortedrolledarray[:advrollmod_count]
            print(drop)
            for d in drop:
                for x in rolls:
                    if x == d:
                        total = total - d
                        rolls[rolls.index(d)] = "~~" + str(rolls[rolls.index(d)]) + "~~"
                        break
            rolledarray.append(str(rolls))

    mod = 0
    for x in roll_mod:
        x = re.sub(' *', '', x)
        if x.startswith('+'):
            mod = mod + int(x[1:])
        else:
            mod = mod + int(x)
    total = total+mod

    print(rolledarray)
    #print('MOD: ' + str(mod))
    print('TOTAL: ' + str(total))
    print("-------")
    print(f'USER LIST = {users}')

    prettystring = ''
    for i in range(rolledarray.__len__()):
        if i == 0:
            prettystring = prettystring + str(rolledarray[i])
        else:
            prettystring = prettystring + ', ' + str(rolledarray[i])
    prettystring = prettystring + ' '
    if mod < 0:
        prettystring = prettystring + '- ' + str(abs(mod))
    elif mod > 0:
        prettystring = prettystring + '+ ' + str(mod)
    prettystring = re.sub(r'\'', '', prettystring)
    if re.search(r'__\d+__', prettystring):
        if fullroll.__len__() > 0:
            output = message.author.mention + ' rolled **' + str(total) + '**! : ' + fullroll + '\n' + prettystring + '\n :star2: **A CRITICAL HIT, HUZZAH!** :star2:'
        else:
            output = message.author.mention + ' rolled **' + str(total) + '**!\n' + prettystring + '\n :star2: **A CRITICAL HIT, HUZZAH!** :star2:'
    else:
        if fullroll.__len__() > 0:
            output = message.author.mention + ' rolled **' + str(total) + '**! : ' + fullroll + '\n' + prettystring
        else:
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


async def dhroll(fullroll, message):
    #split roll into parts
    diceparts = re.split("<", fullroll)

    # assign parts to function
    target = int(diceparts[1])

    roll = random.randint(1, 100)

    diff = target - roll
    if diff >= 0:
        succ = True
        diff = diff / 10
        diff = math.trunc(diff)
    elif diff < 0:
        succ = False
        diff = diff / 10
        diff = math.trunc(diff)
        diff = -diff

    dos = diff+1

    print(roll)
    print('TARGET: ' +str(target))
    print("-------")

    prettystring = '[' + str(roll) + '] - Target: ' + str(target)
    if succ:
        output = message.author.mention + ' succeeded with **' + str(dos) + '** DoS!\n' + prettystring
    else:
        output = message.author.mention + ' failed with **' + str(dos) + '** DoF!\n' + prettystring

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


async def postluck(message):
    msg = []
    for user in users:
        rolls = user[1:]
        diecount = len(user[1:])
        d20rolls = []
        bestroll = [0, 999]
        worstroll = [999, 1]
        bestd20 = 0
        worstd20 = 21
        allper = []
        maxcount = 0
        mincount = 0
        for rollpair in rolls:
            rollper = rollpair[0]/rollpair[1]
            allper.append(rollper*100)
            # Checking for best roll
            # Checking if roll is better by proportion
            if rollper > bestroll[0]/bestroll[1]:
                bestroll = rollpair
            # Checking if roll is same by proportion but larger die (considered better roll)
            elif rollper == bestroll[0]/bestroll[1]:
                if rollpair[1] > bestroll[1]:
                    bestroll = rollpair
            # In all other cases, bestroll remains unchanged

            # Checking for worst roll
            # Checking if roll is worse by proportion
            if rollper < worstroll[0]/worstroll[1]:
                worstroll = rollpair
            # Checking if roll is the same by proportion but larger die
            elif rollper == worstroll[0]/worstroll[1]:
                if rollpair[1] > worstroll[1]:
                    worstroll = rollpair
            # In all other cases, worstroll remains unchanged

            if rollpair[1] == 20:
                if rollpair[0] > bestd20:
                    bestd20 = rollpair[0]
                if rollpair[0] < worstd20:
                    worstd20 = rollpair[0]
                d20rolls.append(rollpair[0])

            if rollpair[0] == rollpair[1]:
                maxcount = maxcount+1
            if rollpair[0] == 1:
                mincount = mincount+1
        nat20 = d20rolls.count(20)
        nat1 = d20rolls.count(1)
        averageper = sum(allper)/diecount
        average = sum(d20rolls)/len(d20rolls)
        msg.append(str(user[0].mention) + ' stats:' + '\n' + f'You rolled a total of **{diecount}** dice.\n' +
                   f'On average you rolled in {round(averageper,2)} percentile on all of your dice.\n' +
                   f'Your best roll was a {bestroll[0]} on a d{bestroll[1]} ({round((bestroll[0]/bestroll[1])*100,2)} percentile)\n' +
                   f'Your worst roll was a {worstroll[0]} on a d{worstroll[1]} ({round((worstroll[0]/worstroll[1])*100,2)} percentile)\n' +
                   f'You rolled maximum on {maxcount} die.\n' +
                   f'You rolled minimum on {mincount} die.\n\n' +
                   f'Total number of d20s rolled: **{len(d20rolls)}**\n' +
                   f'Your average on all of these was {round(average,2)}\n' +
                   f'Your best roll on a d20 was {bestd20}\n' +
                   f'Your worst roll on a d20 was {worstd20}\n' +
                   f'You rolled {nat20} nat 20s and {nat1} nat 1s.')
    for m in msg:
        await message.channel.send(m)


client.run(TOKEN)
