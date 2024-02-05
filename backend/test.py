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
print(wb.getOneSquareDiag1(wb.location)==False)
print(wb.getOneSquareDiag2(wb.location)==False)
print(wb.getOneSquareDiag3(wb.location)==False)
print(wb.getOneSquareDiag4(wb.location)==('b', 2))

# testing one square cardinals
print(wb.getOneSquareDown(wb.location)==False)
print(wp.getOneSquareDown(wp.location)==('d', 3)) 
print(bp.getOneSquareUp(bp.location)==('h', 8))
print(wb.getOneSquareLeft(wb.location)==False)
print(wp.getOneSquareRight(wp.location)==('e', 4))

# testing king valid move
wk = King("White", "4", ("c", 6))
placePiece(wk)
print(type(BOARD[2][2])==King)

print(wk.isMoveValid(("c", 5))==True)
print(wk.isMoveValid(("c", 7))==True)
print(wk.isMoveValid(("b", 6))==True)
print(wk.isMoveValid(("d", 6))==True)
print(wk.isMoveValid(("d", 7))==True)
print(wk.isMoveValid(("d", 5))==True)
print(wk.isMoveValid(("b", 7))==True)
print(wk.isMoveValid(("b", 5))==True)
print(wk.isMoveValid(("a", 5))==False)

# moving white king
print(moveFromCurrentSquare(wk, ("b", 5))=="King C6 to B5")
print(moveFromCurrentSquare(wk, ("d", 7))=="invalid move")
print(wk.location==("b", 5))

print(wk.checkSquaresUp(("b", 5)))