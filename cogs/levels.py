#modules
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
class levels(commands.Cog):

    def __init__(self, client):  
        self.client = client
        self.dbcursor = db.cursor()
    
    async def update_levels(self, member):
        #checks if members id exists in database
        self.dbcursor.execute("SELECT memberid FROM members where memberid = %s", (member.id))
        id = self.dbcursor.fetchone()
        if not id:
            self.dbcursor.execute("INSERT INTO members (memberid, xp, level, messages) VALUES (%s, %s, %s)", (member.id, 0, 0, 0))
            db.commit()

    async def add_xp(self, member, xp):
        self.dbcursor.execute("SELECT xp FROM members WHERE memberid = %s", (member.id))
        xp += self.dbcursor[0]
        self.dbcursor.execute("UPDATE members SET xp = %s WHERE memberid = %s", (xp, member.id))
        db.commit()
    
    async def level_up(self, member, channel):
        self.dbcursor.execute("SELECT xp, level FROM members WHERE memberid = %s", (member.id))
        currentXp = self.dbcursor[0]
        currentLvl = self.dbcursor[1]
        newLvl = int(currentXp ** (1/4)) #calculates new level

        if currentLvl < newLvl:
            self.dbcursor("UPDATE members SET lvl = %s WHERE memberid = %s", (newLvl, member.id))
            db.commit()
            await channel.send(f"{member} has leveled up to level {newLvl}")

    @commands.Cog.listener()
    async def on_member_join(self, member):

        await self.update_levels(member)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot: #if member sending message isn't a bot account
            
            await self.update_levels(message.author)
            await self.add_xp(message.author, 5)
            await self.level_up(message.author, message.channel)

    @commands.command()
    async def level(self, ctx):
        
        self.dbcursor.execute("SELECT xp, level FROM members WHERE memberid = %s", (ctx.message.author.id))
        currentXp = self.dbcursor[0] #members current xp
        currentLvl = self.dbcursor[1] #members current lvl
        baseXp = currentLvl**4 #base xp of members current level
        neededXp = (currentLvl+1)**4 #xp needed to level up

        message = f"Current xp: {currentXp}\nXp for next level: {neededXp}\nCurrent level: {currentLvl} \n {baseXp} xp - | "

        #calculates amount of green and white squares the message needs
        xpTotalRange = neededXp - baseXp
        xpCurrentRange = currentXp - baseXp
        xpGreenBlocksRange = xpTotalRange/10
        num_GreenBlocks = int(xpCurrentRange/xpGreenBlocksRange)

        #add green block emojis to message
        for i in range(num_GreenBlocks):
            message += "<:green_square:728017489690099834>"

        #add white block emojis to message
        for i in range(10-num_GreenBlocks):
            message += "<:white_large_square:728029678799159397>"

        message += f" | - {neededXp} xp"

        #send message
        await ctx.send(message)

def setup(client):
    client.add_cog(levels(client))