from classes import *
from typing import Union

BOARD = [
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
]

fileIndex = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}


# gets the indices of the Board from rank and file 
def getBoardIndexFromRankAndFile(square: tuple[str, int]):
    file, rank = square
    col = fileIndex[file]
    row = len(BOARD) - rank
    return (row, col)


# gets the rank and file from indices of the Board
def getRankAndFileFromBoardIndex(row, col):
    file = list(fileIndex.keys())[list(fileIndex.values()).index(col)]
    rank = len(BOARD) - row 
    return (file, rank)


# convert rank and file tuple to string
def stringifyRankFile(square: tuple):
    return f"{square[0]}{square[1]}"


# place a piece on the board at its initial square
def placePiece(piece: Piece):
    currentSquare = piece.location
    row, col = getBoardIndexFromRankAndFile(currentSquare)
    BOARD[row][col] = piece
    return f"{piece} placed"


# move piece from current square to new `square`
def moveFromCurrentSquare(piece: Union[King, Queen, Rook, Bishop, Knight, Pawn], newSquare: tuple):
    if not piece.isMoveValid(newSquare):
        return "invalid move"
    
    # getting current location of piece
    currentSquare = piece.location
    currentRow, currentCol = getBoardIndexFromRankAndFile(currentSquare)

    # getting location of move
    newRow, newCol = getBoardIndexFromRankAndFile(newSquare)
    newRank, newFile = getRankAndFileFromBoardIndex(newRow, newCol)

    # move piece from the current square
    BOARD[currentRow][currentCol] = None

    # to new
    piece.location = (newRank, newFile)
    BOARD[newRow][newCol] = piece

    # condition for en passant and first turn two-square forward move
    if type(piece) == Pawn:
        piece.firstTurn = False

    # print out the move 
    return f"{piece.name} {stringifyRankFile(currentSquare)} to {stringifyRankFile(newSquare)}"

def capture(capturer: Piece, capturee: Piece):
    captureeRow, captureeCol = getBoardIndexFromRankAndFile(capturee.location)
    BOARD[captureeRow][captureeCol] = None
    capturer.location = capturee.location
    BOARD[captureeRow][captureeCol] = capturer
    return f"{capturee} captured"


# the oneSquareLeft function returns the left adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def oneSquareLeft(piece: Piece):
    file, rank = piece.location
    if file == "a":
        return False

    newFile = chr(ord(file) - 1)
    r, c = getBoardIndexFromRankAndFile(newFile, rank)

    occupant = BOARD[r][c]
    if type(occupant) == Piece:
        if occupant.color == piece.color:
            return False

        else:
            return "can capture"
        
    return (newFile, rank)


# the oneSquareRight function returns the right adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def oneSquareRight(piece: Piece):
    file, rank = piece.location
    if file == "h":
        return False

    newFile = chr(ord(file) + 1)
    r, c = getBoardIndexFromRankAndFile(newFile, rank)
    
    occupant = BOARD[r][c]
    if type(occupant) == Piece:
        if occupant.color == piece.color:
            return False
        
        else:
            return "can capture"

    return (newFile, rank)


# the oneSquareUp function returns the up adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def oneSquareUp(piece: Piece):
    file, rank = piece.location
    if rank == len(BOARD):
        return False

    newRank = rank + 1
    r, c = getBoardIndexFromRankAndFile(file, newRank)
    
    occupant = BOARD[r][c]
    if type(occupant) == Piece:
        if occupant.color == piece.color:
            return False
        
        else:
            return "can capture"

    return (file, newRank)

# the oneSquareDown function returns the down adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def oneSquareDown(piece: Piece):
    file, rank = piece.location
    if rank == 1:
        return False

    newRank = rank - 1
    r, c = getBoardIndexFromRankAndFile(file, newRank)
    
    occupant = BOARD[r][c]
    if type(occupant) == Piece:
        if occupant.color == piece.color:
            return False
        
        else:
            return "can capture"

    return (file, newRank)


# diag1 means the diagonal from top left to bottom right
# the oneSquareDiag1 function returns the diag1 adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def oneSquareDiag1(piece: Piece):
    file, rank = piece.location
    if file == "h":
        return False
    
    newFile = chr(ord(file) + 1)
    newRank = rank - 1
    r, c = getBoardIndexFromRankAndFile(newFile, newRank)
    
    occupant = BOARD[r][c]
    if type(occupant) == Piece:
        if occupant.color == piece.color:
            return False
        
        else:
            return "can capture"

    return (file, newRank)


# diag2 means the diagonal from bottom right to top left
# the oneSquareDiag2 function returns the diag2 adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def oneSquareDiag2(piece: Piece):
    file, rank = piece.location
    if file == "a":
        return False
    
    newFile = chr(ord(file) - 1)
    newRank = rank + 1
    r, c = getBoardIndexFromRankAndFile(newFile, newRank)
    
    occupant = BOARD[r][c]
    if type(occupant) == Piece:
        if occupant.color == piece.color:
            return False
        
        else:
            return "can capture"

    return (file, newRank)


# diag3 means the diagonal from top right to bottom left
# the oneSquareDiag3 function returns the diag3 adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def oneSquareDiag3(piece: Piece):
    file, rank = piece.location
    if file == "a":
        return False
    
    newFile = chr(ord(file) - 1)
    newRank = rank - 1
    r, c = getBoardIndexFromRankAndFile(newFile, newRank)
    
    occupant = BOARD[r][c]
    if type(occupant) == Piece:
        if occupant.color == piece.color:
            return False
        
        else:
            return "can capture"

    return (file, newRank)


# diag4 means the diagonal from bottom left to top right 
# the oneSquareDiag4 function returns the diag4 adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def oneSquareDiag4(piece: Piece):
    file, rank = piece.location
    if file == "h":
        return False
    
    newFile = chr(ord(file) + 1)
    newRank = rank + 1
    r, c = getBoardIndexFromRankAndFile(newFile, newRank)
    
    occupant = BOARD[r][c]
    if type(occupant) == Piece:
        if occupant.color == piece.color:
            return False
        
        else:
            return "can capture"

    return (file, newRank)