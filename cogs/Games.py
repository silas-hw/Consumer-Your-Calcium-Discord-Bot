import discord
from discord.ext import commands

#games
from games import TicTacToe


class Games(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ttt'])
    async def tic_tac_toe(self, ctx, player2: discord.Member):

        player = 'O'

        def _reply(m):
            return m.channel == ctx.message.channel and m.author == players[player] and m.content in [str(x) for x in range(1, 10)]

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
                    reply_msg = await self.client.wait_for('message', timeout=40.0, check=_reply)
                    
                    position = int(reply_msg.content)
                    game.playerMove(player, position)
                    
                    break
                except:
                    await ctx.send("Invalid move")

            await ctx.send(game.display())

            if game.checkWin(player):
                await ctx.send(f"{players[player].mention} won!")
                break

            



def setup(client):
    client.add_cog(Games(client))