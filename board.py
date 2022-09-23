from ChessAI import Pieces


#95% of this is not written by me. All it is doing is creating our chess board and setting its rules.
# For this project I focused more on the AI so I did not bother writing this class which has been created 100 times before.
class Board:

    #Setting Board Demensions
    WIDTH = 8
    HEIGHT = 8

    #TODO Test larger boards (Would most likely break AI)


    def __init__(self, chesspieces, white_king_moved, black_king_moved):
        self.chesspieces = chesspieces
        self.white_king_moved = white_king_moved
        self.black_king_moved = black_king_moved

    @classmethod
    def clone(cls, chessboard):
        chesspieces = [[0 for x in range(Board.WIDTH)] for y in range(Board.HEIGHT)]
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = chessboard.chesspieces[x][y]
                if (piece != 0):
                    chesspieces[x][y] = piece.clone()
        return cls(chesspieces, chessboard.white_king_moved, chessboard.black_king_moved)

    @classmethod
    def new(cls, weight_dict):
        chess_pieces = [[0 for x in range(Board.WIDTH)] for y in range(Board.HEIGHT)]

        #Sets Rules of each piece
        #Function Credit to Dirk
        # Create pawns.
        for x in range(Board.WIDTH):
            chess_pieces[x][Board.HEIGHT-2] = Pieces.Pawn(x, Board.HEIGHT - 2, Pieces.Piece.WHITE, weight_dict['pawn'])
            chess_pieces[x][1] = Pieces.Pawn(x, 1, Pieces.Piece.BLACK)

        # Create rooks.
        chess_pieces[0][Board.HEIGHT-1] = Pieces.Rook(0, Board.HEIGHT - 1, Pieces.Piece.WHITE, weight_dict['rook'])
        chess_pieces[Board.WIDTH-1][Board.HEIGHT-1] = Pieces.Rook(Board.WIDTH - 1, Board.HEIGHT - 1, Pieces.Piece.WHITE)
        chess_pieces[0][0] = Pieces.Rook(0, 0, Pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-1][0] = Pieces.Rook(Board.WIDTH - 1, 0, Pieces.Piece.BLACK)

        # Create Knights.
        chess_pieces[1][Board.HEIGHT-1] = Pieces.Knight(1, Board.HEIGHT - 1, Pieces.Piece.WHITE, weight_dict['knight'])
        chess_pieces[Board.WIDTH-2][Board.HEIGHT-1] = Pieces.Knight(Board.WIDTH - 2, Board.HEIGHT - 1, Pieces.Piece.WHITE)
        chess_pieces[1][0] = Pieces.Knight(1, 0, Pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-2][0] = Pieces.Knight(Board.WIDTH - 2, 0, Pieces.Piece.BLACK)

        # Create Bishops.
        chess_pieces[2][Board.HEIGHT-1] = Pieces.Bishop(2, Board.HEIGHT - 1, Pieces.Piece.WHITE, weight_dict['bishop'])
        chess_pieces[Board.WIDTH-3][Board.HEIGHT-1] = Pieces.Bishop(Board.WIDTH - 3, Board.HEIGHT - 1, Pieces.Piece.WHITE)
        chess_pieces[2][0] = Pieces.Bishop(2, 0, Pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-3][0] = Pieces.Bishop(Board.WIDTH - 3, 0, Pieces.Piece.BLACK)

        # Create King & Queen.
        chess_pieces[4][Board.HEIGHT-1] = Pieces.King(4, Board.HEIGHT - 1, Pieces.Piece.WHITE, weight_dict['king'])
        chess_pieces[3][Board.HEIGHT-1] = Pieces.Queen(3, Board.HEIGHT - 1, Pieces.Piece.WHITE, weight_dict["queen"])
        chess_pieces[4][0] = Pieces.King(4, 0, Pieces.Piece.BLACK)
        chess_pieces[3][0] = Pieces.Queen(3, 0, Pieces.Piece.BLACK)

        return cls(chess_pieces, False, False)

    def get_possible_moves(self, color):
        moves = []
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = self.chesspieces[x][y]
                if (piece != 0):
                    if (piece.color == color):
                        moves += piece.get_possible_moves(self)


        return moves

    def perform_move(self, move):
        piece = self.chesspieces[move.x_from][move.y_from]
        piece.x = move.x_to
        piece.y = move.y_to
        self.chesspieces[move.x_to][move.y_to] = piece
        self.chesspieces[move.x_from][move.y_from] = 0

        if (piece.piece_type == Pieces.Pawn.PIECE_TYPE):
            if (piece.y == 0 or piece.y == Board.HEIGHT-1):
                self.chesspieces[piece.x][piece.y] = Pieces.Queen(piece.x, piece.y, piece.color)

        if (move.castling_move):
            if (move.x_to < move.x_from):
                rook = self.chesspieces[move.x_from][0]
                rook.x = 2
                self.chesspieces[2][0] = rook
                self.chesspieces[0][0] = 0
            if (move.x_to > move.x_from):
                rook = self.chesspieces[move.x_from][Board.HEIGHT-1]
                rook.x = Board.WIDTH-4
                self.chesspieces[Board.WIDTH-4][Board.HEIGHT-1] = rook
                self.chesspieces[move.x_from][Board.HEIGHT-1] = 0

        if (piece.piece_type == Pieces.King.PIECE_TYPE):
            if (piece.color == Pieces.Piece.WHITE):
                self.white_king_moved = True
            else:
                self.black_king_moved = True

    # Returns if the given color is checked.
    def is_check(self, color):
        other_color = Pieces.Piece.WHITE
        if (color == Pieces.Piece.WHITE):
            other_color = Pieces.Piece.BLACK

        for move in self.get_possible_moves(other_color):
            copy = Board.clone(self)
            copy.perform_move(move)

            king_found = False
            for x in range(Board.WIDTH):
                for y in range(Board.HEIGHT):
                    piece = copy.chesspieces[x][y]
                    if (piece != 0):
                        if (piece.color == color and piece.piece_type == Pieces.King.PIECE_TYPE):
                            king_found = True

            if (not king_found):
                return True

        return False

    # Returns Piece at given position or 0 if: No Piece or out of bounds.
    def get_piece(self, x, y):
        if (not self.in_bounds(x, y)):
            return 0

        return self.chesspieces[x][y]

    #Check if input is in correct range for given board
    def in_bounds(self, x, y):
        return (x >= 0 and y >= 0 and x < Board.WIDTH and y < Board.HEIGHT)



    def to_string(self):
        string =  "    A  B  C  D  E  F  G  H\n"
        string += "    -----------------------\n"
        for y in range(Board.HEIGHT):
            string += str(8 - y) + " | "
            for x in range(Board.WIDTH):
                piece = self.chesspieces[x][y]
                if (piece != 0):
                    string += piece.to_string()
                else:
                    string += ".. "
            string += "\n"
        return string + "\n"
