import discord
from discord.ext import commands

def check_owner():
    def predicate(ctx):
        return ctx.message.author.id == 385126151342915588
    return commands.check(predicate)

class Admin(commands.Cog):

    def __ini__(self, client):
        self.client = client
    
    @commands.command(aliases=["announce"])
    @check_owner()
    async def announcement(self, ctx, message):

        await ctx.message.delete() #deletes message used to invoke command
        await ctx.send(f"{ctx.message.guild.default_role} {message}")

def setup(client):
    client.add_cog(Admin(client))