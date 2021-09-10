from discord import member, voice_client
from discord.ext.commands.bot import Bot
import youtube_dl
import os
import discord
from discord.utils import get
from discord import utils
from discord.ext import commands




class voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('voice is ready')

    @commands.command()
    async def joinchannel(self, ctx, channel : str):
        if discord.utils.get(ctx.guild.voice_channels, name = channel) is None:
            await ctx.send("this aint a voicechannel you fcking donkey")
        else:
            print("got here")
            voice_Channel = discord.utils.get(ctx.guild.voice_channels, name = channel)
            voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        
            await voice_Channel.connect()
         
    @commands.command()
    async def leavechannel(self, ctx):
        if(ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send("I'm not in a voicechannel")


    @commands.command()
    async def playsong(self, ctx, url : str):
        songcheck = os.path.isfile("song.mp3")
        try:
            if songcheck:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("wait")
            return
        voice_Channel = discord.utils.get(ctx.guild.voice_channels, name = "Allgemein")
        await voice_Channel.connect()
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

        
        await voice_Channel.connect()

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Currently no audio is playing.")
 
    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")


def setup(bot):
    bot.add_cog(voice(bot))


