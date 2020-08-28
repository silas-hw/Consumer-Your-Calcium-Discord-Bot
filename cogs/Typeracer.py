import json
import requests
import os

import discord
from discord.ext import commands, tasks

class Typeracer(commands.Cog):

    def __init__(self, client):
        self.client = client

    @property
    def users(self):
        try:
            with open(".\\data\\typeracer\\users.json", "r") as f:
                users = json.load(f)
        except Exception as e:
            print(e)
            users = {}
        return users

    def get_userData(self, username):
        data = requests.get(f"https://data.typeracer.com/users?id=tr:{username}&universe=play")
        dataDict = json.loads(data.text)
        
        return dataDict

    @commands.group(aliases=["type", "tracer"], brief="Group of commands used for typeracer stats", description="Used to check your typeracer stats against other server members", usage=r"//typeracer set, //typeracer wpm, //typeracer leaderboard")
    async def typeracer(self, ctx):
        users = self.users
        get_userData = self.get_userData
        client = self.client

    @typeracer.command(brief="Check your typeracer wpm", description="Gets your average wpm from your typeracer account")
    async def wpm(self, ctx):
        try:
            username = self.users[str(ctx.message.author.id)]
            
            userData = self.get_userData(username)
            wpm = userData['tstats']['wpm']
            
            await ctx.send(f"{ctx.message.author.mention}: {int(wpm)}")
        except KeyError:
            await ctx.send("⚠️ You're discord account does not have a typeracer username linked to it. To do so user `//typeracer set`")

    @typeracer.command(name="set", brief="Set your typeracer username", description="Set your typeracer username to be tied to your discord account, if the username is already being used you cannot use it", usage=r"//typeracer set <username>")
    async def setUsername(self, ctx, username):
        
        #ensure a username can only be used by one person
        if username not in self.users.values():
            self.users[str(ctx.message.author.id)] = username
            print(self.users)
            with open(".\\data\\typeracer\\users.json", "w") as f:
                json.dump(self.users, f, indent=4)
            await ctx.send(f"Username now set to {username}")
        else:
            await ctx.send("That username is already being used")

    @commands.guild_only()
    @typeracer.command(aliases=["leader"], brief="Display a typeracer leaderboard", description="Displays a leaderboard of all members who have tied a typeracer username to their account")
    async def leaderboard(self, ctx):
        users_list = []
        for user in self.users:
            membername = ctx.guild.get_member(int(user))

            #only adds user if they exist in the guild
            if membername:
                username = self.users[user]
                userdata = self.get_userData(username)
                wpm = userdata['tstats']['wpm']

                users_list.append([membername, wpm])

        users_list.sort(key=lambda x: x[1], reverse=True)

        msg = discord.Embed(title="Typeracer Leaderboard")
        for index, user in enumerate(users_list):
            wpm = int(user[1])
            name = user[0]
            msg.add_field(name=f"**{index+1}**:  {name}", value=f"`wpm: {wpm}`\n", inline=False)

        await ctx.send(embed=msg)
            
def setup(client):
    client.add_cog(Typeracer(client))