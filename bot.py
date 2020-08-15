"""https://discord.com/oauth2/authorize?client_id=605758711071506432&permissions=67119104&scope=bot"""

import discord
from discord.ext import commands
import os, sqlite3

def get_prefix(client, message):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM guilds WHERE guild_id="{message.guild.id}"')
    query = curr.fetchone()

    if query == None:
        curr.execute(f"INSERT INTO guilds VALUES ('{message.guild.id}','$')")
        conn.commit()
        return "$"
    else:
        return query[1]

client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_guild_join(guild):
    print(dir(guild))
    print(guild.id)

    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f"INSERT INTO guilds VALUES ('{guild.id}','$')")
    conn.commit()
    conn.close()

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run('NjA1NzU4NzExMDcxNTA2NDMy.XUBKww.sI5-DZzdCCXdgW44uEACqGzaVpc')
