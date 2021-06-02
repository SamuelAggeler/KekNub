import os
import discord
import random

from discord import utils
from discord import channel
from discord.ext import commands
from discord.abc import GuildChannel
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


bot = commands.Bot(command_prefix='?')

@bot.command(name='create-channel')
@commands.has_role(':)')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)



@bot.event
async def on_message(message):
    if 'fabian' in message.content.lower():
        await message.channel.send('Schnitte! :smirk: ')



@bot.command(name = '99', help='this is a helper command')
async def test(ctx):
    testquote = ['test']

    response = random.choice(testquote)
    await ctx.send(response)



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)