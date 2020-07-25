#modules
import asyncio
import mysql.connector
import json
import discord
from discord.ext import commands, tasks

with open("sqlpasswords.json", "r") as f:
    passwords = json.load(f)

db = mysql.connector.connect (
    host="johnny.heliohost.org",
    user="silashw_user1",
    passwd=passwords['profiles'],
    database="silashw_levelsData"
)

class Profiles(commands.Cog):

    def __init__(self, client):  
        self.client = client
        self.dbcursor = db.cursor(buffered=True)

    #when the bot is ready start the sqlreconnect2 task
    @commands.Cog.listener()
    async def on_ready(self):

        # pylint: disable=no-member
        self.sqlreconnect2.start()

    #updates users twitter handle in MySQL database
    @commands.command(brief="Adds your twitter feed to the website", description="Adds your twitter handle to the database so your feed appears on your profile on the website\nSimply type your twitter handle *(without @)* after the command", usage=r"//twitter silas_hw")
    async def twitter(self, ctx, handle):

        self.dbcursor.execute(f"UPDATE members SET twitter = '{handle}' WHERE memberid = {ctx.message.author.id}" )
        db.commit()

        await ctx.send("<:ballot_box_with_check:730138696069939331> twitter handle updated!")

    #adds pinned message to be shown on membe
    @commands.command(brief="Pin a message!", description="Pins a message to be displayed ors profilen your profile on the website\nThe maximum character length is 50", usage=r"//pin UwU")
    async def pin(self, ctx, *, message):

        if len(message) > 50:
            await ctx.send("Message must be 50 characters or less")
        else:
            self.dbcursor.execute(f"UPDATE members SET pinned = '{message}' WHERE memberid = {ctx.message.author.id}")
            db.commit()

            await ctx.send(f"<:pushpin:731608868420845608> *'{message}'* pinned!")

    #adds pinned image to be displayed on the website
    @commands.command(brief="Add an image to your profile!", description="Adds an image to be displayed on your profile page on the website\n The image *will* be stretched", usage=r"//image <attachement>")
    async def image(self, ctx):

        imageUrl = ctx.message.attachments[0].url
        self.dbcursor.execute(f"UPDATE members SET pinnedImage = '{imageUrl}' WHERE memberid = {ctx.message.author.id}")
        db.commit()

        await ctx.send("Image added!")

    #reconnects to the sql server every 2 hours
    @tasks.loop(seconds=7200)
    async def sqlreconnect2(self):
        
        #create sql connection
        db.reconnect(attempts=10, delay=0)

        #update dbcursor
        self.dbcursor = db.cursor(buffered=True)

        print('\n Profiles cog reconnected to MySql server\n')

def setup(client):
    client.add_cog(Profiles(client))