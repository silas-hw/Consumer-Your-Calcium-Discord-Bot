import discord
from discord.ext import commands

class Owner():
    @staticmethod
    def check():
        def predicate(ctx):
            return ctx.message.author.id == 385126151342915588
        return commands.check(predicate)