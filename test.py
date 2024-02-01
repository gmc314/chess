from backend import *
from pprint import pprint

# testing placing a piece on the board
bb = Bishop("Black", "1", ("b", 2))
placePiece(bb)
print(type(BOARD[6][1])==Bishop)

# testing moving piece
print(moveFromCurrentSquare(bb, ("a", 1)))
print(BOARD[6][1]==None)
print(type(BOARD[7][0])==Bishop)
