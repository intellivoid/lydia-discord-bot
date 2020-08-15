import discord
from discord.ext import commands
import sqlite3

class Basic(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong!")

    @commands.command(aliases=["cp"], brief="Change the guild-wide bot prefix", usage="<prefix>")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def changeprefix(self, ctx, *, prefix):
        conn = sqlite3.connect('./db.sqlite3')
        curr = conn.cursor()
        curr.execute(f'UPDATE guilds SET prefix = "{prefix}" WHERE guild_id = "{ctx.guild.id}"')
        conn.commit()
        await ctx.send(f"Prefix changed to `{prefix}`")

def setup(client):
    client.add_cog(Basic(client))
