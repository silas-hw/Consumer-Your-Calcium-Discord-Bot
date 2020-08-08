#modules
import logging
import asyncio
import mysql.connector
import json
import discord
from discord.ext import commands, tasks

#checks
from checks import Muted

with open("sqlpasswords.json", "r") as f:
    passwords = json.load(f)

db = mysql.connector.connect (
    host="johnny.heliohost.org",
    user="silashw_user2",
    passwd=passwords['levels'],
    database="silashw_levelsData"
)
class Levels(commands.Cog):

    def __init__(self, client):  
        self.client = client
        self.dbcursor = db.cursor(buffered=True)

    @commands.Cog.listener()
    async def on_ready(self):
        
        # pylint: disable=no-member
        self.sqlreconnect.start() 
    
    async def update_levels(self, member):
        
        #checks if members id exists in database
        self.dbcursor.execute(f"SELECT memberid FROM members WHERE memberid = {member.id}")
        
        #update the profile url of the member if they're are not in the database, add them.
        id = self.dbcursor.fetchone()
        if not id:
            self.dbcursor.execute("INSERT INTO members (username, memberid, xp, level, messages, pic_url) VALUES (%s, %s, %s, %s, %s, %s)", (str(member.name), member.id, 0, 0, 0, str(member.avatar_url)))
            db.commit()
        else:
            self.dbcursor.execute(f"UPDATE members SET pic_url= '{str(member.avatar_url)}' WHERE memberid = {member.id}")

    async def add_xp(self, member, xp):
        
        #find the xp value of the member and add passed xp to it, then update databse with new value
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
    @Muted.check()
    async def on_message(self, message):
        if not message.author.bot and Muted.not_muted(message.guild.id, message.author.id): #if member sending message isn't a bot account

            await asyncio.sleep(2) #wait a minute to avoid sql error
            
            await self.update_levels(message.author)
            await self.add_xp(message.author, 5)
            await self.level_up(message.author, message.channel)

    @commands.command(brief="Displays information about your level", description="Displays level and xp information alonside a nifty progress bar", usage=r"//level")
    @Muted.check()
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
        for _ in range(num_GreenBlocks):
            message += "<:green_square:728017489690099834>"

        #add white block emojis to message
        for _ in range(10-num_GreenBlocks):
            message += "<:white_large_square:728029678799159397>"

        message += f" | - {neededXp} xp"

        #send message
        await ctx.send(message)

    #reconnects to the sql server every 2 hours
    @tasks.loop(seconds=7200)
    async def sqlreconnect(self):
        
        db.reconnect(attempts=10, delay=0)
        self.dbcursor = db.cursor(buffered=True)

        logging.info('Levels cog reconnected to MySql server')

def setup(client):
    client.add_cog(Levels(client))