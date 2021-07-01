# Work with Python 3.6
import discord
import re
import random

TOKEN = ''

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('.hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    elif message.content.startswith('.roll'):
        # Remove leading command
        fullroll = message.content.replace('.roll', '')
        # Remove any whitespace
        fullroll = fullroll.replace(' ', '')
        # Split into parts to be subtracted from each other
        negrollparts = re.split("[-]", fullroll)
        # Create empty array to collect all values
        fullsplit = []
        i = 0
        # For each component of negative parts, split on + and add to full split
        for x in negrollparts:
            # Need to add a '-' to the FIRST split of every rollpart other than the first
            rollpart = re.split("[+]", x)
            if i>0:
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


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
