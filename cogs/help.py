#modules
import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, command=None):

        embed = discord.Embed(
            colour = discord.Colour.orange()
        )

        if command == None:
            for command in self.client.commands:

                name = command(name)
                brief = command(brief)
                embed.add_field(name=name, value=brief, inline=False)

        await ctx.send(embed=embed)
                
