import logging
import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO, filename='log.log', format="[%(asctime)s]%(levelname)s:%(module)s~ %(message)s")
class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.mutedMembers = {}
    
    @commands.command(brief="mutes a member", description="any message sent by a muted member will be deleted", usage=r"//mute @CleanlyWolf#5407")
    @commands.has_role('Admin')
    async def mute(self, ctx, member: discord.Member):
        if member in self.mutedMembers[str(ctx.message.guild.id)]:
            self.mutedMembers[ctx.guild.id].remove(member)

            logging.info(f"\n{ctx.message.author} unmuted {member}")
            await ctx.send(f"<:speaker:727914839615471687> {member} is no longer muted")
        else:
            self.mutedMembers[str(ctx.message.guild.id)].append(member)

            logging.info(f"\n{ctx.message.author} muted {member}")
            await ctx.send(f"<:mute:727914643879886929> {member} is now muted")

    @commands.command()
    @commands.has_role('Admin')
    async def muted(self, ctx):
        message = "```Muted members:\n"
        for member in self.mutedMembers[str(ctx.message.guild.id)]:
            message += f"    {member}\n"
        message += "```"
        await ctx.send(message)
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.mutedMembers[guild.id] = []

    @commands.Cog.listener()
    async def on_message(self, message):
        
        guildid = str(message.guild.id)
        if guildid not in self.mutedMembers:
            self.mutedMembers[guildid] = []

        if message.author in self.mutedMembers[guildid]:
            await message.delete() #deletes message if user is muted
            return

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.message.author in self.mutedMembers[str(ctx.message.guild.id)]:
            return

def setup(client):
    client.add_cog(Admin(client))