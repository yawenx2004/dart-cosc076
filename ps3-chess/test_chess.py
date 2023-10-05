# pip3 install python-chessg


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame

import sys

player1 = HumanPlayer()
player2 = RandomAI()
player3 = MinimaxAI(4, "iterative")
player4 = MinimaxAI(3, "non-iterative")
player5 = AlphaBetaAI(4)
player6 = AlphaBetaAI(3)
player7 = AlphaBetaAI(4, "italian_game")
player8 = AlphaBetaAI(3, "italian_game")

# human vs. minimax
#game = ChessGame(player1, player4)

# human vs. iterative minimax
#game = ChessGame(player1, player3)

# human vs. alphabeta
#game = ChessGame(player5, player1)

# alphabeta vs. random
#game = ChessGame(player6, player2)

# alphabeta deeper vs. shallower
#game = ChessGame(player5, player6)

# alphabeta deeper vs. shallower, with opening book
game = ChessGame(player7, player8)


while not game.is_game_over():
    print(game)
    game.make_move()


#print(hash(str(game.board)))
