import discord
import random as rand
from discord.ext import commands

class random(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    
    @commands.Cog.listener()
    async def on_ready(self):
        print('random is ready')
        

    @commands.command(name = 'random', help='takes input and returns random choice')
    async def random(ctx, *args):
        await ctx.send(rand.choice(args))


    
def setup(bot):
    bot.add_cog(random(bot))