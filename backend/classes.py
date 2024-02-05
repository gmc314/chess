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


class Piece:
    def __init__(self, color: str, name: str, ID: str, location: tuple, canCastle: bool, points: int):
        self.color = color 
        self.name = name
        self.ID = ID
        self.location = location
        self.canCastle = canCastle
        self.points = points

    def __repr__(self) -> str:
        return f"{self.color} {self.name}"


# inheriting from Piece class
class King(Piece):    
    def __init__(self, color, ID, location):
        super().__init__(color, "King", ID, location, True, 0) 

    def isMoveValid(self, newSquare):
        up = getOneSquareUp(self, self.location) 
        down = getOneSquareDown(self, self.location)
        left = getOneSquareLeft(self, self.location)
        right = getOneSquareRight(self, self.location)
        d1 = getOneSquareDiag1(self, self.location)
        d2 = getOneSquareDiag2(self, self.location)
        d3 = getOneSquareDiag3(self, self.location)
        d4 = getOneSquareDiag4(self, self.location)
        
        if up == newSquare:
            return True
        
        elif down == newSquare:
            return True
        
        elif left == newSquare:
            return True
        
        elif right == newSquare:
            return True
        
        elif d1 == newSquare:
            return True
        
        elif d2 == newSquare:
            return True
        
        elif d3 == newSquare:
            return True
        
        elif d4 == newSquare:
            return True
        
        else:
            return False
        

class Queen(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Queen", ID, location, False, 9) 
    
    def isMoveValid(self, newSquare):
        upMoves = getValidMovesInStraightDir(self, getOneSquareUp, self.location)
        downMoves = getValidMovesInStraightDir(self, getOneSquareDown, self.location)
        leftMoves = getValidMovesInStraightDir(self, getOneSquareLeft, self.location)
        rightMoves = getValidMovesInStraightDir(self, getOneSquareRight, self.location)
        
        diag1Moves = getValidMovesInStraightDir(self, getOneSquareDiag1, self.location)
        diag2Moves = getValidMovesInStraightDir(self, getOneSquareDiag2, self.location)
        diag3Moves = getValidMovesInStraightDir(self, getOneSquareDiag3, self.location)
        diag4Moves = getValidMovesInStraightDir(self, getOneSquareDiag4, self.location)
        
        validMoves = upMoves+downMoves+leftMoves+rightMoves+diag1Moves+diag2Moves+diag3Moves+diag4Moves
        
        if newSquare not in validMoves:
            return False
        
        else:
            return True
    

class Rook(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Rook", ID, location, True, 5)

    def isMoveValid(self, newSquare):
        upMoves = getValidMovesInStraightDir(self, getOneSquareUp, self.location)
        downMoves = getValidMovesInStraightDir(self, getOneSquareDown, self.location)
        leftMoves = getValidMovesInStraightDir(self, getOneSquareLeft, self.location)
        rightMoves = getValidMovesInStraightDir(self, getOneSquareRight, self.location)
        
        validMoves = upMoves + downMoves + leftMoves + rightMoves
        
        if newSquare not in validMoves:
            return False
        
        else:
            return True
    
class Bishop(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Bishop", ID, location, False, 3) 
    
    def isMoveValid(self, newSquare):
        diag1Moves = getValidMovesInStraightDir(self, getOneSquareDiag1, self.location)
        diag2Moves = getValidMovesInStraightDir(self, getOneSquareDiag2, self.location)
        diag3Moves = getValidMovesInStraightDir(self, getOneSquareDiag3, self.location)
        diag4Moves = getValidMovesInStraightDir(self, getOneSquareDiag4, self.location)
        
        validMoves = diag1Moves + diag2Moves + diag3Moves + diag4Moves
        
        if newSquare not in validMoves:
            return False
        
        else:
            return True
    

class Knight(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Knight", ID, location, False, 3) 
    
    def isMoveValid(self, newSquare):
        return True    



class Pawn(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Pawn", ID, location, False, 1) 
        self.firstTurn = True

    def isMoveValid(self, newSquare):
        # getting files and ranks of currrent and new squares
        currentFile, currentRank = self.location
        newFile, newRank = newSquare

        if self.color == "White":
            if self.firstTurn == True:
                # returns a boolean 
                return (currentFile == newFile) and (1 <= newRank - currentRank <= 2)
        
            else:
                # returns a boolean 
                return (currentFile == newFile) and (newRank - currentRank == 1)
        
        if self.color == "Black":
            if self.firstTurn == True:
                # returns a boolean 
                return (currentFile == newFile) and (1 <= currentRank - newRank <= 2)
        
            else:
                # returns a boolean 
                return (currentFile == newFile) and (currentRank - newRank == 1)
            

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
def stringifyRankFile(square: tuple[str, int]):
    return f"{square[0].upper()}{square[1]}"


# place a piece on the board at its initial square
def placePiece(piece: Piece):
    currentSquare = piece.location
    row, col = getBoardIndexFromRankAndFile(currentSquare)
    BOARD[row][col] = piece
    return f"{piece} placed"


# captures the capturee
def capture(capturer: Piece, capturee: Piece):
    captureeRow, captureeCol = getBoardIndexFromRankAndFile(capturee.location)
    BOARD[captureeRow][captureeCol] = None
    capturer.location = capturee.location
    BOARD[captureeRow][captureeCol] = capturer
    return f"{capturee} captured."


# returns the piece at the specific square
def getPieceFromLocation(square):
    r, c = getBoardIndexFromRankAndFile(square)
    return BOARD[r][c]


# move piece from current square to new `square`
def moveFromCurrentSquare(piece: Union[King, Queen, Rook, Bishop, Knight, Pawn], newSquare: tuple[str, int]):
    if not piece.isMoveValid(newSquare):
        return "invalid move"
    
    # getting current location of piece
    currentSquare = piece.location
    currentRow, currentCol = getBoardIndexFromRankAndFile(currentSquare)

    # getting location of move
    newRow, newCol = getBoardIndexFromRankAndFile(newSquare)
    newRank, newFile = getRankAndFileFromBoardIndex(newRow, newCol)
    occupant = getPieceFromLocation((newRank, newFile))
    
    if occupant != None:
        captureMessage = capture(piece, occupant)
    else:
        captureMessage = ""
    
    # move piece from the current square
    BOARD[currentRow][currentCol] = None

    # to new square
    piece.location = (newRank, newFile)    
    
    BOARD[newRow][newCol] = piece

    # condition for en passant and first turn two-square forward move
    if type(piece) == Pawn:
        piece.firstTurn = False

    # print out the move 
    return f"{piece.name} {stringifyRankFile(currentSquare)} to {stringifyRankFile(newSquare)}. {captureMessage}"


# the getOneSquareLeft function returns the left adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def getOneSquareLeft(piece: Piece, currentSquare: tuple[str, int]):
    file, rank = currentSquare
    if file == "a":
        return False

    newFile = chr(ord(file) - 1)
    r, c = getBoardIndexFromRankAndFile((newFile, rank))

    occupant = BOARD[r][c]
    if isinstance(occupant, Piece):
        if occupant.color == piece.color:
            return False
        
    return (newFile, rank)


# the getOneSquareRight function returns the right adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def getOneSquareRight(piece: Piece, currentSquare: tuple[str, int]):
    file, rank = currentSquare
    if file == "h":
        return False

    newFile = chr(ord(file) + 1)
    r, c = getBoardIndexFromRankAndFile((newFile, rank))
    
    occupant = BOARD[r][c]
    if isinstance(occupant, Piece):
        if occupant.color == piece.color:
            return False

    return (newFile, rank)


# the getOneSquareUp function returns the up adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def getOneSquareUp(piece: Piece, currentSquare: tuple[str, int]):
    file, rank = currentSquare
    if rank == len(BOARD):
        return False

    newRank = rank + 1
    r, c = getBoardIndexFromRankAndFile((file, newRank))
    
    occupant = BOARD[r][c]
    if isinstance(occupant, Piece):
        if occupant.color == piece.color:
            return False

    return (file, newRank)


# the getOneSquareDown function returns the down adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def getOneSquareDown(piece: Piece, currentSquare: tuple[str, int]):
    file, rank = currentSquare
    if rank == 1:
        return False

    newRank = rank - 1
    r, c = getBoardIndexFromRankAndFile((file, newRank))
    
    occupant = BOARD[r][c]
    if isinstance(occupant, Piece):
        if occupant.color == piece.color:
            return False

    return (file, newRank)


# diag1 means the diagonal from top left to bottom right
# the getOneSquareDiag1 function returns the diag1 adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def getOneSquareDiag1(piece: Piece, currentSquare: tuple[str, int]):
    file, rank = currentSquare
    if file == "h" or rank == 1:
        return False
    
    newFile = chr(ord(file) + 1)
    newRank = rank - 1
    r, c = getBoardIndexFromRankAndFile((newFile, newRank))
    
    occupant = BOARD[r][c]
    if isinstance(occupant, Piece):
        if (not isinstance(piece, Knight)) or occupant.color == piece.color:
            return False
        
    return (newFile, newRank)


# diag2 means the diagonal from bottom right to top left
# the getOneSquareDiag2 function returns the diag2 adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def getOneSquareDiag2(piece: Piece, currentSquare: tuple[str, int]):
    file, rank = currentSquare
    if file == "a" or rank == len(BOARD):
        return False
    
    newFile = chr(ord(file) - 1)
    newRank = rank + 1
    r, c = getBoardIndexFromRankAndFile((newFile, newRank))
    
    occupant = BOARD[r][c]
    if isinstance(occupant, Piece):
        if (not isinstance(piece, Knight)) or occupant.color == piece.color:
            return False

    return (newFile, newRank)


# diag3 means the diagonal from top right to bottom left
# the getOneSquareDiag3 function returns the diag3 adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def getOneSquareDiag3(piece: Piece, currentSquare: tuple[str, int]):
    file, rank = currentSquare
    if file == "a" or rank == 1:
        return False
    
    newFile = chr(ord(file) - 1)
    newRank = rank - 1
    r, c = getBoardIndexFromRankAndFile((newFile, newRank))
    
    occupant = BOARD[r][c]
    if isinstance(occupant, Piece):
        if (not isinstance(piece, Knight)) or occupant.color == piece.color:
            return False
        
    return (newFile, newRank)


# diag4 means the diagonal from bottom left to top right 
# the getOneSquareDiag4 function returns the diag4 adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def getOneSquareDiag4(piece: Piece, currentSquare: tuple[str, int]):
    file, rank = currentSquare
    if file == "h" or rank == len(BOARD):
        return False
    
    newFile = chr(ord(file) + 1)
    newRank = rank + 1
    r, c = getBoardIndexFromRankAndFile((newFile, newRank))
    
    occupant = BOARD[r][c]
    if isinstance(occupant, Piece):
        if (not isinstance(piece, Knight)) or occupant.color == piece.color:
            return False

    return (newFile, newRank)


# this function returns a list of valid moves in a straight (cardinal and diagonal) direction
def getValidMovesInStraightDir(piece: Piece, getOneSquareDirFunction, square: tuple[str, int]):
    validMoves = []
    nextSquareUp = getOneSquareDirFunction(piece, square)
    while type(nextSquareUp) == tuple:
        validMoves.append(nextSquareUp)
        upOneSquare = getOneSquareDirFunction(piece, nextSquareUp)
        
        if type(upOneSquare) != tuple:
            break
        
        nextSquareUp = getOneSquareDirFunction(piece, nextSquareUp)

    return validMoves


# gets a list of valid moves for the Knight
def knightWheel(knight: Knight):
    currentSquare = knight.location
    oneSquareD1 = getOneSquareDiag1(knight, currentSquare)
    oneSquareD2 = getOneSquareDiag2(knight, currentSquare)
    oneSquareD3 = getOneSquareDiag3(knight, currentSquare)
    oneSquareD4 = getOneSquareDiag4(knight, currentSquare)

    if oneSquareD1 != False:
        movesD1 = [getOneSquareRight(oneSquareD1), getOneSquareDown(oneSquareD1)]
    
    if oneSquareD2 != False:
        movesD2 = [getOneSquareLeft(oneSquareD2), getOneSquareUp(oneSquareD2)]
    
    if oneSquareD3 != False:
        movesD3 = [getOneSquareLeft(oneSquareD3), getOneSquareDown(oneSquareD3)]
    
    if oneSquareD4 != False:
        movesD4 = [getOneSquareRight(oneSquareD4), getOneSquareUp(oneSquareD4)]
    
    validMoves = movesD1 + movesD2 + movesD3 + movesD4
    validMoves = list(filter(lambda x: x != False, validMoves))

    return validMoves