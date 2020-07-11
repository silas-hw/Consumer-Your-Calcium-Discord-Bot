#modules
import asyncio
import mysql.connector
import json
import discord
from discord.ext import commands

db = mysql.connector.connect (
    host="johnny.heliohost.org",
    user="silashw",
    passwd="elephantCode88",
    database="silashw_levelsData"
)

class profiles(commands.Cog):

    def __init__(self, client):  
        self.client = client
        self.dbcursor = db.cursor(buffered=True)

    #updates users twitter handle in MySQL database
    @commands.command(brief="Adds your twitter feed to the website", description="Adds your twitter handle to the database so your feed appears on your profile on http://silashw.heliost.org/\nSimply type your twitter handle *(without @)* after the command")
    async def twitter(self, ctx, handle):

        self.dbcursor.execute(f"UPDATE members SET twitter = '{handle}' WHERE memberid = {ctx.message.author.id}" )
        db.commit()

        await ctx.send("<:ballot_box_with_check:730138696069939331> twitter handle updated!")

    #adds pinned message to be shown on members profile
    @commands.command(brief="Pin a message!")
    async def pin(self, ctx, *, message):

        if len(message) > 50:
            await ctx.send("Message must be 50 characters or less")
        else:
            self.dbcursor.execute(f"UPDATE members SET pinned = '{message}' WHERE memberid = {ctx.message.author.id}")
            db.commit()

def setup(client):
    client.add_cog(profiles(client))