import os
import discord
import random as rand
import datetime
import asyncio
import sys
import json
import sqlite3
from sqlite3 import Error
from discord import client
from discord import guild


from discord.ext.commands.core import Group
from discord.flags import Intents

from discord.utils import get
from discord import utils
from discord import channel
from discord.ext import commands
from discord.abc import GuildChannel
from discord.user import ClientUser
from dotenv import load_dotenv



#load token, discord intents and db 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
print(GUILD)




Intents = discord.Intents.default()
#initalize bot prefix



#methode still in testing, returns a valid prefix for the bot
def get_prefix(bot, message):
    prefixes = ["?","!","help"]

    if not message.guild:
        return "?"

    return commands.when_mentioned_or(*prefixes)(bot,message)

extensions = ["cogs.utiliy",
              "cogs.voice",
              "cogs.admin",
              "cogs.events",
              "cogs.listener"]


bot = commands.Bot(command_prefix=get_prefix, description= "testing my new bot")

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        print(filename[:-3])
        bot.load_extension(f"cogs.{filename[:-3]}")

#helper message to see, when the bot is connected
#also now displays watching you as status of the bot.
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(
        type = discord.ActivityType.watching,
        name = "you"
    ))

 
#takes arbitrary amount of arguments and retur
# ns a random one
@bot.command(name = 'random', help='takes input and returns random choice')
async def random(ctx, *args):
    await ctx.send(rand.choice(args))

#expects a name and then creates a textchannel, :) role is requiered to create a channel
@bot.command()
@commands.has_role(':)')
async def create_channel(ctx,channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

#small errorhandling if someone without :) roles tries to create a text channel
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@bot.command()
async def reaction(ctx):
    message = 'this should send a thumb'
    emoji = '👍'
    await ctx.send(message + emoji)

@bot.command()
async def pingpong(ctx):
    await ctx.send("pong")


@bot.command(help = "start a giveaway takes time in mins and then the prize as \na String")
async def startgive(ctx, mins : int, *, prize: str):
    embed = discord.Embed(title = 'Giveaway', description = f"{prize}", color = ctx.author.color)

    end = datetime.datetime.utcnow() + datetime.timedelta(seconds = mins*60)

    embed.add_field(name = "Ends At: ", value = f"{end} UTC")
    embed.set_footer(text = "Ends {mins} minutes from now!" )

    my_msg = await ctx.send(embed = embed)

    await my_msg.add_reaction("👍")

    await asyncio.sleep(mins*60)

    new_msg = await ctx.channel.fetch_message(my_msg.id)

    user = new_msg.reaction[0].users().flatten()
    user.pop(user.index(bot.user))

    winner = random.choice(user)

    await ctx.send(f"Congratulation {winner.mention} won {prize}")





##pings user a certain amount of time with a custom message
@bot.command(help = "takes a user, amount of pings and a message as argument")
async def ping(ctx, user1 : discord.Member, amount : int, message):
    for i in range(0, amount):
        await ctx.send(message + user1.mention)

#fetch Profilepicture from User that is passed as argument
@bot.command()
async def pfp(ctx, user: discord.Member):
    pfp = user.avatar_url
    embed = discord.Embed(title="Profilepicture ", description = "{}, current profilepicture".format(user.mention), color=ctx.author.color)
    embed.set_image(url=(pfp))
    await ctx.send(embed=embed)



@bot.command()
async def playsong(ctx, url : str):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = "Allgemein")
    voice = discord.utils.get(client.voice_clients, GUILD)
    await channel.VoiceChannel.connect()


bot.run(TOKEN)
