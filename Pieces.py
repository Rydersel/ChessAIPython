import AI_Model
from Piece_Class import Piece






#Core Written by dirk (Made some small tweaks)


class Queen(Piece):

    PIECE_TYPE = "♕"


    def __init__(self, x, y, color, weight=900):
        super(Queen, self).__init__(x, y, color, Queen.PIECE_TYPE, weight)
        self.VALUE = weight
    def get_possible_moves(self, board):
        diagonal = self.diag_pos(board)
        horizontal = self.get_possible_horizontal_moves(board)
        return horizontal + diagonal

    def clone(self):
        return Queen(self.x, self.y, self.color)


class Rook(Piece):
    PIECE_TYPE = "♖"
    def __init__(self, x, y, color, weight=250):
        super(Rook, self).__init__(x, y, color, Rook.PIECE_TYPE, weight)
        self.VALUE = weight

    def get_possible_moves(self, board):
        return self.get_possible_horizontal_moves(board)

    def clone(self):
        return Rook(self.x, self.y, self.color)



class Bishop(Piece):
    PIECE_TYPE = "♗"


    def __init__(self, x, y, color, weight=350):
        super(Bishop, self).__init__(x, y, color, Bishop.PIECE_TYPE, weight)
        self.VALUE = weight
    def get_possible_moves(self, board):
        return self.diag_pos(board)

    def clone(self):
        return Bishop(self.x, self.y, self.color)



class Knight(Piece):

    PIECE_TYPE = "♘"

    def __init__(self, x, y, color, weight=320):
        super(Knight, self).__init__(x, y, color, Knight.PIECE_TYPE, weight)
        self.VALUE = weight
    def get_possible_moves(self, board):
        moves = []

        moves.append(self.get_move(board, self.x+2, self.y+1))
        moves.append(self.get_move(board, self.x-1, self.y+2))
        moves.append(self.get_move(board, self.x-2, self.y+1))
        moves.append(self.get_move(board, self.x+1, self.y-2))
        moves.append(self.get_move(board, self.x+2, self.y-1))
        moves.append(self.get_move(board, self.x+1, self.y+2))
        moves.append(self.get_move(board, self.x-2, self.y-1))
        moves.append(self.get_move(board, self.x-1, self.y-2))

        return self.remove_null_from_list(moves)

    def clone(self):
        return Knight(self.x, self.y, self.color)




class King(Piece):

    PIECE_TYPE = "♔"


    def __init__(self, x, y, color,weight=20000):
        super(King, self).__init__(x, y, color, King.PIECE_TYPE, weight)
        self.VALUE = weight
    def get_possible_moves(self, board):
        moves = []

        moves.append(self.get_move(board, self.x+1, self.y))
        moves.append(self.get_move(board, self.x+1, self.y+1))
        moves.append(self.get_move(board, self.x, self.y+1))
        moves.append(self.get_move(board, self.x-1, self.y+1))
        moves.append(self.get_move(board, self.x-1, self.y))
        moves.append(self.get_move(board, self.x-1, self.y-1))
        moves.append(self.get_move(board, self.x, self.y-1))
        moves.append(self.get_move(board, self.x+1, self.y-1))

        moves.append(self.get_top_castling_move(board))
        moves.append(self.get_bottom_castling_move(board))

        return self.remove_null_from_list(moves)

    def get_top_castling_move(self, board):
        if (self.color == Piece.WHITE and board.white_king_moved):
            return 0
        if (self.color == Piece.BLACK and board.black_king_moved):
            return 0

        piece = board.get_piece(self.x, self.y-3)
        if (piece != 0):
            if (piece.color == self.color and piece.piece_type == Rook.PIECE_TYPE):
                if (board.get_piece(self.x, self.y-1) == 0 and board.get_piece(self.x, self.y-2) == 0):
                    return AI_Model.Move(self.x, self.y, self.x, self.y - 2, True)

        return 0

    def get_bottom_castling_move(self, board):
        if (self.color == Piece.WHITE and board.white_king_moved):
            return 0
        if (self.color == Piece.BLACK and board.black_king_moved):
            return 0

        piece = board.get_piece(self.x, self.y+4)
        if (piece != 0):
            if (piece.color == self.color and piece.piece_type == Rook.PIECE_TYPE):
                if (board.get_piece(self.x, self.y+1) == 0 and board.get_piece(self.x, self.y+2) == 0 and board.get_piece(self.x, self.y+3) == 0):
                    return AI_Model.Move(self.x, self.y, self.x, self.y + 2, True)

        return 0


    def clone(self):
        return King(self.x, self.y, self.color)


class Pawn(Piece):

    PIECE_TYPE = "♙"

    def __init__(self, x, y, color, weight=100):
        super(Pawn, self).__init__(x, y, color, Pawn.PIECE_TYPE, weight)
        self.VALUE = weight
    def is_starting_position(self):
        if (self.color == Piece.BLACK):
            return self.y == 1
        else:
            return self.y == 8 - 2
    #Finds all possible moves for a given piece
    def get_possible_moves(self, board):
        moves = []

        # Direction the pawn can move in.
        direction = -1
        if (self.color == Piece.BLACK):
            direction = 1

        # The general 1 step forward move.
        if (board.get_piece(self.x, self.y+direction) == 0):
            moves.append(self.get_move(board, self.x, self.y + direction))

        # The Pawn can take 2 steps as the first move.
        if (self.is_starting_position() and board.get_piece(self.x, self.y+ direction) == 0 and board.get_piece(self.x, self.y + direction*2) == 0):
            moves.append(self.get_move(board, self.x, self.y + direction * 2))

        # Eating pieces.
        piece = board.get_piece(self.x + 1, self.y + direction)
        if (piece != 0):
            moves.append(self.get_move(board, self.x + 1, self.y + direction))

        piece = board.get_piece(self.x - 1, self.y + direction)
        if (piece != 0):
            moves.append(self.get_move(board, self.x - 1, self.y + direction))

        return self.remove_null_from_list(moves)

    def clone(self):
        return Pawn(self.x, self.y, self.color)

