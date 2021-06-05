import os
import discord
import random as rand

from discord import utils
from discord import channel
from discord.ext import commands
from discord.abc import GuildChannel
from dotenv import load_dotenv



#load token, discord and intents 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')




#initalize bot prefix
bot = commands.Bot(command_prefix='?')

#helper message to see, when the bot is connected
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
 
#takes arbitrary amount of arguments and returns a random one
@bot.command(name = 'random', help='takes input and returns random choice')
async def random(ctx, *args):
    await ctx.send(rand.choice(args))


@bot.command()
@commands.has_role(':)')
async def create_channel(ctx, channel_name='testchannel1'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')





bot.run(TOKEN)