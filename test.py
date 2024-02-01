from backend import *
from pprint import pprint

# testing placing a piece on the board
bb = Pawn("White", "1", ("b", 2))
placePiece(bb)
print(type(BOARD[6][1])==Pawn)

# testing moving piece
print(moveFromCurrentSquare(bb, ("b", 4)))
print(BOARD[6][1]==None)
print(type(BOARD[4][1])==Pawn)

