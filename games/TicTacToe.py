class TicTacToe():

    def __init__(self):

        self.rules = "The game follows a grid of:\n1 2 3\n4 5 6\n7 8 9\nTo pick a position type its relative number"
        self.board = ['-','-','-',
                      '-','-','-',
                      '-','-','-']
    
    @staticmethod
    def _check_player(player):
        if player not in ['X', 'O']:
            raise ValueError("Player argument must be either 'X' or 'O'")

    @staticmethod
    def _check_position(position: int):
        if position not in range(0, 9):
            raise ValueError("Position given is invalid")

    def display(self):
        board=self.board
        output = f'{board[0]}  {board[1]}  {board[2]}\n'
        output += f'{board[3]}  {board[4]}  {board[5]}\n'
        output += f'{board[6]}  {board[7]}  {board[8]}\n'

        return output
    
    def checkWin(self, player):
        
        self._check_player(player)
        
        board = self.board
        win_positions = [
        [board[0], board[1], board[2]],
        [board[3], board[4], board[5]],
        [board[6], board[7], board[8]],
        [board[0], board[3], board[6]],
        [board[1], board[4], board[7]],
        [board[2], board[5], board[8]],
        [board[0], board[4], board[8]],
        [board[2], board[4], board[6]]
        ]

        for position in win_positions:
            if position == [player, player, player]:
                return True

        return False

    def playerMove(self, player, position: int):

        self._check_player(player)
        self._check_position(position-1)

        if self.board[position-1] != '-':
            raise ValueError("Position taken")

        self.board[position-1] = player

if __name__ == "__main__":
    
    game = TicTacToe()
    print(game.rules)
    player = 'X'
    while True:
        player = 'O' if player == 'X' else 'X' #switch player
        while True:

            try:
                move = input(f"{player}: Choose a position ")
                if move == "rules":
                    print(game.rules)
                else:
                    game.playerMove(player, int(move))
                    break
            except:
                print("Invalid move, try again")
                
        print(game.display())
        if game.checkWin(player):
            print(f"{player} won!")
            break



