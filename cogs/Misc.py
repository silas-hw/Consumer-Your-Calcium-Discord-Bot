#modules used
import re
import pytz
import asyncio
from datetime import datetime
import discord
from discord.ext import commands, tasks

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.afkUsers = {}

    #allows a user to set them self as afk
    @commands.command(brief="Set yourself as afk", description="set yourself as afk so if others mention you they are told", usage=r"//afk haha brrrr")
    async def afk(self, ctx, *, userMessage=" "):

        #if user is already afk, remove them from the afk dict, if not add them to it
        if ctx.message.author in self.afkUsers:
            self.afkUsers.pop(ctx.message.author)
            await ctx.send("you are no longer afk")
        else:
            self.afkUsers[ctx.message.author] = userMessage
            await ctx.send(f"<:zzz:727916453466210434> you are now afk with message - {userMessage}")

    @commands.Cog.listener()
    async def on_message(self, message):
        
        #if a member is mentioned but the member is afk, a message is sent
        textChannel = message.channel
        afkChannel = self.client.get_channel(690550327975346176)
        
        for member in message.mentions:
            if member != message.author:
                if member in self.afkUsers:
                    await textChannel.send(f"<:zzz:727916453466210434> {member} is afk - {self.afkUsers[member]}")
                elif member in afkChannel.members:
                    await textChannel.send(f"<:zzz:727916453466210434> {member} is afk")
    
    #gives information of given user
    @commands.command(aliases=["info", "i"], brief="get details of any member", description="get the nickname, date joined, top role and current status of any member", usage=r"//info @CleanlyWolf#5407")
    async def information(self, ctx, member: discord.Member):

        message = ""
        message += f"Nickname: {member.display_name}\n"
        message += f"Joined server at: {member.joined_at}\n"
        message += f"Top role: {member.top_role}\n"
        message += f"Status: {member.status}\n"
        try:
            message += f"Current activity: {member.activities[0]}\n"
        except:
            pass

        embed = discord.Embed(
            title = str(member.name),
            description = message
        )
        
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    #gives them the role mentioned for announcements
    @commands.command(aliases=['ping'], brief="get pinged for announcements", description="give you the *consumer* role, which is pinged for announcements and updates")
    async def pingme(self, ctx):

        role = ctx.guild.get_role(732354594536947803)
        await ctx.message.author.add_roles(role, reason=f'{ctx.message.author.name} now pinged for announcements')
        await ctx.send("You'll now be pinged for announcements in <#684458229090353222>")

    #react to the message before the command with a given set of emojis
    @commands.command(aliases=['r'], brief="reacts to messages", description="Reacts to the previous message sent\nThe message used to invoke the command is deleted", usage=r"//react epic")
    async def react(self, ctx, reaction='epic'):

        await ctx.message.delete()

        reactions = {
            'epic': ['🇪', '🇵', '🇮', '🇨'],
            'lmao': ['🇱', '🇲', '🇦',  '🇴'],
            'pride': ['🏳️‍🌈', '🌈', '❤️' ,'🧡', '💛' ,'💚' ,'💙' ,'💜', '🖤', '🤎', '🤍'],
            'shy': ['🥺', '👉', '👈']
        }

        messageHistory = await ctx.channel.history(limit=2).flatten()

        for emoji in reactions[reaction.lower()]:
            await messageHistory[0].add_reaction(emoji)

def setup(client):
    client.add_cog(Misc(client))
