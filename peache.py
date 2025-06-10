import discord
from discord.ext import commands
import yaml
import re
from utils.grammar import parse_roll_command

# Load configuration from YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

TOKEN = config['bot']['TOKEN']
LOG_CHANNEL = config['bot']['LOG_CHANNEL']
LOG_FILE = config['bot']['LOG_FILE']

# Intents are required for bots to work with newer versions of Discord's API
intents = discord.Intents.all()
intents.messages = True

# Initialize bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    login_message = f"```peachebot online\nlogged in as: {bot.user.name}\nbot user id: {bot.user.id}```"
    await bot.get_channel(LOG_CHANNEL).send(login_message)


@bot.command()
async def roll(ctx, *, input_command: str):
    """Command to handle dice rolls."""
    print(f"User Input: {input_command}")
    try:
        rolls = await parse_roll_command(input_command)

        for r in rolls:
            count = r['count']
            expression = r['expression']
            comment = r['comment']

            if count < 1:
                raise SyntaxError("You cannot roll a dice expression fewer than 1 times!")

            print(f"Count: {count}")
            print(f"Expression: {expression}")
            print(f"Comment: {comment}")

            #for count in range(count):
            #    roll_these(expression, comment)

        await ctx.reply(f"Command received: {rolls}")

    except SyntaxError as e:
        await ctx.reply(f"Oops! Syntax Error Detected: {e}")



if __name__ == "__main__":
    bot.run(TOKEN)
