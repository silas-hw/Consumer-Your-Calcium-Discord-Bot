import logging
import discord
from discord.ext import commands

#games
from games import TicTacToe

logging.basicConfig(level=logging.INFO, filename='log.log', format="[%(asctime)s]%(levelname)s:%(module)s~ %(message)s")

class Games(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ttt'], brief="Tic tac toe", description="Play a game of tic tac toe", usage=r"//ttt <player2>")
    async def tic_tac_toe(self, ctx, player2: discord.Member):

        def _confirm_reply(m):
            return m.channel == ctx.message.channel and m.author == player2 and m.content.lower() in ['y', 'n']
        await ctx.send(f"{player2.mention} play a game of tic tac toe with {ctx.message.author}?")
        reply_msg = await self.client.wait_for('message', timeout=40.0, check =_confirm_reply)
        if reply_msg.content == 'n':
            await ctx.send('Ok!, game cancelled')
            return
        
        def _move_reply(m):
            return m.channel == ctx.message.channel and m.author == players[player] and m.content in [str(x) for x in range(1, 10)]

        player = 'O'
        player1 = ctx.message.author
        players = {
            'X': player1,
            'O': player2,
        }

        game = TicTacToe()

        await ctx.send(game.rules)
        await ctx.send(f"{player1.mention} ~ X\n{player2.mention} ~ O")

        while True:
            player = 'O' if player == 'X' else 'X'

            while True:
                try:
                    await ctx.send(f"{players[player].mention}: enter a position")
                    reply_msg = await self.client.wait_for('message', timeout=40.0, check=_move_reply)
                    
                    position = int(reply_msg.content)
                    game.playerMove(player, position)
                    
                    break
                except ValueError:
                    await ctx.send(f"{players[player].mention} Invalid move")

            await ctx.send(game.display())

            if game.checkWin(player):
                await ctx.send(f"{players[player].mention} won!")
                break
            if game.checkDraw():
                await ctx.send(f"{players['X'].mention} {players['O'].mention} Draw!")
                break

def setup(client):
    client.add_cog(Games(client))