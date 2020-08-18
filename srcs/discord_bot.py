import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='<')
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Bot running with :')
    print('Username : {}'.format(bot.user.name))
    print('User ID : {}'.format(bot.user.id))
    game = discord.Game('searching cool jobs')
    await bot.change_presence(activity=game)


async def send_message(channel, message):
    await bot.get_channel(channel).send(content=message)


async def send_embed(channel, embed):
    await bot.get_channel(channel).send(embed=embed)

bot.run(DISCORD_TOKEN)
