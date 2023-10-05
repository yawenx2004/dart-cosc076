# author: @yawen_xue
# date: 3 oct. 23
# purpose: better heuristic -- material heuristic provided by the textbook is very passive

import chess

class AggressiveHeuristic():
    def __init__(self):
        # as provided by textbook, plus my modification for king
        self.material_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 100
        }

    def evaluate(self, board):
        """
        evaluates score for each move; favors capturing opponent's pieces
        :param board:
        :return:
        """
        score = 0

        # loop through pieces and get value
        pieces = board.piece_map()
        for square, piece in pieces.items():
            if piece.color == chess.WHITE:
                score -= self.material_values.get(piece.piece_type)
            else:
                score += self.material_values.get(piece.piece_type)

        # factor in captures
        for move in list(board.generate_legal_captures()):
            capture = board.piece_at(move.to_square)
            if capture:

                # add to score if you capture
                score += self.material_values.get(capture.piece_type)

        return score