"""https://discord.com/oauth2/authorize?client_id=605758711071506432&permissions=67119104&scope=bot"""

import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = "$")


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
