#modules used
import re
import pytz
import asyncio
from datetime import datetime
import discord
from discord.ext import commands

class useful(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.afkUsers = {}

    @commands.command()
    async def afk(self, ctx, *, userMessage=" "):

        #if user is already afk, remove them from the afk dict, if not add them to it
        print("test")
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
    
    #mentions a role or member after a given amount of time has passed
    @commands.command(brief="Reminds friends to play games", description="mentions role/user after given amount of minutes has passed")
    async def reminder(self, ctx, users, timeStr = "5", *, message="reminder"):
        
        if re.search(r"\d\d:\d\d", timeStr): #checks formatting of time given
            givenHourStr, givenMinuteStr = timeStr.split(":") #the numbers seperated by the : are assigned to two variables
            givenMinuteStr = givenMinuteStr.lstrip("0") #removes leading zeros

            tz = pytz.timezone('Europe/London') #sets timezone to be used to get current hour and minute
            currentHour = datetime.now(tz).hour
            currentMinute = datetime.now(tz).minute

            hour, minute = int(givenHourStr) - currentHour, int(givenMinuteStr) - currentMinute
            time = hour*60**2 + minute*60

            await ctx.send(f"<:bell:727914124230787104> Reminder set for {timeStr} with message '{message}'")
        else:
            time = int(timeStr)*60
            await ctx.send(f"<:bell:727914124230787104> Reminder set for {time/60} minutes with message '{message}'")
        
        await asyncio.sleep(time)
        await ctx.send(f"<:bell:727914124230787104> {users} {message} *(reminder set by {ctx.message.author})*")

    #gives information of given user
    @commands.command(aliases=["info", "i"], brief="get details of any member")
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

def setup(client):
    client.add_cog(useful(client))
