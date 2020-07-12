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
            for cog in self.client.cogs:
                
                string = ""

                cogInstance = self.client.get_cog(cog)

                for cmd in cogInstance.get_commands():

                    
                    brief = self.client.get_command(str(cmd)).short_doc

                    string += f"|----**{cmd}**:\n"
                    string += f"|--------*{brief}*\n|\n"

                embed.add_field(name=f"| __{cog}__:", value=string, inline=False)

        

        else:

            description = self.client.get_command(command).description

            example = self.client.get_command(command).usage

            if description == '':
                description = 'No description available'

            string = f"{description}\n*{example}*"

            embed.add_field(name=command, value=string, inline=False)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))