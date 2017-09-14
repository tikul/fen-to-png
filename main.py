from constants import *
from fen2png import DrawImage, Board
import argparse
import os

parser = argparse.ArgumentParser(description=DESC)
parser.add_argument(dest="FEN", nargs=6, default=None, help=FEN_HELP)
parser.add_argument("-f", dest="fmt", metavar="format", default="png", help=FORMAT_HELP)
parser.add_argument("-o", dest="filename", metavar="output file", default="result", help=FILE_HELP)
parser.add_argument("-dir", dest="folder", metavar="output folder", default=OUTPUT, help=FOLDER_HELP)

def main():
    args = parser.parse_args()
    fen = Board(args.FEN)
    if fen.isvalid:
        if args.fmt not in VALID_FORMATS:
            print("{} is not an accepted image format. Saving as .png".format(args.fmt))
            args.fmt = "png"
        if not os.path.isdir(args.folder):
            #Handle if directory is not valid
            os.mkdir(args.folder)
            print("Creating new directory: {}".format(args.folder))
        boardGrid = fen.board
        boardImg = DrawImage(boardGrid, args.fmt, args.folder, args.filename)
        boardImg.create()
        boardImg.to_image()
        print("Completed! File created in {}/{}.{}".format(args.folder, args.filename, args.fmt))
    else:
        print("Invalid FEN. No Image file was generated.")

if __name__ == "__main__":
    main()