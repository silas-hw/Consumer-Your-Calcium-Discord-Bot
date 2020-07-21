from morsepy import Morsepy as mpy
import discord
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief="Encrypts english to morse", description="Returns morse code for any sentence given\nCertain special characters may not be supported, such as 'Û'")
    async def encrypt(self, ctx, string):

        try:
            cipher = mpy.encrypt(string)
            await ctx.send(f"Morse - {cipher}")
        except:
            await ctx.send("Invalid character! - for more info type `//help decrypt`")

    @commands.command(brief="Decrypts morse to english", description="Returns english for any morse given \n Each morse character should be seperated by a space and each word with /")
    async def decrypt(self, ctx, morse):

        try:
            decipher = mpy.decrypt(morse)
            await ctx.send(f"English - {decipher}")
        except:
            await ctx.send("Invalid morse character or incorrect formatting - for more info type `//help decrypt`")

def setup(client):
    client.add_cog(Fun(client))