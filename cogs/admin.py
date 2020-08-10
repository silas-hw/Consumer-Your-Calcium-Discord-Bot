import json
import logging
from logging import FileHandler
import discord
from discord.ext import commands

adminLog = logging.getLogger('Admin-log')
adminLog.setLevel(logging.INFO)

formatter = logging.Formatter("[%(asctime)s]%(levelname)s~ %(message)s")

fileHandler = logging.FileHandler('admin.log')
fileHandler.setFormatter(formatter)

adminLog.addHandler(fileHandler)


class mutedinst():

    @property
    def members(self):
        with open('muted_members.json', 'r') as f:
            muted = json.load(f)
        return muted
    
    def mute(self, guildid, memberid):
        with open('muted_members.json', 'r') as f:
            muted = json.load(f)
        if memberid not in muted[str(guildid)]:
            muted[str(guildid)].append(memberid)
        with open('muted_members.json', 'w') as f:
            json.dump(muted, f, indent=4)

    def unmute(self, guildid, memberid):
        with open('muted_members.json', 'r') as f:
            muted = json.load(f)
        if memberid in muted[str(guildid)]:
            muted[str(guildid)].remove(memberid)
        with open('muted_members.json', 'w') as f:
            json.dump(muted, f, indent=4)

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.mutedinst = mutedinst()

    def write_file(self):
        with open('muted_members.json', 'r') as f:
            json.dump(mutedinst.members, f, indent=4)

    @commands.command(brief="mutes a member", description="any message sent by a muted member will be deleted", usage=r"//mute <mute>")
    @commands.guild_only()
    @commands.has_role('Admin')
    async def mute(self, ctx, member: discord.Member):
        self.mutedinst.mute(ctx.message.guild.id, member.id)
        await ctx.send(f"<:mute:727914643879886929> {member} is now muted")

        adminLog.info(f"{ctx.message.author} muted {member}")

    @commands.command(brief="Unmutes a member", description="Unmutes a member so they can speak and use commands again", usage=r"//unmute <member>")
    @commands.guild_only()
    @commands.has_role('Admin')
    async def unmute(self, ctx, member: discord.Member):
        self.mutedinst.unmute(ctx.message.guild.id, member.id)
        await ctx.send(f"<:speaker:727914839615471687> {member} is no longer muted")

        adminLog.info(f"{ctx.message.author} unmuted {member}")
        
    @commands.command(brief="Show who's muted", descrption="Display a list of currently muted members", usage=r"//muted")
    @commands.guild_only()
    @commands.has_role('Admin')
    async def muted(self, ctx):
        message = "```Muted members:\n"
        for memberid in self.mutedinst.members[str(ctx.message.guild.id)]:
            message += f"    {ctx.guild.get_member(memberid)}\n"
        message += "```"
        await ctx.send(message)

    @commands.command(aliases=['audit', 'adminlog', 'alogs', 'alog'], brief="Show a log of admin commands used", description="Displays the last 5 lines of the admin logs, displaying when an admin command was used and who used it", usage=r"//alog")
    @commands.guild_only()
    @commands.has_role('Admin')
    async def adminlogs(self, ctx):
        logs=''
        with open('admin.log', 'r') as f:
            for line in (f.readlines() [-5:]):
                logs += f'{line}'
        await ctx.send(f'```css\n{logs}```')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in self.mutedinst.members[str(message.guild.id)]:
            await message.delete() #deletes message if user is muted

def setup(client):
    client.add_cog(Admin(client))