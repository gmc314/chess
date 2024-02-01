from backend import *
from pprint import pprint

# testing placing a piece on the board
pprint(BOARD)
bb = Bishop("Black", "1", ("b", 2))
placePiece(bb)
pprint(BOARD)