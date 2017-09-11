from PIL import Image

PIECES = set("RNBKQPrnbkqp")
FEN_PIECES = { i : ("b" if i.islower() else "w") + i.lower() for i in PIECES}

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

def FENtoBoard(fen):
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
        for row in result:
            print(*row)
    else:
        print("Invalid FEN.")

# print(FEN_PIECES)
getFEN()
