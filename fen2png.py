from constants import *
from PIL import Image


class DrawImage:
    def __init__(self, board, fmt, dest, fname):
        self.result = Image.open(RESOURCES + "board.png").resize(BOARD_SIZE)
        self.board = board
        self.fmt = fmt
        self.fname = fname
        self.dest = dest

    def open_image(self, piece):
        try:
            im = Image.open(RESOURCES + "{}.png".format(piece))
            return im.resize(PIECE_SIZE)
        except:
            print(piece + ".png", "does not exist.")
            return None

    def insert(self, piece, square):  # square is tuple (r,c)
        R = square[0] * SQUARE_SIZE
        C = square[1] * SQUARE_SIZE
        self.result.paste(piece, (R, C), piece)

    def create(self):  # Fix orientation of board
        for i in range(8):
            for j in range(8):
                if self.board[i][j]:
                    piece = self.open_image(self.board[i][j])
                    self.insert(piece, (i, j))

    def to_image(self):
        self.result.save("{}/{}.{}".format(self.dest, self.fname, self.fmt))


class Board:
    def __init__(self, fen):
        self.fen = fen
        self.isvalid = self.isValidFEN()
        self.board = None
        if self.isvalid:
            self.board = self.FENtoBoard()

    def isValidFEN(self):
        board, move, castle, enpassant, halfmove, fullmove = self.fen
        return (
            self.isValidBoard(board)
            and self.isValidMove(move)
            and self.isValidCastle(castle)
            and self.isValidEnPassant(enpassant)
            and self.isInt(halfmove)
            and self.isInt(fullmove)
        )

    def FENtoBoard(self):  # Fix orientation of board
        board = [["" for j in range(8)] for i in range(8)]
        board_str = self.fen[0].split("/")
        for i, rank in enumerate(board_str):
            pos = 0
            for square in rank:
                if self.isInt(square):
                    pos += int(square)
                else:
                    board[pos][i] = FEN_PIECES[square]
                    pos += 1
        return board

    def isInt(self, value):
        try:
            value = int(value)
            return True
        except:
            return False

    def isValidEnPassant(self, square):
        return self.isValidSquare(square) or square == "-"

    def isValidSquare(self, square):
        if len(square) > 2:
            return False
        return square[0] in "abcdefgh" and square[1] in "12345678"

    def isValidCastle(self, castle):
        if len(castle) > 4:
            return False
        if castle == "-":
            return True
        possible = {i: 0 for i in ["K", "Q", "k", "q"]}
        for letter in castle:
            if letter not in possible.keys():
                return False
            if possible[letter]:
                return False
            possible[letter] = 1
        return True

    def isValidMove(self, move):
        return move == "w" or move == "b"

    def isValidBoard(self, board):
        board = board.split("/")
        if len(board) != 8:
            return False
        for rank in board:
            length = 0
            for piece in rank:
                if self.isInt(piece):
                    length += int(piece)
                elif piece in PIECES:
                    length += 1
                else:
                    return False
            if length != 8:
                return False
        return True
