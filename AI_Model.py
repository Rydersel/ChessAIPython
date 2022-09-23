import board
from ChessAI import Pieces
import numpy


class Point_Tables:

    #Assigns score to each move for each piece.
    #Using numpy for array managment
    PAWN_TABLE = numpy.array([
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    KNIGHT_TABLE = numpy.array([
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-30,   5,  10,  15,  15,  10,   5, -30],
        [-30,   0,  15,  20,  20,  15,   0, -30],
        [-30,   5,  15,  20,  20,  15,   0, -30],
        [-30,   0,  10,  15,  15,  10,   0, -30],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ])

    BISHOP_TABLE = numpy.array([
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-10,  10,  10,  10,  10,  10,  10, -10],
        [-10,   0,  10,  10,  10,  10,   0, -10],
        [-10,   5,   5,  10,  10,   5,   5, -10],
        [-10,   0,   5,  10,  10,   5,   0, -10],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ])

    ROOK_TABLE = numpy.array([
        [ 0,  0,  0,  5,  5,  0,  0,  0],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    QUEEN_TABLE = numpy.array([
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10,   0,   5,  0,  0,   0,   0, -10],
        [-10,   5,   5,  5,  5,   5,   0, -10],
        [  0,   0,   5,  5,  5,   5,   0,  -5],
        [ -5,   0,   5,  5,  5,   5,   0,  -5],
        [-10,   0,   5,  5,  5,   5,   0, -10],
        [-10,   0,   0,  0,  0,   0,   0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ])

    @staticmethod
    def evaluate(board):
        material = Point_Tables.get_material_score(board)

        pawns = Point_Tables.get_piece_position_score(board, Pieces.Pawn.PIECE_TYPE, Point_Tables.PAWN_TABLE)

        knights = Point_Tables.get_piece_position_score(board, Pieces.Knight.PIECE_TYPE, Point_Tables.KNIGHT_TABLE)

        bishops = Point_Tables.get_piece_position_score(board, Pieces.Bishop.PIECE_TYPE, Point_Tables.BISHOP_TABLE)

        rooks = Point_Tables.get_piece_position_score(board, Pieces.Rook.PIECE_TYPE, Point_Tables.ROOK_TABLE)

        queens = Point_Tables.get_piece_position_score(board, Pieces.Queen.PIECE_TYPE, Point_Tables.QUEEN_TABLE)

        return material + pawns + knights + bishops + rooks + queens

    # Returns the score for the position of the given type of piece.

    # The table is the 2d numpy array used for the scoring. Ex: Point_Tables.PAWN_TABLE
    @staticmethod
    def get_piece_position_score(board, piece_type, table):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                piece = board.chesspieces[x][y]
                if (piece != 0):
                    if (piece.piece_type == piece_type):
                        if (piece.color == Pieces.Piece.WHITE):
                            white += table[x][y]
                        else:
                            black += table[7 - x][y]

        return white - black

    @staticmethod
    def get_material_score(board):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                piece = board.chesspieces[x][y]
                if (piece != 0):
                    if (piece.color == Pieces.Piece.WHITE):
                        white += piece.value
                    else:
                        black += piece.value

        return white - black


class AI:

    INFINITE = 10000000

    @staticmethod
    def get_ai_move(chessboard, invalid_moves):
        best_move = 0
        best_score = AI.INFINITE
        for move in chessboard.get_possible_moves(Pieces.Piece.BLACK):
            if (AI.is_invalid_move(move, invalid_moves)):
                continue

            copy = board.Board.clone(chessboard)
            copy.perform_move(move)

            score = AI.alphabeta(copy, 2, -AI.INFINITE, AI.INFINITE, True)
            if (score < best_score):
                best_score = score
                best_move = move

        #If Checkmate
        if (best_move == 0):
            return 0

        copy = board.Board.clone(chessboard)
        copy.perform_move(best_move)

        if (copy.is_check(Pieces.Piece.BLACK)):
            invalid_moves.append(best_move)
            return AI.get_ai_move(chessboard, invalid_moves)

        return best_move

    @staticmethod
    def is_invalid_move(move, invalid_moves):
        for invalid_move in invalid_moves:
            if (invalid_move.equals(move)):
                return True
        return False

    @staticmethod
    def minimax(board, depth, maximizing):
        if (depth == 0):
            return Point_Tables.evaluate(board)

        if (maximizing):
            best_score = -AI.INFINITE
            for move in board.get_possible_moves(Pieces.Piece.WHITE):
                copy = board.Board.clone(board)
                copy.perform_move(move)

                score = AI.minimax(copy, depth-1, False)
                best_score = max(best_score, score)

            return best_score
        else:
            best_score = AI.INFINITE
            for move in board.get_possible_moves(Pieces.Piece.BLACK):
                copy = board.Board.clone(board)
                copy.perform_move(move)

                score = AI.minimax(copy, depth-1, True)
                best_score = min(best_score, score)

            return best_score

    @staticmethod
    def alphabeta(chessboard, depth, a, b, maximizing):
        if (depth == 0):
            return Point_Tables.evaluate(chessboard)

        if (maximizing):
            best_score = -AI.INFINITE
            for move in chessboard.get_possible_moves(Pieces.Piece.WHITE):
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)

                best_score = max(best_score, AI.alphabeta(copy, depth-1, a, b, False))
                a = max(a, best_score)
                if (b <= a):
                    break
            return best_score
        else:
            best_score = AI.INFINITE
            for move in chessboard.get_possible_moves(Pieces.Piece.BLACK):
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)

                best_score = min(best_score, AI.alphabeta(copy, depth-1, a, b, True))
                b = min(b, best_score)
                if (b <= a):
                    break
            return best_score


class Move:

    def __init__(self, x_from, y_from, x_to, y_to, castling_move):
        self.x_from = x_from
        self.y_from = y_from
        self.x_to = x_to
        self.y_to = y_to
        self.castling_move = castling_move

    # Returns true if (x_from,y_from) and (x_to,y_to) are the same.
    def equals(self, other_move):
        return self.x_from == other_move.x_from and self.y_from == other_move.y_from and self.x_to == other_move.x_to and self.y_to == other_move.y_to

    def to_string(self):
        return "(" + str(self.x_from) + ", " + str(self.y_from) + ") -> (" + str(self.x_to) + ", " + str(self.y_to) + ")"
