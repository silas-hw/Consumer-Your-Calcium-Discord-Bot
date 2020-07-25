#modules used
import re
import pytz
import asyncio
from datetime import datetime
import discord
from discord.ext import commands, tasks

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.afkUsers = {}

    #allows a user to set them self as afk
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

    @commands.command(brief="Make a poll and have the results given after a certain amount of time", description="Make a poll that can people can vote yes or no to\nYou give the time in minutes the poll should remain active followed by what the poll is about", usage=r"//poll 5 Haha brrrrr?")
    async def poll(self, ctx, waitTime: float, *, text):
        
        #used to check message sent by user
        def check(m):
            return m.channel == ctx.message.channel and m.author == ctx.message.author and m.content.lower() == 'y' or m.content.lower() == 'n'

        try:
            confirm_msg = await ctx.send(f"Create poll '{text}' with wait time {waitTime} minutes? (y/n)")
            user_msg = await self.client.wait_for('message', timeout=60, check=check)
            if user_msg.content.lower() == "y":
                await confirm_msg.delete()
                await ctx.message.delete()
                await user_msg.delete()

                pollEmbed = discord.Embed()
                pollEmbed.add_field(name=f"Poll by {ctx.message.author}", value=text)
                message = await ctx.send(embed=pollEmbed)  
                for emoji in ['👍', '👎']:
                    await message.add_reaction(emoji)

                await asyncio.sleep(waitTime*60)

                #count number of reactions on message
                cache_msg = await ctx.message.channel.fetch_message(message.id)
                yes_count = cache_msg.reactions[0].count-1
                no_count = cache_msg.reactions[1].count-1

                #add percent bars to result message
                total = yes_count + no_count
                yes_squares = int(yes_count/(total/10))
                yes_percent = int((yes_count/total)*100)
                no_squares = int(no_count/(total/10))
                no_percent = int((no_count/total)*100)

                resultText = f"\nYes: {yes_percent}% "
                for _ in range(yes_squares):
                    resultText += "<:blue_square:736366642719621211>"
                for _ in range(10-yes_squares):
                    resultText += "<:white_large_square:728029678799159397>"

                resultText += f"\nNo: {no_percent}% "
                for _ in range(no_squares):
                    resultText += "<:green_square:728017489690099834>"
                for _ in range(10-no_squares):
                    resultText += "<:white_large_square:728029678799159397>"

                result = discord.Embed(title="Poll", url=message.jump_url)
                result.add_field(name=f"`{text}` by {ctx.message.author}", value=resultText)

                poll_msg = await ctx.send(embed=result)

                confirmEmbed = discord.Embed()
                confirmEmbed.add_field(name="Poll Completed", value=f"Your poll [`{text}`]({poll_msg.jump_url}) has completed\n View the results [here]({poll_msg.jump_url})")
                await ctx.author.send(embed=confirmEmbed)
            
        except:
            embed = discord.Embed()
            embed.add_field(name="Poll Error", value=f" Your poll [`{text}`]({ctx.message.jump_url}) in the `{ctx.guild.name}` server timed out or some other error occured\nIn future, to confirm your poll type y or n")
            await ctx.author.send(embed=embed)

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

    #gives them the role mentioned for announcements
    @commands.command(aliases=['ping'], brief="get pinged for announcements", description="give you the *consumer* role, which is pinged for announcements and updates")
    async def pingme(self, ctx):

        role = ctx.guild.get_role(732354594536947803)
        await ctx.message.author.add_roles(role, reason=f'{ctx.message.author.name} now pinged for announcements')
        await ctx.send("You'll now be pinged for announcements in <#684458229090353222>")

    #react to the message before the command with a given set of emojis
    @commands.command(aliases=['r'], brief="reacts to messages", description="Reacts to the previous message sent\nThe message used to invoke the command is deleted", usage=r"//react epic")
    async def react(self, ctx, reaction='epic'):

        await ctx.message.delete()

        reactions = {
            'epic': ['🇪', '🇵', '🇮', '🇨'],
            'lmao': ['🇱', '🇲', '🇦',  '🇴'],
            'pride': ['🏳️‍🌈', '🌈', '❤️' ,'🧡', '💛' ,'💚' ,'💙' ,'💜', '🖤', '🤎', '🤍'],
            'shy': ['🥺', '👉', '👈']
        }

        messageHistory = await ctx.channel.history(limit=2).flatten()

        for emoji in reactions[reaction.lower()]:
            await messageHistory[0].add_reaction(emoji)

def setup(client):
    client.add_cog(Misc(client))
