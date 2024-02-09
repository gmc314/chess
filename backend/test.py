from script import *
from pprint import pprint
########
# BISHOP
# testing placing a piece on the board
# wb = Bishop("White", "1", ("b", 2))
# placePiece(wb)
# print(type(BOARD[6][1])==Bishop)

# # testing moving piece
# moveFromCurrentSquare(wb, ("a", 1))
# print(BOARD[6][1]==" -- ")
# print(type(BOARD[7][0])==Bishop)

# ########
# # PAWN 
# # testing placing a pawn on the board
# wp = Pawn("White", "1", ("d", 2))
# placePiece(wp)
# print(type(BOARD[6][3])==Pawn)
# print(wp.firstTurn == 0)

# # testing moving piece
# moveFromCurrentSquare(wp, ("d", 4))
# print(BOARD[6][3]==' -- ')
# print(type(BOARD[4][3])==Pawn)
# print(wp.firstTurn==1)

# # testing invalid move
# bp = Pawn("Black", "1", ("h", 7))
# placePiece(bp)
# print(type(BOARD[1][7])==Pawn)
# print(moveFromCurrentSquare(bp, ("h", 4)) == "invalid move")

# # testing one square diagonals
# print(getOneSquareDiagBR(wb, wb.location)==False)
# print(getOneSquareDiagTL(wb, wb.location)==False)
# print(getOneSquareDiagBL(wb, wb.location)==False)
# print(getOneSquareDiagTR(wb, wb.location)==('b', 2))

# # testing one square cardinals
# print(getOneSquareDown(wb, wb.location)==False)
# print(getOneSquareDown(wp, wp.location)==('d', 3)) 
# print(getOneSquareUp(bp, bp.location)==('h', 8))
# print(getOneSquareLeft(wb, wb.location)==False)
# print(getOneSquareRight(wp, wp.location)==('e', 4))

# # testing king valid move
# wk = King("White", "4", ("c", 6))
# placePiece(wk)
# print(type(BOARD[2][2])==King)

# print(wk.isMoveValid(("c", 5))==True)
# print(wk.isMoveValid(("c", 7))==True)
# print(wk.isMoveValid(("b", 6))==True)
# print(wk.isMoveValid(("d", 6))==True)
# print(wk.isMoveValid(("d", 7))==True)
# print(wk.isMoveValid(("d", 5))==True)
# print(wk.isMoveValid(("b", 7))==True)
# print(wk.isMoveValid(("b", 5))==True)
# print(wk.isMoveValid(("a", 5))==False)

# # moving white king
# print(moveFromCurrentSquare(wk, ("b", 5))=="K C6 to B5. ")
# print(moveFromCurrentSquare(wk, ("d", 7))=="invalid move")
# print(wk.location==("b", 5))
# moveFromCurrentSquare(wk, ("b", 5))

# ######## 
# # QUEEN
# # testing queen capture
# bn = Knight("Black", "8", ("b", 8))
# placePiece(bn)
# wq = Queen("White", "123", ("b", 6))

# print(getValidMovesInStraightDir(wq, getOneSquareUp, wq.location) == [('b', 7), ('b', 8)])

# print(moveFromCurrentSquare(wq, bn.location)=='Q B6 to B8. BN captured.')


# #########
# # KNIGHT
# # obstructed knight wheel
# bn2 = Knight("Black", "8", ("g", 1))
# placePiece(bn2)
# bp2 = Pawn("Black", "8", ("e", 2))
# placePiece(bp2)
# print(bn2.getValidMoves() == [('f', 3), ('h', 3)])

# # two pawns are placed for testing knight's ability to jump over any piece
# bp2 = Pawn("Black", "8", ("f", 2))
# placePiece(bp2)
# wp2 = Pawn("White", "8", ("d", 2))
# placePiece(wp2)

# # this pawn is placed for the knight to capture
# wp3 = Pawn("White", "8", ("c", 2))
# placePiece(wp3)

# # placing the knight and printing valid moves via getValidMoves function
# bn5 = Knight("Black", "8", ("e", 3))
# placePiece(bn5)
# print(bn5.getValidMoves() == [('g', 2), ('f', 1), ('c', 4), ('d', 5), ('c', 2), ('d', 1), ('g', 4), ('f', 5)])

# # capturing the pawn
# print(moveFromCurrentSquare(bn5, wp3.location) == 'N E3 to C2. WP captured.')
# print(bn5.getValidMoves() == [('e', 1), ('a', 3), ('b', 4), ('a', 1), ('e', 3), ('d', 4)])


# #######
# # KING
# bk = King("Black", "7", ("e", 6))
# placePiece(bk)
# print(bk.getValidMoves() == [('e', 7), ('e', 5), ('d', 6), ('f', 6), ('f', 5), ('d', 7), ('d', 5), ('f', 7)])
clearBoard()
######
# EN PASSANT 

wp = Pawn("White", "F", ("g", 2))
placePiece(wp)
moveFromCurrentSquare(wp, ("g", 4))
moveFromCurrentSquare(wp, ("g", 5))

bp = Pawn("Black", "W", ("h", 7))
placePiece(bp)
moveFromCurrentSquare(bp, ("h", 5))
#print(("h", 6) in bp.getValidMoves())

print(moveFromCurrentSquare(wp, ("h", 6)))
pprint(BOARD)