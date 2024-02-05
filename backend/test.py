from classes import *
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
print(wb.oneSquareDiag1(wb.location)==False)
print(wb.oneSquareDiag2(wb.location)==False)
print(wb.oneSquareDiag3(wb.location)==False)
print(wb.oneSquareDiag4(wb.location)==('b', 2))

# testing one square cardinals
print(wb.oneSquareDown(wb.location)==False)
print(wp.oneSquareDown(wp.location)==('d', 3)) 
print(bp.oneSquareUp(bp.location)==('h', 8))
print(wb.oneSquareLeft(wb.location)==False)
print(wp.oneSquareRight(wp.location)==('e', 4))
