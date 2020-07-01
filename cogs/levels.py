#modules
import json
import discord
from discord.ext import commands

class levels(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @staticmethod
    async def update_levels(file, member):
        if not str(member.id) in file:
            file[str(member.id)] = {}
            file[str(member.id)]['xp'] = 0
            file[str(member.id)]['lvl'] = 0

    @staticmethod
    async def add_xp(file, member, xp):
        file[str(member.id)]['xp'] += xp
    
    @staticmethod
    async def level_up(file, member, channel):
        currentXp = file[str(member.id)]['xp']
        currentLvl = file[str(member.id)]['lvl']
        newLvl = int(currentXp ** (1/4)) #calculates new level

        if currentLvl < newLvl:
            file[str(member.id)]['lvl'] = newLvl
            await channel.send(f"{member} has leveled up to level {newLvl}")

    @commands.command()
    async def manualLevelUpdate(self, ctx):
        with open("./cogs/levelsData.json", "r") as f:
            levelsData = json.load(f)

        for member in ctx.guild.members:
            await self.update_levels(levelsData, member)

        with open("./cogs/levelsData.json", "w") as f:
            json.dump(levelsData, f)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("./cogs/levelsData.json", "r") as f:
            levelsData = json.load(f)

        await self.update_levels(levelsData, member)

        with open("./cogs/levelsData.json", "w") as f:
            json.dump(levelsData, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot: #if member sending message isn't a bot account
            with open("./cogs/levelsData.json", "r") as f:
                levelsData = json.load(f)
            
            await self.update_levels(levelsData, message.author)
            await self.add_xp(levelsData, message.author, 5)
            await self.level_up(levelsData, message.author, message.channel)

            with open("./cogs/levelsData.json", "w") as f:
                json.dump(levelsData, f)

    
    @commands.command()
    async def level(self, ctx):

        with open("./cogs/levelsData.json", "r") as f:
            levelsData = json.load(f)
        
        currentXp = levelsData[str(ctx.author.id)]['xp'] #members current xp
        currentLvl = levelsData[str(ctx.author.id)]['lvl'] #members current lvl
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