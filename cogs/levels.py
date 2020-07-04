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
        self.dbcursor = db.cursor(buffered=True)
    
    async def update_levels(self, member):
        #checks if members id exists in database
        self.dbcursor.execute(f"SELECT memberid FROM members WHERE memberid = {member.id}")
        id = self.dbcursor.fetchone()
        if not id:
            self.dbcursor.execute("INSERT INTO members (memberid, xp, level, messages) VALUES (%s, %s, %s, %s)", (member.id, 0, 0, 0))
            db.commit()

    async def add_xp(self, member, xp):
        self.dbcursor.execute(f"SELECT xp FROM members WHERE memberid = {member.id}")
        for value in self.dbcursor:
            xp += value[0]
        self.dbcursor.execute(f"UPDATE members SET xp = {xp} WHERE memberid = {member.id}")
        db.commit()
    
    async def level_up(self, member, channel):
        self.dbcursor.execute(f"SELECT xp, level FROM members WHERE memberid = {member.id}")
        for value in self.dbcursor:
            currentXp = value[0]
            currentLvl = value[1]
        newLvl = int(currentXp ** (1/4)) #calculates new level

        if currentLvl < newLvl:
            self.dbcursor.execute(f"UPDATE members SET level = {newLvl} WHERE memberid = {member.id}")
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
        
        self.dbcursor.execute(f"SELECT xp, level FROM members WHERE memberid = {ctx.message.author.id}")
        for value in self.dbcursor:
            currentXp = value[0] #members current xp
            currentLvl = value[1] #members current lvl
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
    
    @commands.command()
    async def addMemberNames(self, ctx):

        self.dbcursor.execute("SELECT memberid FROM members")

        for memberid in self.dbcursor:
            print(memberid)
            memberName = str(ctx.message.guild.get_member(memberid[0]))
            self.dbcursor.execute(f"UPDATE members SET username = '{memberName}' WHERE member id = {memberid[0]}")
            db.commit()

            print(memberName) #for testing

def setup(client):
    client.add_cog(levels(client))