import os
import discord
import random as rand
import datetime
import asyncio
import sys
import json

from discord.ext.commands.core import Group
import utility
from discord.flags import Intents

from discord.utils import get
from discord import utils
from discord import channel
from discord.ext import commands
from discord.abc import GuildChannel
from discord.user import ClientUser
from dotenv import load_dotenv



#load token, discord and intents 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
Groupdb = r"C:\Users\samue\Desktop\KekNub\Group.db"


Intents = discord.Intents.default()
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
#restart command for the bot
@bot.command()
@commands.has_role(':)')
async def restart(ctx):
    await ctx.send("Bot will restart now")
    bot.logout
    bot.login
    await ctx.send("Bot is back online")
 
#takes arbitrary amount of arguments and returns a random one
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


#testreaction that puts a thumb under a message that contains thumbs
@bot.listen('on_message')
async def addingEmote(message):
    if 'thumbs' in message.content.lower():
        emoji = '👍'
        await message.add_reaction(emoji)

#pings user a certain amount of time with a custom message
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
async def create(ctx, GroupName):
    conn = utility.create_connection(Groupdb)
    sql_create_Group_table = """ CREATE TABLE IF NOT EXISTS """ + GroupName + """(
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    if conn is not None:
        utility.create_table(conn, sql_create_Group_table)
    else:
        print("couldnt create Table with name " + GroupName)
    
    user = ctx.message.author
    await ctx.channel.send(user.mention + f" You succesfully created the group " + GroupName)


@bot.command()
async def join(ctx, GroupName):
    user = ctx.message.author
    conn = utility.create_connection(Groupdb)
    with conn :
        utility.create_group(conn, GroupName,ctx.message.author,)
    await ctx.channel.send(f" joined group " + GroupName + user.mention)

bot.run(TOKEN)
