from PIL import Image
import argparse
import os

PIECES = set("RNBKQPrnbkqp")
FEN_PIECES = { i : ("b" if i.islower() else "w") + i.lower() for i in PIECES}
BOARD_DIMENSIONS = 320
BOARD_SIZE = (BOARD_DIMENSIONS, BOARD_DIMENSIONS)
SQUARE_SIZE = 40
PIECE_SIZE = (SQUARE_SIZE, SQUARE_SIZE)
RESOURCES = "resources/"
OUTPUT = "output"
VALID_FORMATS = set(["jpg", "png", "gif", "bmp"])
desc = "A CLI tool to convert a valid FEN to an image file."
fenhelp = '''
A valid FEN (see https://en.wikipedia.org/wiki/Forsyth-Edwards_Notation)
'''
formathelp = "Specify the format of the output file (the extension i.e jpg, png)"
filehelp = "Specify the name of the output file (without an extension)"
folderhelp = "Specify the output folder (no leading or trailing slashes)"

parser = argparse.ArgumentParser(description=desc)
parser.add_argument(dest="FEN", nargs=6, default=None, help=fenhelp)
parser.add_argument("-f", dest="fmt", metavar="format", default="png", help=formathelp)
parser.add_argument("-o", dest="filename", metavar="output file", default="result", help=filehelp)
parser.add_argument("-dir", dest="folder", metavar="output folder", default=OUTPUT, help=folderhelp)


class Board():
    def __init__(self, board, fmt, dest, fname):
        self.result = Image.open(RESOURCES+"board.png").resize(BOARD_SIZE)
        self.board = board
        self.fmt = fmt
        self.fname = fname
        self.dest = dest
    
    def open_image(self, piece):
        try:
            im = Image.open(RESOURCES+"{}.png".format(piece))
            return im.resize(PIECE_SIZE)
        except:
            print(piece+".png", "does not exist.")
            return None

    def insert(self, piece, square): #square is tuple (r,c)
        R = square[0]*SQUARE_SIZE
        C = square[1]*SQUARE_SIZE
        self.result.paste(piece, (R,C), piece)

    def create(self): #Fix orientation of board
        for i in range(8):
            for j in range(8):
                if self.board[i][j]:
                    piece = self.open_image(self.board[i][j])
                    self.insert(piece, (i,j))

    def to_image(self):
        self.result.save("{}/{}.{}".format(self.dest, self.fname, self.fmt))

def isInt(value):
    try:
        value = int(value)
        return True
    except:
        return False

def isValidEnPassant(square):
    return isValidSquare(square) or square == "-"

def isValidSquare(square):
    if len(square) > 2:
        return False
    return square[0] in "abcdefgh" and square[1] in "12345678"

def isValidCastle(castle):
    if len(castle) > 4:
        return False
    possible = {i: 0 for i in ["K", "Q", "k", "q"]}
    for letter in castle:
        if letter not in possible.keys():
            return False
        if possible[letter]:
            return False
        possible[letter] = 1
    return True

def isValidMove(move):
    return move=="w" or move == "b"

def isValidBoard(board):
    board = board.split("/")
    if len(board) != 8:
        return False
    for rank in board:
        length = 0
        for piece in rank:
            if isInt(piece):
                length += int(piece)
            elif piece in PIECES:
                length += 1
            else:
                return False
        if length != 8:
            return False
    return True

def isValidFEN(fen):
    board, move, castle, enpassant, halfmove, fullmove = fen
    return (isValidBoard(board) and isValidMove(move) and isValidCastle(castle) 
    and isValidEnPassant(enpassant) and isInt(halfmove) and isInt(fullmove))

def FENtoBoard(fen): #Fix orientation of board
    board = [["" for j in range(8)] for i in range(8)]
    board_str = fen[0].split("/")
    for i, rank in enumerate(board_str):
        pos = 0
        for square in rank:
            if isInt(square):
                pos += int(square)
            else:
                board[i][pos] = FEN_PIECES[square]
                pos += 1
    return board

def main():
    args = parser.parse_args()
    fen = args.FEN
    if isValidFEN(fen):
        if args.fmt not in VALID_FORMATS:
            print("{} is not an accepted image format. Saving as .png".format(args.fmt))
            args.fmt = "png"
        if not os.path.isdir(args.folder):
            #Handle if directory is not valid
            os.mkdir(args.folder)
            print("Creating new directory: {}".format(args.folder))
        board = FENtoBoard(fen)
        boardToImage = Board(board, args.fmt, args.folder, args.filename)
        boardToImage.create()
        boardToImage.to_image()
        print("Completed! File created in {}/{}.{}".format(args.folder, args.filename, args.fmt))
    else:
        print("Invalid FEN. No Image file was generated.")

if __name__ == "__main__":
    main()