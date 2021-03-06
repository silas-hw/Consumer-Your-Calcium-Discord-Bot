#modules
import logging
import discord
from discord.ext import commands

#checks
from checks import Muted

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief="Display infomation on any command", description="Give a detailed explanation of any command alongside how to use it", usage=r"//help <command>")
    @Muted.check()
    async def help(self, ctx, command=None):

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
                cmd = self.client.get_command(command)
                description = cmd.description
                example = cmd.usage
                guild_only = ([check for check in cmd.checks if 'guild_only' in str(check)] != []) #check if command is guild only

                if description == '':
                    description = 'No description available'

                helpMessage = discord.Embed(title="Calcium Consumer Help")
                helpMessage.add_field(name=command, value=f"{description}\n\nServer exclusive: {guild_only}\n`{example}`")

                await ctx.send(embed=helpMessage)

            
            #if the command given doesn't exist
            except:
                await ctx.send("Command does not exist")
                return
    
    #give link to changelog
    @commands.command(aliases=['log', 'change', 'changes'], brief="Provides link to the change log", description="Gives a link to the changelog,\n where all notable and unreleased changes will be documented")
    @Muted.check()
    async def changelog(self, ctx):
        await ctx.send('https://github.com/silas-hw/Consumer-Your-Calcium-Discord-Bot/blob/master/CHANGELOG.md')
        
def setup(client):
    client.add_cog(Help(client))