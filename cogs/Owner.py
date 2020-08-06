import discord
from discord.ext import commands

class Owner(command.Cog):

    def __init__(self, client):
        self.client = client

    @staticmethod
    def _check_owner():
        def predicate(ctx):
            return ctx.message.author.id == 385126151342915588
        return commands.check(predicate)

    #used to reload cogs
    @client.command()
    @check_owner()
    async def reload(ctx, extension):
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")

        print(f"{extension} reloaded by {ctx.message.author}")

    #used to load cogs
    @client.command()
    @check_owner()
    async def load(ctx, extension):
        client.load_extension(f"cogs.{extension}")

        print(f"{extension} loaded by {ctx.message.author}")