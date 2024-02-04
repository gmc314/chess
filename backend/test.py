from classes import *
from functions import *
from pprint import pprint

# testing placing a piece on the board
wb = Bishop("White", "1", ("b", 2))
placePiece(wb)
print(type(BOARD[6][1])==Bishop)

# testing moving piece
moveFromCurrentSquare(wb, ("a", 1))
print(BOARD[6][1]==None)
print(type(BOARD[7][0])==Bishop)

########
# PAWN 
# testing placing a pawn on the board
wp = Pawn("White", "1", ("d", 2))
placePiece(wp)
print(type(BOARD[6][3])==Pawn)
print(wp.firstTurn)

# testing moving piece
moveFromCurrentSquare(wp, ("d", 4))
print(BOARD[6][3]==None)
print(type(BOARD[4][3])==Pawn)
print(not wp.firstTurn)

# testing invalid move
bp = Pawn("Black", "1", ("h", 7))
placePiece(bp)
print(type(BOARD[1][7])==Pawn)
print(moveFromCurrentSquare(bp, ("h", 4)) == "invalid move")

# testing one square diagonals
print(oneSquareDiag1(wb)==False)
print(oneSquareDiag2(wb)==False)
print(oneSquareDiag3(wb)==False)
print(oneSquareDiag4(wb)==('b', 2))

# testing one square cardinals
print(oneSquareDown(wb)==False)
print(oneSquareDown(wp)==('d', 3)) 
print(oneSquareUp(bp)==('h', 8))
print(oneSquareLeft(wb)==False)
print(oneSquareRight(wp)==('e', 4))
