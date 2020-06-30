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
    async def afk(self, ctx, *, userMessage):

        #if user is already afk, remove them from the afk dict, if not add them to it
        print("test")
        if ctx.message.author in self.afkUsers:
            self.afkUsers.pop(ctx.message.author)
        else:
            self.afkUsers[ctx.message.author] = userMessage

    @commands.Cog.listener()
    async def on_message(self, message):
        
        #if a member is mentioned but the member is afk, a message is sent
        textChannel = message.channel
        afkChannel = self.client.get_channel(690550327975346176)
        
        for member in message.mentions:
            if member in self.afkUsers:
                await textChannel.send(f"{member} is afk- {self.afkUsers[member]}")
            elif member in afkChannel.members:
                await textChannel.send(f"{member} is afk")
            
        #allows commands to work with on_message event
        #await self.client.process_commands(message)
    
    #mentions a role or member after a given amount of time has passed
    @commands.command(brief="Reminds friends to play games", description="mentions role/user after given amount of minutes has passed")
    async def reminder(self, ctx, users, timeStr, *, message="reminder"):
        
        print('yeet')
        if re.search(r"\d\d:\d\d", timeStr): #checks formatting of time given
            givenHourStr, givenMinuteStr = timeStr.split(":") #the numbers seperated by the : are assigned to two variables
            givenMinuteStr = givenMinuteStr.lstrip("0") #removes leading zeros

            tz = pytz.timezone('Europe/London') #sets timezone to be used to get current hour and minute
            currentHour = datetime.now(tz).hour
            currentMinute = datetime.now(tz).minute

            hour, minute = int(givenHourStr) - currentHour, int(givenMinuteStr) - currentMinute
            time = hour*60**2 + minute*60

            await ctx.send(f"Reminder set for {timeStr} with message '{message}'")
        else:
            time = int(timeStr)*60
            await ctx.send(f"Reminder set for {time/60} minutes with message '{message}'")
        
        await asyncio.sleep(time)
        await ctx.send(f"{users} {message} *(reminder set by {ctx.message.author})*")

    

def setup(client):
    client.add_cog(useful(client))
