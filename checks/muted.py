import json
import discord
from discord.ext import commands

class Muted():
    @staticmethod
    def check():
        with open('muted_members.json', 'r') as f:
            muted = json.load(f)

        def predicate(ctx):
            if isinstance(ctx.channel, discord.channel.DMChannel):
                return True
            return ctx.message.author.id not in muted[str(ctx.guild.id)]
        return commands.check(predicate)

    @staticmethod
    def not_muted(guildid, memberid):
        with open('muted_members.json', 'r') as f:
            muted = json.load(f)
        return (memberid not in muted[str(guildid)])
