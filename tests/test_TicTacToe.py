# pylint: disable=import-error
import pytest
from games import TicTacToe

@pytest.fixture
def game():
    return TicTacToe()

def test_checkWin(game):

    assert game.checkWin('X') == False
    assert game.checkWin('O') == False

    for position in range(1, 4):
        game.playerMove('X', position)
    assert game.checkWin('X') == True

    with pytest.raises(ValueError):
        game.checkWin('P')

def test_checkDraw(game):
    
    assert game.checkDraw() == False

    for position in [1, 2, 6, 7, 8]:
        game.playerMove('X', position)
    
    for position in [3, 4, 5, 9]:
        game.playerMove('O', position)

    assert game.checkDraw() == True

def test_playerMove(game):

    assert game.board[0] == '-'
    game.playerMove('X', 1)
    assert game.board[0] == 'X'

def test_display(game):

    assert game.display() == '-  -  -\n-  -  -\n-  -  -\n'
    game.playerMove('X', 1)
    assert game.display() == 'X  -  -\n-  -  -\n-  -  -\n'
