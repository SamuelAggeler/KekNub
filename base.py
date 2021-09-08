import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


#load token, discord intents and db 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


Intents = discord.Intents.default()



#returns a valid prefix for the bot
def get_prefix(bot, message):
    prefixes = ["?","!","help"]

    if not message.guild:
        return "?"

    return commands.when_mentioned_or(*prefixes)(bot,message)

extensions = ["cogs.utiliy",
              "cogs.voice",
              "cogs.admin",
              "cogs.events",
              ]


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

#initalizes the botstatus once the bot is ready
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(
        type = discord.ActivityType.watching,
        name = "you"
    ))

bot.run(TOKEN)
