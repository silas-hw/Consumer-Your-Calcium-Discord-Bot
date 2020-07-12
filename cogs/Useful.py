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

    @commands.command(brief="Set yourself as afk", description="set yourself as afk so if others mention you they are told", usage=r"//afk foo bar")
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
    
    #mentions a role or member after a given amount of time has passed
    @commands.command(brief="Reminds members or roles", description="mentions role/user after given time has passed\nWhen using 24 hr time it is only possible to set a reminder within the same day,\n a possible way of getting around this is setting a reminder in minutes", usage=r"//reminder @CleanlyWolf#5407 14:00 reeeeeee")
    async def reminder(self, ctx, users, timeStr = "5", *, message="reminder"):
        
        try:
            #if in 24 hour time format
            if re.search(r"\d\d:\d\d", timeStr): #checks formatting of time given
                
                givenHourStr, givenMinuteStr = timeStr.split(":") #the numbers seperated by the : are assigned to two variables
                
                #sets the hour and minute of when the command was sent
                tz = pytz.timezone('Europe/London') #sets timezone to be used to get current hour and minute
                currentHour = datetime.now(tz).hour
                currentMinute = datetime.now(tz).minute

                #calculates the amount time that needs to pass in seconds
                hour, minute = int(givenHourStr) - currentHour, int(givenMinuteStr) - currentMinute
                time = hour*60**2 + minute*60

                await ctx.send(f"<:bell:727914124230787104> Reminder set for {timeStr} with message '{message}'")

            #if time is given in minutes
            else:

                #calculates amount of time that needs to pass in seconds
                time = int(timeStr)*60
                await ctx.send(f"<:bell:727914124230787104> Reminder set for {timeStr} minutes with message '{message}'")
            
            await asyncio.sleep(time)
            await ctx.send(f"<:bell:727914124230787104> {users} {message} *(reminder set by {ctx.message.author})*")
        except:
            
            await ctx.send("Uwu We made a fucky wucky!! A wittle fucko boingo! The code monkeys at our headquarters are working VEWY HAWD to fix this!")

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

def setup(client):
    client.add_cog(useful(client))
