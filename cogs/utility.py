import json
import sqlite3
from sqlite3 import Error

import discord
from discord.ext import commands



Groupdb = r"C:\Users\samue\Desktop\KekNub\Group.db"

class utility(commands.Cog):


    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit = amount)

    @commands.command()
    async def create(self,ctx, GroupName):
        conn = utility.create_connection(Groupdb)
        sql_create_Group_table = """ CREATE TABLE IF NOT EXISTS """ + GroupName + """ (
                                        id integer
                                        ); """

        if conn is not None:
            utility.create_table(conn, sql_create_Group_table)
        else:
            print("couldnt create Table with name " + GroupName)
    
        user = ctx.message.author
        await ctx.channel.send(user.mention + f" You succesfully created the group " + GroupName)


    @commands.command()
    async def join(self,ctx, GroupName):
        userpingable = ctx.message.author
        user = ctx.message.author.id
        conn = utility.create_connection(Groupdb)
        with conn:
            print("user")
            print(user)
            utility.join_group(conn, GroupName,user)
        await ctx.channel.send(f" joined group " + GroupName + userpingable.mention)

    @commands.command()
    async def pingGroup(self,ctx, GroupName):
        conn = utility.create_connection(Groupdb)
        cur = conn.cursor()
        sql = "SELECT * FROM " + GroupName
        print(sql)
        cur.execute(sql)
        print("its working")
        rows = cur.fetchall()
        print("its working2")
        for user in rows:
            userstring = str(user)
            length = len(userstring)
            userstring_formated = userstring[1:length-2]
            pingable = "<@" + userstring_formated + ">"
            await ctx.channel.send(pingable)


    @commands.command()
    async def pfp(self,ctx, user: discord.Member):
        pfp = user.avatar_url
        embed = discord.Embed(title="Profilepicture ", description = "{}, current profilepicture".format(user.mention), color=ctx.author.color)
        embed.set_image(url=(pfp))
        await ctx.send(embed=embed)

    @commands.command(help = "takes a user, amount of pings and a message as argument")
    async def ping(self,ctx, pinguser : discord.Member, amount : int, message):
        for i in range(0, amount):
            await ctx.send(message + pinguser.mention)



    @commands.Cog.listener()
    async def on_ready(self):
        print('utility is ready')

def setup(bot):
    bot.add_cog(utility(bot))

def write_json(new_data, filename):
    with open(filename, 'r') as file:
        file_data = json.load(file)
        file_data.update(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)


def create_connection(db_file):
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_db(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()



def join_group(conn, GroupName, user):
        
    cur = conn.cursor()
    print ("before sql query")
    sql = "INSERT INTO " + GroupName + "(id) VALUES " + "(" + str(user) + ")"
    print("after sql")
    print(sql)
    cur.execute(sql)
    print ("its working")
    conn.commit()
    return cur.lastrowid
