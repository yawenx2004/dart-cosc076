# author: @yawen_xue
# date: 3 oct. 23
# purpose: zobrist hashing function

import chess
import random

class Zobrist():
    def __init__(self):
        self.piece_at_square = {}                   # dictionary for each piece-square combination
        self.side_to_move = random.getrandbits(64)  # represents which side moves

        # each piece type; there are 6
        for piece_type in range(0, 6):

            # for each square, assign bit
            for square in chess.SQUARES:
                key = random.getrandbits(64)
                self.piece_at_square[(piece_type, square)] = key

    def get_hash(self, board):
        """
        calculates hash using XOR
        :param board:
        :return:
        """
        hash_key = 0

        # loops through squares on board
        for square in chess.SQUARES:
            piece = board.piece_at(square)

            # for occupied squares, XOR key
            if piece is not None:
                piece_type = piece.piece_type - 1
                hash_key ^= self.piece_at_square[(piece_type, square)]

        # XOR side_to_move key into hash key
        if board.turn == chess.WHITE:
            hash_key ^= self.side_to_move

        return hash_key
