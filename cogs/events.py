import discord
from discord.ext import commands


class events(commands.Cog):


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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please pass in all requiered arguments")
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("This command doesn't exist")
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')




def setup(bot):
    bot.add_cog(events(bot))

