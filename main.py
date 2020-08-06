#modules
import json
import os
import discord
from discord.ext import commands, tasks

#set token
with open('tokens.json', 'r') as tokenfile:
    tokens = json.load(tokenfile)
    TOKEN = tokens['test']

#custom prefixes
def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
client.remove_command('help')

@client.event
async def on_ready():
    print('\nbot online\n')

@client.event
async def on_guild_join(guild):
    #creates default prefix for servers'''

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "//"
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    print(f"\nbot added to {guild}")

@client.event
async def on_guild_remove(guild):
    #removes server from prefixes json file when they remove the bot'''

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    print(f"\nbot removed from {guild}")

#allows users to changeprefix
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
print('loading cogs: ')
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        print(filename)
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN) #when going from testing branches to the main branch remember to change to the main bot token      