import discord
from discord.ext import commands

def check_owner():
    def predicate(ctx):
        return ctx.message.author.id == 385126151342915588
    return commands.check(predicate)

def check_admin():
    def predicate(ctx):
        return ctx.guild.get_role(699302808784207992) in ctx.message.author.roles
    return commands.check(predicate)

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.mutedMembers = []
    
    @commands.command(aliases=["announce"], brief="Makes an announcement", description="mention everyone with an announcement sent by the bot", usage=r"//announcement test announcement")
    @check_owner()
    async def announcement(self, ctx, *, message):

        await ctx.message.delete() #deletes message used to invoke command
        await ctx.send(f"<@&732354594536947803> {message}")
    
    @commands.command(brief="mutes a member", description="any message sent by a muted member will be deleted", usage=r"//mute @CleanlyWolf#5407")
    @check_admin()
    async def mute(self, ctx, member: discord.Member):

        if member in self.mutedMembers:
            self.mutedMembers.remove(member)

            print(f"\n{ctx.message.author} unmuted {member}")
            await ctx.send(f"<:speaker:727914839615471687> {member} is no longer muted")
        else:
            self.mutedMembers.append(member)

            print(f"\n{ctx.message.author} muted {member}")
            await ctx.send(f"<:mute:727914643879886929> {member} is now muted")

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author in self.mutedMembers:
            await message.delete() #deletes message if user is muted

    @commands.command(brief="used to test and debug code", description="Is only available to the owner. Is used to test and debug code and check how things work")
    @check_owner()
    async def test(self, ctx):
        messageHistory = await ctx.channel.history(limit=2).flatten()
        await messageHistory[1].add_reaction('🙃')

def setup(client):
    client.add_cog(Admin(client))