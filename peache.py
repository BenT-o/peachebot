# Work with Python 3.6
import discord
import re

# TOKEN = 'NDY2NjYzNjI0MjM3MzgzNjgw.Dq-y0A.4Tjypst5ZTWdhdI5cnwzxtIzPqs'

TOKEN = 'NDQ2OTMzMzU5MDMwMTczNjk2.XweDxg.IzcQFiHmGfktLSTnAfWOJi3J8VI'

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
        fullroll = message.content.replace('.roll ', '')
        print("full roll:")
        print(fullroll)
        # Remove any whitespace
        fullroll = fullroll.replace(' ', '')
        print("whitespace removed:")
        print(fullroll)
        # Split into parts to be subtracted from each other
        negrollparts = re.split("[-]", fullroll)
        print("neg split array:")
        print(negrollparts)
        # Create empty array to collect all values
        fullsplit = []
        i = 0
        # For each component of negative parts, split on + and add to full split
        for x in negrollparts:
            # Need to add a '-' to the FIRST split of every rollpart other than the first
            rollpart = re.split("[+]", x)
            if i>0:
                rollpart[0] = '-' + rollpart[0]
            print("split part:")
            print(rollpart)
            for p in rollpart:
                fullsplit.append(p)
            print(fullsplit)
            i = i+1

        print("-------")
        # rolltotal = 0
        # for i in range(fullsplit.__len__()):
        #     if i>0:
        #
        #     for j in fullsplit[i]:




@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
