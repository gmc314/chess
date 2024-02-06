from typing import Union

# the board is an 8x8 matrix
BOARD = [[" -- " for i in range(8)] for j in range(8)]

# this is for mapping the board's letters of the files to list indices
fileIndex = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}


class Piece:
    def __init__(self, color: str, name: str, ID: str, location: tuple, canCastle: bool, points: int) -> None:
        self.color = color 
        self.name = name
        self.ID = ID
        self.location = location
        self.canCastle = canCastle
        self.points = points

    def __repr__(self) -> str:
        return f"' {self.color[0]}{self.name} '"


# inheriting from Piece class
class King(Piece):    
    def __init__(self, color, ID, location):
        super().__init__(color, "K", ID, location, True, 0) 
    
    # returns one-square moves in all directions
    def getValidMoves(self):
        up = getOneSquareUp(self, self.location) 
        down = getOneSquareDown(self, self.location)
        left = getOneSquareLeft(self, self.location)
        right = getOneSquareRight(self, self.location)
        d1 = getOneSquareDiag1(self, self.location)
        d2 = getOneSquareDiag2(self, self.location)
        d3 = getOneSquareDiag3(self, self.location)
        d4 = getOneSquareDiag4(self, self.location)

        validMoves = [up, down, left, right, d1, d2, d3, d4]
        validMoves = list(filter(lambda x: x != False, validMoves))
    
        return validMoves

    def isMoveValid(self, newSquare):
        return newSquare in self.getValidMoves()
        

class Queen(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Q", ID, location, False, 9) 
    
    # getting all valid moves in all directions
    def getValidMoves(self):
        # valid vertical and horizontal moves
        upMoves = getValidMovesInStraightDir(self, getOneSquareUp, self.location)
        downMoves = getValidMovesInStraightDir(self, getOneSquareDown, self.location)
        leftMoves = getValidMovesInStraightDir(self, getOneSquareLeft, self.location)
        rightMoves = getValidMovesInStraightDir(self, getOneSquareRight, self.location)
        
        # valid diagonal moves
        diag1Moves = getValidMovesInStraightDir(self, getOneSquareDiag1, self.location)
        diag2Moves = getValidMovesInStraightDir(self, getOneSquareDiag2, self.location)
        diag3Moves = getValidMovesInStraightDir(self, getOneSquareDiag3, self.location)
        diag4Moves = getValidMovesInStraightDir(self, getOneSquareDiag4, self.location)
        
        # a list of all valid moves
        validMoves = upMoves+downMoves+leftMoves+rightMoves+diag1Moves+diag2Moves+diag3Moves+diag4Moves
        return validMoves    

    def isMoveValid(self, newSquare):
        return newSquare in self.getValidMoves()
            

class Rook(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "R", ID, location, True, 5)

    def getValidMoves(self):
        # valid vertical and horizontal moves
        upMoves = getValidMovesInStraightDir(self, getOneSquareUp, self.location)
        downMoves = getValidMovesInStraightDir(self, getOneSquareDown, self.location)
        leftMoves = getValidMovesInStraightDir(self, getOneSquareLeft, self.location)
        rightMoves = getValidMovesInStraightDir(self, getOneSquareRight, self.location)
        
        # list of valid moves
        validMoves = upMoves + downMoves + leftMoves + rightMoves
        return validMoves
        
    def isMoveValid(self, newSquare):
        return newSquare in self.getValidMoves()
    

class Bishop(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "B", ID, location, False, 3) 
    
    def getValidMoves(self):
        # valid diagonal moves
        diag1Moves = getValidMovesInStraightDir(self, getOneSquareDiag1, self.location)
        diag2Moves = getValidMovesInStraightDir(self, getOneSquareDiag2, self.location)
        diag3Moves = getValidMovesInStraightDir(self, getOneSquareDiag3, self.location)
        diag4Moves = getValidMovesInStraightDir(self, getOneSquareDiag4, self.location)
        
        # list of valid moves
        validMoves = diag1Moves + diag2Moves + diag3Moves + diag4Moves
        return validMoves
    
    def isMoveValid(self, newSquare):
        return newSquare in self.getValidMoves()

class Knight(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "N", ID, location, False, 3) 
    
    # gets a list of valid moves for the Knight
    # for a knight to move, it can go in a diagonal direction one 
    # square regardless if the square is occupied, and then it goes one more 
    # square in an either vertical or horizontal direction 
    # referring to standard chess rules 
    def getValidMoves(self):
        currentSquare = self.location

        # the four diagonal directions 
        oneSquareD1 = getOneSquareDiag1(self, currentSquare)
        oneSquareD2 = getOneSquareDiag2(self, currentSquare)
        oneSquareD3 = getOneSquareDiag3(self, currentSquare)
        oneSquareD4 = getOneSquareDiag4(self, currentSquare)
        movesD1 = []
        movesD2 = []
        movesD3 = []
        movesD4 = []

        # if the diagonal is on the board, then check the vertical or horizontal adjacent squares
        if oneSquareD1 != False:
            movesD1 = [getOneSquareRight(self, oneSquareD1), getOneSquareDown(self, oneSquareD1)]        
        
        if oneSquareD2 != False:
            movesD2 = [getOneSquareLeft(self, oneSquareD2), getOneSquareUp(self, oneSquareD2)]
            
        if oneSquareD3 != False:
            movesD3 = [getOneSquareLeft(self, oneSquareD3), getOneSquareDown(self, oneSquareD3)]
        
        if oneSquareD4 != False:
            movesD4 = [getOneSquareRight(self, oneSquareD4), getOneSquareUp(self, oneSquareD4)]
        
        # then gather all the results and filter for valid moves
        validMoves = movesD1 + movesD2 + movesD3 + movesD4

        # filter for non-False values in the validMoves list because 
        # of the output of the getOneSquare functions  
        validMoves = list(filter(lambda x: x != False, validMoves))

        return validMoves

    def isMoveValid(self, newSquare):
        # valid moves from knightWheel function 
        return newSquare in self.getValidMoves() 
        

class Pawn(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "P", ID, location, False, 1) 
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


# converts the rank and file tuple to a string
# returns a capital letter followed by a number 
def stringifyRankFile(square: tuple[str, int]) -> str:
    return f"{square[0].upper()}{square[1]}"


# place a piece on the board at its initial square. 
# returns a verification message
# modifies: BOARD
def placePiece(piece: Piece) -> str:
    currentSquare = piece.location
    row, col = getBoardIndexFromRankAndFile(currentSquare)
    BOARD[row][col] = piece
    return f"{piece} placed"


# this function does the process of capturing where
# the capturer piece captures the capturee piece
# modifies: BOARD 
# returns a verification message
def capture(capturer: Piece, capturee: Piece) -> str:
    captureeRow, captureeCol = getBoardIndexFromRankAndFile(capturee.location)
    BOARD[captureeRow][captureeCol] = " -- "
    capturer.location = capturee.location
    BOARD[captureeRow][captureeCol] = capturer
    return f"{capturee.color[0]}{capturee.name} captured."


# returns the piece at the specific square,
# or the empty square if there isn't a piece on the square
def getPieceFromLocation(square: tuple[str, int]) -> Union[Piece, str]:
    r, c = getBoardIndexFromRankAndFile(square)
    return BOARD[r][c]


# move piece from current square to new `square`
def moveFromCurrentSquare(piece: Union[King, Queen, Rook, Bishop, Knight, Pawn], newSquare: tuple[str, int]) -> str:
    if not piece.isMoveValid(newSquare):
        return "invalid move"
    
    # getting current location of piece
    currentSquare = piece.location
    currentRow, currentCol = getBoardIndexFromRankAndFile(currentSquare)

    # getting location of move
    newRow, newCol = getBoardIndexFromRankAndFile(newSquare)
    newRank, newFile = getRankAndFileFromBoardIndex(newRow, newCol)
    
    # if the space is occupied by the opposite colour:
    occupant = getPieceFromLocation((newRank, newFile))
    if occupant != " -- ":
        # call the capture function and print out the message
        captureMessage = capture(piece, occupant)
    else:
        captureMessage = ""
    
    # move piece from the current square
    BOARD[currentRow][currentCol] = " -- "

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
def getOneSquareLeft(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
    file, rank = currentSquare
    if file == "a":
        return False

    newFile = chr(ord(file) - 1)
    newSquare = (newFile, rank)
    occupant = getPieceFromLocation(newSquare)
    
    if isinstance(occupant, Piece):
        if occupant.color == piece.color:
            return False
        
    return newSquare


# the getOneSquareRight function returns the right adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def getOneSquareRight(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
    file, rank = currentSquare
    if file == "h":
        return False

    newFile = chr(ord(file) + 1)
    newSquare = (newFile, rank)
    occupant = getPieceFromLocation(newSquare)    
    
    if isinstance(occupant, Piece):
        if occupant.color == piece.color:
            return False

    return newSquare


# the getOneSquareUp function returns the up adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def getOneSquareUp(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
    file, rank = currentSquare
    if rank == len(BOARD):
        return False

    newRank = rank + 1

    occupant = getPieceFromLocation((file, newRank))
    
    if isinstance(occupant, Piece):
        if occupant.color == piece.color:
            return False

    return (file, newRank)


# the getOneSquareDown function returns the down adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def getOneSquareDown(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
    file, rank = currentSquare
    if rank == 1:
        return False

    newRank = rank - 1
    
    occupant = getPieceFromLocation((file, newRank))
    
    if isinstance(occupant, Piece):
        if occupant.color == piece.color:
            return False

    return (file, newRank)


# diag1 means the diagonal from top left to bottom right
# the getOneSquareDiag1 function returns the diag1 adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def getOneSquareDiag1(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
    file, rank = currentSquare
    if file == "h" or rank == 1:
        return False
    
    newFile = chr(ord(file) + 1)
    newRank = rank - 1    
    newSquare = (newFile, newRank)

    occupant = getPieceFromLocation(newSquare)
    if isinstance(occupant, Piece):
        if (not isinstance(piece, Knight)):
            return False
        
        if occupant.color == piece.color and (not isinstance(piece, Knight)):
            return False
    
    return newSquare


# diag2 means the diagonal from bottom right to top left
# the getOneSquareDiag2 function returns the diag2 adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def getOneSquareDiag2(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
    file, rank = currentSquare
    if file == "a" or rank == len(BOARD):
        return False
    
    newFile = chr(ord(file) - 1)
    newRank = rank + 1
    newSquare = (newFile, newRank)

    occupant = getPieceFromLocation(newSquare)
    if isinstance(occupant, Piece):
        if (not isinstance(piece, Knight)):
            return False
        
        if occupant.color == piece.color and (not isinstance(piece, Knight)):
            return False
    
    return newSquare


# diag3 means the diagonal from top right to bottom left
# the getOneSquareDiag3 function returns the diag3 adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def getOneSquareDiag3(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
    file, rank = currentSquare
    if file == "a" or rank == 1:
        return False
    
    newFile = chr(ord(file) - 1)
    newRank = rank - 1
    newSquare = (newFile, newRank)

    occupant = getPieceFromLocation(newSquare)
    if isinstance(occupant, Piece):
        if (not isinstance(piece, Knight)):
            return False
        
        if occupant.color == piece.color and (not isinstance(piece, Knight)):
            return False
    
    return newSquare


# diag4 means the diagonal from bottom left to top right 
# the getOneSquareDiag4 function returns the diag4 adjacent square of the piece. returns 
# false if the square is occupied by the same color or if the square is off the board
def getOneSquareDiag4(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
    file, rank = currentSquare
    if file == "h" or rank == len(BOARD):
        return False
    
    newFile = chr(ord(file) + 1)
    newRank = rank + 1
    newSquare = (newFile, newRank)

    occupant = getPieceFromLocation(newSquare)
    if isinstance(occupant, Piece):
        if (not isinstance(piece, Knight)):
            return False
        
        if occupant.color == piece.color and (not isinstance(piece, Knight)):
            return False
    
    return newSquare


# this function returns a list of valid moves in a vertical, horizontal, or diagonal direction
# depending on getOneSquareDirFunction
def getValidMovesInStraightDir(piece: Piece, getOneSquareDirFunction, square: tuple[str, int]) -> list:
    validMoves = []
    nextSquare = getOneSquareDirFunction(piece, square)
    
    # while the next square is a valid move for the piece
    while type(nextSquare) == tuple:

        # append that square to the valid move list
        validMoves.append(nextSquare)

        # see one more square ahead
        oneMoreSquare = getOneSquareDirFunction(piece, nextSquare)
        
        # if this future square is not a valid move, then break out of the loop
        if type(oneMoreSquare) != tuple:
            break
        
        # otherwise, update the looping variable
        nextSquare = getOneSquareDirFunction(piece, nextSquare)

    return validMoves