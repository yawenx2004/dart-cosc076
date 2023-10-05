# author: @yawen_xue
# date: 29 sep. 23
# purpose: minimax algorithm for chess

import chess
from BONUS_AggressiveHeuristic import AggressiveHeuristic

class MinimaxAI():
    def __init__(self, depth, version):
        self.depth = depth
        self.nodes_visited = 0
        self.version = version
        self.better_heuristic = AggressiveHeuristic()
        self.transposition_table = {}

    def choose_move(self, board):
        """
        loops through all legal moves, evaluates each moves with minimax(),
        returns best move (that is, move with best score); has a switch for
        toggling between iterative and non-iterative versions
        :param board:
        :return:
        """
        # iterative version
        if self.version == "iterative":
            best_move = None

            # runs with different depths until depth increments to max depth
            for curr_depth in range(1, self.depth + 1):
                best_move, best_score = self.minimax(board, curr_depth, False)
                print("Depth: ", curr_depth, "\tBest move: ", best_move)

            print("Iterative Minimax AI recommending move " + str(best_move))
            print("after ", self.nodes_visited, " nodes explored")
            self.nodes_visited = 0  # reset
            return best_move

        # non-iterative version
        elif self.version == "non-iterative":
            best_move, best_score = self.minimax(board, self.depth, False)

            print("Minimax AI recommending move " + str(best_move))
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

    def minimax(self, board, depth, maximizing_player):
        """
        recursive minimax algorithm, explores game tree to select best move
        based on the criteria of maximizing your score and minimizing opponent's
        score
        :param board:
        :param depth:
        :param maximizing_player:
        :return:
        """
        # check if position already in transposition table; if so return value that's already there
        key = hash(str(board))
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
                next_move, next_score = self.minimax(board, depth - 1, False)
                board.pop()

                if next_score > best_score:
                    best_move = move
                    best_score = next_score

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
                next_move, next_score = self.minimax(board, depth - 1, True)
                board.pop()

                if next_score < best_score:
                    best_move = move
                    best_score = next_score

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