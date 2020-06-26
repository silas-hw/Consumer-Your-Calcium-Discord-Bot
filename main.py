#modules
import os
import discord
from discord.ext import commands

client = commands.Bot(command_prefix="%")

@client.event
async def on_ready():
    print('bot online\n')

#used to reload cogs
@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")

    print(f"{extension} reloaded by {ctx.message.author}")

#used to load cogs
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

    print(f"{extension} reloaded by {ctx.message.author}")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run('NzI2MTkzODQ1ODYzMzE3NTg2.XvZvXA.pKIPyoVn51D5cUWcw-302gwMiwA')