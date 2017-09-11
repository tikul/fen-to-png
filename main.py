from PIL import Image

PIECES = set("RNBKQPrnbkqp")
FEN_PIECES = { i : ("b" if i.islower() else "w") + i.lower() for i in PIECES}
BOARD_DIMENSIONS = 320
BOARD_SIZE = (BOARD_DIMENSIONS, BOARD_DIMENSIONS)
SQUARE_SIZE = 40
PIECE_SIZE = (SQUARE_SIZE, SQUARE_SIZE)
RESOURCES = "resources/"

class Board():
    def __init__(self, board, no=0):
        self.result = Image.open(RESOURCES+"board.png").resize(BOARD_SIZE)
        self.board = board
        self.no = no
    
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
        self.result.save(RESOURCES+"{}.png".format(self.no))

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
    fen = fen.split()
    if len(fen) != 6:
        return False
    board, move, castle, enpassant, halfmove, fullmove = fen
    return (isValidBoard(board) and isValidMove(move) and isValidCastle(castle) 
    and isValidEnPassant(enpassant) and isInt(halfmove) and isInt(fullmove))
    # if isValidBoard(board):
    #     print("Good board.")
    # if isValidMove(move):
    #     print("Good move.")
    # if isValidCastle(castle):
    #     print("Good castle.") 
    # if isValidSquare(enpassant):
    #     print("Good en-passant.")
    # if isInt(halfmove):
    #     print("Good half-move.") 
    # if isInt(fullmove):
    #     print("Good fullmove.")

def FENtoBoard(fen): #Fix orientation of board
    board = [["" for j in range(8)] for i in range(8)]
    board_str = fen.split()[0].split("/")
    for i, rank in enumerate(board_str):
        pos = 0
        for square in rank:
            if isInt(square):
                pos += int(square)
            else:
                board[i][pos] = FEN_PIECES[square]
                pos += 1
    return board

def getFEN():
    fen = input("Enter fen: ")
    if isValidFEN(fen):
        print("Valid FEN.")
        result = FENtoBoard(fen)
        bb = Board(result)
        bb.create()
        bb.to_image()
    else:
        print("Invalid FEN.")

# print(FEN_PIECES)
getFEN()


