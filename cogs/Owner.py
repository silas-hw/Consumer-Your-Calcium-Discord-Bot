import discord
from discord.ext import commands

class Owner(commands.Cog):

    def __init__(self, client):
        self.client = client

    @staticmethod
    def _check_owner():
        def predicate(ctx):
            return ctx.message.author.id == 385126151342915588
        return commands.check(predicate)

    #used to reload cogs
    @commands.command()
    @_check_owner()
    async def reload(self, ctx, extension):
        self.client.unload_extension(f"cogs.{extension}")
        self.client.load_extension(f"cogs.{extension}")

        print(f"{extension} reloaded by {ctx.message.author}")

    #used to load cogs
    @commands.command()
    @_check_owner()
    async def load(self, ctx, extension):
        self.client.load_extension(f"cogs.{extension}")

        print(f"{extension} loaded by {ctx.message.author}")

def setup(client):
    client.add_cog(Owner(client))