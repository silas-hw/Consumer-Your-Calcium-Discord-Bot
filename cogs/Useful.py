#modules used
import re
import pytz
from datetime import datetime
import asyncio
import discord
from discord.ext import commands

class Useful(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief="Reminds friends to play games", description="mentions role/user after given amount of minutes has passed\nTo send a multiword message wrap the message with quotes")
    async def reminder(self, ctx, users, timeStr, message="reminder"):
        
        if re.search(r"\d\d:\d\d", timeStr):
            givenHourStr, givenMinuteStr = timeStr.split(":")
            givenMinuteStr = givenMinuteStr.lstrip("0") #removes leading zeros

            tz = pytz.timezone('GMT') #sets timezone to be used to get current hour and minute
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
    client.add_cog(Useful(client))
