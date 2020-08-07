#modules
import logging
import json
import os
import discord
from discord.ext import commands, tasks

logging.basicConfig(level=logging.INFO, filename='log.log', format="[%(asctime)s]%(levelname)s:%(module)s~ %(message)s")
logging.info('New main run\n\n')

#set token
with open('tokens.json', 'r') as tokenfile:
    tokens = json.load(tokenfile)
    TOKEN = tokens['main']

#custom prefixes
def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
client.remove_command('help')

@client.event
async def on_ready():
    logging.info('bot online')

@client.event
async def on_guild_join(guild):
    #creates default prefix for servers'''

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "//"
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    logging.info(f"bot added to {guild}")

    with open('muted_members.json', 'r') as f:
        muted = json.load(f)
    muted[str(guild.id)] = []
    with open('muted_members.json', 'r') as f:
        json.dump(muted, f, indent=4)


@client.event
async def on_guild_remove(guild):
    #removes server from prefixes json file when they remove the bot'''

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    logging.info(f"bot removed from {guild}")

#allows users to changeprefix
@client.command(aliases=["prefix", "cp"])
async def changeprefix(ctx, prefix):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    logging.info(f"{ctx.message.author} changed prefix in {ctx.guild} to {prefix}")
    await ctx.send(f"Prefix changed to '{prefix}'!")

#cog loading and reloading
logging.info('Loading cogs: ')
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        logging.info(f"\tCog~ {filename}")
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN) #when going from testing branches to the main branch remember to change to the main bot token      