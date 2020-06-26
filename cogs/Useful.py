#modules used
import asyncio
import discord
from discord.ext import commands

class Useful(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief="Reminds friends to play games", description="mentions role/user after given amount of minutes has passed\nTo send a multiword message wrap the message with quotes")
    async def reminder(self, ctx, users, timeStr, message="reminder"):
        
        time = int(timeStr)
        await ctx.send(f"Reminder set for {time} minutes with message '{message}'")
        await asyncio.sleep(time*60)
        await ctx.send(f"{users} {message} *(reminder set by {ctx.message.author})*")

def setup(client):
    client.add_cog(Useful(client))
