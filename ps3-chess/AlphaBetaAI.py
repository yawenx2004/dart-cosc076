# author: @yawen_xue
# date: 1 oct. 23
# purpose: alphabeta algorithm for chess

import chess
from BONUS_AggressiveHeuristic import AggressiveHeuristic
from BONUS_Zobrist import Zobrist
from BONUS_OpeningBook import OpeningBook

class AlphaBetaAI():
    def __init__(self, depth, opening_name=""):
        self.depth = depth
        self.nodes_visited = 0
        self.better_heuristic = AggressiveHeuristic()
        self.transposition_table = {}
        self.zobrist = Zobrist()
        self.opening_book = OpeningBook()
        self.opening_name = opening_name

    def choose_move(self, board):
        """
        loops through all legal moves, evaluates each moves with alphabeta(),
        returns best move (that is, move with best score)
        :param board:
        :return:
        """
        # opening book call
        curr_moves = board.move_stack
        opening_moves = self.opening_book.get_opening(self.opening_name)

        for i in range(0, len(opening_moves)):
            if len(curr_moves) == i:
                next_move = chess.Move.from_uci(opening_moves[i])
                print("Alpha-Beta AI recommending move " + str(next_move))
                print("as per opening book")
                return next_move

        # return best_move
        best_move, best_score = self.alphabeta(board, self.depth, float('-inf'), float('inf'), False)

        print("Alpha-Beta AI recommending move " + str(best_move))
        print("after ", self.nodes_visited, " nodes explored")
        self.nodes_visited = 0  # reset
        return best_move

    def cutoff_test(self, board, depth):
        """
        stops recursion if game over or depth limit reached
        :param board:
        :param depth:
        :return:
        """
        return board.is_game_over() or depth == 0

    def alphabeta(self, board, depth, alpha, beta, maximizing_player):
        """
        # uses alpha-beta pruning to improve search efficiency; does this by
        keeping alpha and beta values to avoid exploring branches that are
        worse than the current best move
        :param board:
        :param depth:
        :param alpha:
        :param beta:
        :param maximizing_player:
        :return:
        """
        # check if position already in transposition table; if so return value that's already there
        #key = hash(str(board))
        key = self.zobrist.get_hash(board)
        if key in self.transposition_table and self.transposition_table[key]["depth"] >= depth:
            return self.transposition_table[key]["move"], self.transposition_table[key]["score"]

        # base case, stops recursion if cutoff test
        if self.cutoff_test(board, depth):
            return board.peek(), self.better_heuristic.evaluate(board)

        # during your move
        best_move = None
        if maximizing_player:
            best_score = float('-inf')

            # loops through possible moves, and uses heuristic to determine best score
            for move in board.legal_moves:
                board.push(move)
                next_move, next_score = self.alphabeta(board, depth - 1, alpha, beta, False)
                board.pop()

                if next_score > best_score:
                    best_move = move
                    best_score = next_score

                # prune worse paths
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break

            # store current data in transposition table
            self.transposition_table[key] = {
                "depth": depth,
                "move": best_move,
                "score": best_score
            }

            self.nodes_visited += 1
            return best_move, best_score

        # during opponent's move
        else:
            best_score = float('inf')

            # loops through possible moves, and uses heuristic to determine worst score
            for move in board.legal_moves:
                board.push(move)
                next_move, next_score = self.alphabeta(board, depth - 1, alpha, beta, True)
                board.pop()

                if next_score < best_score:
                    best_move = move
                    best_score = next_score

                # prune worse paths
                beta = min(beta, best_score)
                if beta <= alpha:
                    break

            # store current data in transposition table
            self.transposition_table[key] = {
                "depth": depth,
                "move": best_move,
                "score": best_score
            }

            self.nodes_visited += 1
            return best_move, best_score

    '''
    def material_value_heuristic(self, board):
        """
        material value heuristic taken from textbook; assigns value to each piece
        :param board:
        :return:
        """
        # as provided by textbook
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0}
        pieces = board.piece_map()

        # loop through pieces
        for piece in pieces.values():
            value = 0

            # if your piece, value is positive; if opponent's piece, value is negative
            if piece.color == chess.WHITE:
                value -= values.get(piece.piece_type)
            else:
                value += values.get(piece.piece_type)

        return value
    '''


