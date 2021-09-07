import discord
from discord.ext import commands

class admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(':)')
    async def logout(self, ctx):
        await ctx.send("Bot will logout now")
        self.bot.logout


    @commands.command()
    @commands.has_role(":)")
    async def kick(self, ctx, member : discord.Member, *, reason = None):
        print(reason)
        await member.kick(reason = reason)


    @commands.command()
    @commands.has_role(":)")
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        print(reason)
        await member.ban(reason = reason)


def setup(bot):
    bot.add_cog(admin(bot))