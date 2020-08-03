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
        await ctx.send(f"{ctx.message.author.mention} {random.choice(['heads', 'tails'])}")

    @commands.command(brief="Roll a dice", description="Roll a dice with any number of sides")
    async def roll(self, ctx, type="d6"):
        try:
            range = int(type[1:])
            await ctx.send(f"{ctx.message.author.mention} 🎲{random.randint(1, range)}")
        except ValueError:
            await ctx.send("Invalid dice type. To give a type use d[number of sides] *(e.g d8)*")

    @commands.command()
    async def slots(self, ctx):
        emojis = ['<:max:719639562678173769>', '<:max:719639562678173769>', '<:max:719639562678173769>', '<:max:719639562678173769>',
                  '<:curvearm:719639190836346973>',
                  '<:silas:719639912147845261>', '<:silas:719639912147845261>', '<:silas:719639912147845261>']

        scores = {'<:max:719639562678173769>': 5,
                  '<:silas:719639912147845261>': 10,
                  '<:curvearm:719639190836346973>': 20}
        score = 0

        result = [random.choice(emojis) for _ in range(3)]

        for emoji in result:
            score += scores[emoji]
        message = f">{result[0]} {result[1]} {result[2]}<\n`score - {score}`"

        await ctx.send(message)


def setup(client):
    client.add_cog(Fun(client))