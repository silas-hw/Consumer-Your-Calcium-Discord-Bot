from morsepy import Morsepy as mpy
import random
import discord
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief="Encrypts english to morse", description="Returns morse code for any sentence given\nCertain special characters may not be supported, such as 'Û'", usage=r"//encrypt hello world!")
    async def encrypt(self, ctx, *, string):
        try:
            cipher = mpy.encrypt(string)
            await ctx.send(f"Morse: {cipher}")
        except:
            await ctx.send("Invalid character! - for more info type `//help decrypt`")

    @commands.command(brief="Decrypts morse to english", description="Returns english for any morse given \n Each morse character should be seperated by a space and each word with /", usage=r"//decrypt .... . .-.. .-.. --- / .-- --- .-. .-.. -..")
    async def decrypt(self, ctx, *, morse):
        try:
            decipher = mpy.decrypt(morse)
            await ctx.send(f"English: {decipher}")
        except:
            await ctx.send("Invalid morse character or incorrect formatting - for more info type `//help decrypt`")

    @commands.command(brief="Flip a coin", description="Flip a coin with a random outcome of either heads or tails")
    async def flip(self, ctx):
        result = random.choice['heads', 'tails']
        await ctx.send(f"{ctx.message.author.mention} {result}")

    @commands.command()
    async def slots(self, ctx):
        emojis = ['<:1_:739605377418526830>', '<:1_:739605377418526830>', '<:1_:739605377418526830>', '<:1_:739605377418526830>',
                  '<:2_:739605426664112169>',
                  '<:3_:739605480451604601>', '<:3_:739605480451604601>', '<:3_:739605480451604601>']

        scores = {'<:1_:739605377418526830>': 5,
                  '<:2_:739605426664112169>': 10,
                  '<:3_:739605480451604601>': 20}
        score = 0
        message = f"{random.choice(emojis)} "*3
        for emoji in message.split():
            score += scores[emoji]
        message += f"\nscore - {score}"

        await ctx.send(message)


def setup(client):
    client.add_cog(Fun(client))