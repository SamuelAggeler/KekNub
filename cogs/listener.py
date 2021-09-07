import discord
from discord.ext import commands


class listener(commands.Cog):


    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print('events is ready')

    @commands.Cog.listener('on_message')
    async def testrection(self,message):
        if 'thumbs' in message.content.lower():
            emoji = '👍'
            await message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        await ctx.send("Hello there f'{member}")

    @commands.Cog.listener()
    async def on_member_remove(self, ctx, member):
        await ctx.send("bye f'{member}")

        

def setup(bot):
    bot.add_cog(listener(bot))

