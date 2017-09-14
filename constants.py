PIECES = set("RNBKQPrnbkqp")
FEN_PIECES = { i : ("b" if i.islower() else "w") + i.lower() for i in PIECES}
BOARD_DIMENSIONS = 320
BOARD_SIZE = (BOARD_DIMENSIONS, BOARD_DIMENSIONS)
SQUARE_SIZE = 40
PIECE_SIZE = (SQUARE_SIZE, SQUARE_SIZE)
RESOURCES = "resources/"
OUTPUT = "output"
VALID_FORMATS = set(["jpg", "png", "gif", "bmp"])
DESC = "A CLI tool to convert a valid FEN to an image file."
FEN_HELP = '''
A valid FEN (see https://en.wikipedia.org/wiki/Forsyth-Edwards_Notation)
'''
FORMAT_HELP = "Specify the format of the output file (the extension i.e jpg, png)"
FILE_HELP = "Specify the name of the output file (without an extension)"
FOLDER_HELP = "Specify the output folder (no leading or trailing slashes)"