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
            
            #iterate through a list of every cog 
            for cog in self.client.cogs:
                
                helpMessage += f"__**{cog}**__:\n"
                cogInstance = self.client.get_cog(cog) #get the object related to the cog

                #iterate through every command in the cog instance
                for cmd in cogInstance.get_commands():
                    
                    #get the brief attribute from the command and if it is empty change it to 'no brief available'
                    brief = self.client.get_command(str(cmd)).short_doc

                    if brief == '':
                        brief = 'No brief available'

                    #add command name and brief to the help message with formatting
                    helpMessage += f"    **{cmd}**:\n"
                    helpMessage += f"        *{brief}*\n"

                helpMessage += "\n"

        else:

            try:
                #get the description and usage attributes from the object related to the command name
                description = self.client.get_command(command).description
                example = self.client.get_command(command).usage

                #if the description is an empty string
                if description == '':
                    description = 'No description available'

                #add the command name, descriptio and usage to the help message with formatting
                helpMessage += f"**{command}**\n\n{description}\n\n    *{example}*"
            
            #if the command given doesn't exist
            except:
                await ctx.send("Command does not exist")
                return

        await ctx.send(helpMessage)

def setup(client):
    client.add_cog(Help(client))