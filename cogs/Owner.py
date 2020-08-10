import logging
import discord
from discord.ext import commands

class Owner(commands.Cog):

    def __init__(self, client):
        self.client = client

    #used to reload cogs
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        self.client.unload_extension(f"cogs.{extension}")
        self.client.load_extension(f"cogs.{extension}")

        logging.info(f"{extension} reloaded by {ctx.message.author}")

    #used to load cogs
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.client.load_extension(f"cogs.{extension}")

        logging.info(f"{extension} loaded by {ctx.message.author}")

    #returns logs
    @commands.command()
    @commands.is_owner()
    async def logs(self, ctx):
        logs=''
        with open('log.log', 'r') as f:
            for line in (f.readlines() [-5:]):
                logs += f'{line}'
        await ctx.send(f'```css\n{logs}```')

    @commands.command(aliases=["announce"], brief="Makes an announcement", description="mention everyone with an announcement sent by the bot", usage=r"//announcement test announcement")
    @commands.is_owner()
    async def announcement(self, ctx, *, message):
        await ctx.message.delete() #deletes message used to invoke command
        await ctx.send(f"<@&732354594536947803> {message}")

    @commands.command(brief="used to test and debug code", description="Is only available to the owner. Is used to test and debug code and check how things work")
    @commands.is_owner()
    async def test(self, ctx):
        messageHistory = await ctx.channel.history(limit=2).flatten()
        await messageHistory[1].add_reaction('🙃')

def setup(client):
    client.add_cog(Owner(client))