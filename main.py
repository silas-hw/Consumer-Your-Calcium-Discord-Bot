#modules
import json
import os
import discord
from discord.ext import commands

#custom prefixes
def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_ready():
    print('bot online\n')

@client.event
async def on_guild_join(guild):

    print(f"\nbot added to {guild}")

    #creates default prefix for servers
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "//"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):

    print(f"\nbot removed from {guild}")

    #removes server from prefixes json file when they remove the bot
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

#command for server to set custom id
@client.command(aliases=["prefix", "cp"])
async def changeprefix(ctx, prefix):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    print(f"\n{ctx.message.author} changed prefix in {ctx.guild} to {prefix}")
    await ctx.send(f"Prefix changed to '{prefix}'!")



#cog loading and reloading

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