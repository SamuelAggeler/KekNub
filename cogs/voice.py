from discord import member, voice_client
from discord.ext.commands.bot import Bot
import youtube_dl
import asyncio

import os
import discord
import datetime
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



class voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('voice is ready')

    @commands.command()
    async def joinchannel(self, ctx, channel : str):

        channel = ctx.message.author.voice.channel
        if discord.utils.get(ctx.guild.voice_channels, name = channel) is None:
            await ctx.send("this aint a voicechannel you fcking donkey")
        else:
            voice_Channel = discord.utils.get(ctx.guild.voice_channels, name = channel)
            voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if channel is None:
            await voice_Channel.connect()
        else:
            await channel.connect()
        



def setup(bot):
    bot.add_cog(voice(bot))


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)



def endSong(guild, path):
    os.remove(path) 

