#modules
import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, command=None):

        helpMessage = ">>> " #>>> is a block quote on discord
        
        #if a command wasn't passed
        if command == None:
            
            helpEmbed = discord.Embed(
                title="Calcium Consumer",
                url="https://github.com/silas-hw/Consumer-Your-Calcium-Discord-Bot/wiki/Commands",
                description="ℹ️ [Click here](https://github.com/silas-hw/Consumer-Your-Calcium-Discord-Bot/wiki/Commands) for a full list of commands\n\n❓ Type `//help <command>` for more detail on any command\n\n🖥️ [Visit here](http://silashw.heliohost.org) for the leaderboard"
            )
            
            await ctx.send(embed=helpEmbed)

        else:

            try:
                #get the description and usage attributes from the object related to the command name
                description = self.client.get_command(command).description
                example = self.client.get_command(command).usage

                if description == '':
                    description = 'No description available'

                helpMessage = discord.Embed(title="Calcium Consumer Help")
                helpMessage.add_field(name=command, value=f"{description}\n\n`{example}`")

                await ctx.send(embed=helpMessage)

            
            #if the command given doesn't exist
            except:
                await ctx.send("Command does not exist")
                return

def setup(client):
    client.add_cog(Help(client))