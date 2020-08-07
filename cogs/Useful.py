#modules used
import re
import pytz
import asyncio
from datetime import datetime
import discord
from discord.ext import commands, tasks

class Useful(commands.Cog):
    
    def __init__(self, client):
        self.client = client

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
    async def poll(self, ctx, waitTime: str, *, text: commands.clean_content):
        
        #used to check message sent by user
        def check(m):
            return m.channel == ctx.message.channel and m.author == ctx.message.author and m.content.lower() == 'y' or m.content.lower() == 'n'

        try:

            #allow user to chose time type and use minutes as a default
            timeType = "minute(s)"
            time = 0
            if waitTime[-1].isnumeric():
                time = float(waitTime)*60
            elif waitTime[-1].lower() == "m":
                waitTime = waitTime[:-1]
                time = float(waitTime)*60
            elif waitTime[-1].lower() == "h":
                waitTime = waitTime[:-1]
                time = float(waitTime)*3600
                timeType = "hour(s)"
            elif waitTime[-1].lower() == "d":
                waitTime = waitTime[:-1]
                time = float(waitTime)*86400
                timeType = "day(s)"
            else:
                await ctx.send("⚠️ Unsupported time type")
                return 
            
            # allow 60 seconds for the user to reply, after 60 seconds an error is raised and the user is informed
            confirm_msg = await ctx.send(f"Create poll '{text}' with a wait time of {waitTime} {timeType}? (y/n)")
            user_msg = await self.client.wait_for('message', timeout=60, check=check)
            
            if user_msg.content.lower() == "y":
                
                #delete messages involved in setup
                await confirm_msg.delete()
                await ctx.message.delete()
                await user_msg.delete()

                #create message for members to react to
                pollEmbed = discord.Embed(description=f"*{waitTime} {timeType}*")
                pollEmbed.add_field(name=f"Poll by {ctx.message.author}", value=f"`{text}`")
                message = await ctx.send(embed=pollEmbed)  
                for emoji in ['👍', '👎']:
                    await message.add_reaction(emoji)
                await message.pin()

                #wait specified time
                await asyncio.sleep(time)

                #count number of reactions on message
                cache_msg = await ctx.message.channel.fetch_message(message.id)
                yes_count = cache_msg.reactions[0].count-1
                no_count = cache_msg.reactions[1].count-1

                #calculate length of percentage bars of yes votes and no votes
                total = yes_count + no_count
                yes_squares = int(yes_count/(total/10))
                yes_percent = int((yes_count/total)*100)
                no_squares = int(no_count/(total/10))
                no_percent = int((no_count/total)*100)

                #yes votes percent bar
                resultText = f"\nYes: {yes_percent}% "
                resultText += "<:blue_square:736366642719621211>"*yes_squares
                resultText += "<:white_large_square:728029678799159397>"*(10-yes_squares)

                #no votes percent bar
                resultText += f"\nNo: {no_percent}% "
                resultText += "<:red_square:736738749983227955>"*no_squares
                resultText += "<:white_large_square:728029678799159397>"*(10-no_squares)

                result = discord.Embed(title="Poll", url=message.jump_url)
                result.add_field(name=f"`{text}` by {ctx.message.author}", value=resultText)

                poll_msg = await ctx.send(embed=result)

                confirmEmbed = discord.Embed()
                confirmEmbed.add_field(name="Poll Completed", value=f"Your poll [`{text}`]({poll_msg.jump_url}) has completed\n View the results [here]({poll_msg.jump_url})")
                await ctx.author.send(embed=confirmEmbed)
            
            elif user_msg.content.lower() == "n":
               await ctx.send('Ok!, poll declined')
        
        #if they didn't reply with y or n
        except:
            embed = discord.Embed()
            embed.add_field(name="Poll Error", value=f"Your poll [`{text}`]({ctx.message.jump_url}) in the `{ctx.guild.name}` server timed out or some other error occured\nIn future, to confirm your poll type y or n")
            await ctx.author.send(embed=embed)

def setup(client):
    client.add_cog(Useful(client))