import discord
from discord.ext import commands
import yaml
import re

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


def parse_rolls(input):
    rolls_unsplit = []
    rolls = []
    comsplit = input.split(',')
    for command in comsplit:
        command = command.strip()
        match = re.match(r'(\d+)#(.*)', command)
        if match:
            count = int(match.group(1))
            roll_expr = match.group(2).strip()
            rolls_unsplit.extend([roll_expr] * count)
        else:
            rolls_unsplit.append(command)
    for roll in rolls_unsplit:
        text_split = re.match(r'((?:(?:\d+#)?[+-]?\d*d\d+(?:[kd][hl]\d+)?(?:[+-><=]\d+)*))\s*([^,]*)', roll)
        rolls.append([text_split.group(1).strip(), text_split.group(2).strip()])
    return rolls


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
    rolls = parse_rolls(input_command)
    await ctx.reply(f"Command received: {rolls}")

if __name__ == "__main__":
    bot.run(TOKEN)
