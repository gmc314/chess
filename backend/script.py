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
        validMoves = []
        indexToOneSquareMoveFunctions = {
            0: getOneSquareUp,
            1: getOneSquareDown,
            2: getOneSquareLeft,
            3: getOneSquareRight,
            4: getOneSquareDiag1,
            5: getOneSquareDiag2,
            6: getOneSquareDiag3,
            7: getOneSquareDiag4
        }
        for i in range(8):
            validMoves.append(indexToOneSquareMoveFunctions[i](self, self.location))
        
        validMoves = list(filter(lambda x: x != False, validMoves))
    
        return validMoves

    def isMoveValid(self, newSquare):
        return newSquare in self.getValidMoves()
        

class Queen(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Q", ID, location, False, 9) 
    
    # getting all valid moves in all directions
    def getValidMoves(self):
        validMoves = []
        indexToOneSquareMoveFunctions = {
            0: getOneSquareUp,
            1: getOneSquareDown,
            2: getOneSquareLeft,
            3: getOneSquareRight,
            4: getOneSquareDiag1,
            5: getOneSquareDiag2,
            6: getOneSquareDiag3,
            7: getOneSquareDiag4
        }
        
        # looping to get all moves in all directions
        for i in range(8):
            validMoves += getValidMovesInStraightDir(self, indexToOneSquareMoveFunctions[i], self.location)
        
        # return valid vertical and horizontal moves        
        return validMoves
    
    def isMoveValid(self, newSquare):
        return newSquare in self.getValidMoves()
    
class Rook(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "R", ID, location, True, 5)

    def getValidMoves(self):
        validMoves = []
        indexToOneSquareVerticalHorizontalFunctions = {
            0: getOneSquareUp,
            1: getOneSquareDown,
            2: getOneSquareLeft,
            3: getOneSquareRight
        }
        
        # looping over the four vertical and horizontal directions
        for i in range(4):
            validMoves += getValidMovesInStraightDir(self, indexToOneSquareVerticalHorizontalFunctions[i], self.location)
        
        # return valid vertical and horizontal moves        
        return validMoves
    
    def isMoveValid(self, newSquare):
        return newSquare in self.getValidMoves()
    

class Bishop(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "B", ID, location, False, 3) 
    
    def getValidMoves(self):
        validMoves = []
        indexToOneSquareDiagonalFunctions = {
            0: getOneSquareDiag1,
            1: getOneSquareDiag2,
            2: getOneSquareDiag3,
            3: getOneSquareDiag4
        }
        
        # looping over the four diagonal directions
        for i in range(4):
            validMoves += getValidMovesInStraightDir(self, indexToOneSquareDiagonalFunctions[i], self.location)
        
        # return valid diagonal moves
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
        validMoves = []
        # the four diagonal directions 
        oneSquareD1 = getOneSquareDiag1(self, currentSquare)
        oneSquareD2 = getOneSquareDiag2(self, currentSquare)
        oneSquareD3 = getOneSquareDiag3(self, currentSquare)
        oneSquareD4 = getOneSquareDiag4(self, currentSquare)
        
        diagSquares = [oneSquareD1, oneSquareD2, oneSquareD3, oneSquareD4]
        diagSquares = list(filter(lambda x: isinstance(x, tuple), diagSquares))
        
        diagSquaresIndexToKnightMoves = {
            oneSquareD1: [getOneSquareRight, getOneSquareDown],
            oneSquareD2: [getOneSquareLeft, getOneSquareUp],
            oneSquareD3: [getOneSquareLeft, getOneSquareDown],
            oneSquareD4: [getOneSquareRight, getOneSquareUp]
        }
        # if the diagonal is on the board, then check the vertical or horizontal adjacent squares
        for sqr in diagSquares:
            knightMove1 = diagSquaresIndexToKnightMoves[sqr][0](self, sqr)
            knightMove2 = diagSquaresIndexToKnightMoves[sqr][1](self, sqr)
            # gather all the results after looping through the diagonal squares
            validMoves += [knightMove1, knightMove2]
                    
        # filter list for valid moves 
        validMoves = list(filter(lambda x: x != False, validMoves))

        return validMoves

    def isMoveValid(self, newSquare):
        # returns a Boolean value depending on if the square is valid 
        return newSquare in self.getValidMoves() 
        

class Pawn(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "P", ID, location, False, 1) 
        # a number variable to track the number of turns for en passant capturing
        self.firstTurn = 0

    # this function returns the possible adjacent diagonal squares that a pawn could capture  
    def getPawnCaptureSquares(self) -> list[tuple]:
        # maps pawn colour to its diagonal capture moves 
        colorToCaptureMoveFunctions = {
            "White": [getOneSquareDiag2, getOneSquareDiag4],
            "Black": [getOneSquareDiag3, getOneSquareDiag1]
            }
        # the two adjacent diagonal squares stored in a list
        captureSquareDiagLeft = colorToCaptureMoveFunctions[self.color][0](self, self.location)
        captureSquareDiagRight = colorToCaptureMoveFunctions[self.color][1](self, self.location)

        captureSquares = [captureSquareDiagLeft, captureSquareDiagRight]
        
        # if any are not valid moves, filter them out
        captureSquares = list(filter(lambda x: isinstance(x, tuple), captureSquares))

        return captureSquares

    def getPawnCaptureMoves(self) -> list[tuple]:
        capturableMoves = []
        captureSquares = self.getPawnCaptureSquares()

        # tracking occupants of the opposite colour for each diagonal move
        for square in captureSquares:
            occupant = getPieceFromLocation(square)

            if isinstance(occupant, Piece) and square != False and self.color != occupant.color:
                capturableMoves.append(square)
        
        return capturableMoves

    def getPawnAdvanceMoves(self):
        validMoves = []

        colorToAdvanceDirectionFunction = {
            "White": getOneSquareUp,
            "Black": getOneSquareDown
        }

        oneSquareAdvance = colorToAdvanceDirectionFunction[self.color](self, self.location)
        occupant = getPieceFromLocation(oneSquareAdvance)

        if isinstance(occupant, Piece):
            oneSquareAdvance = False
        
        # if this is the pawn's first turn, can advance two squares
        if self.firstTurn == 0:
            try: # get the two valid moves for a white pawn on the first turn
                validMoves += [oneSquareAdvance, colorToAdvanceDirectionFunction[self.color](self, oneSquareAdvance)] 

            except TypeError: # if the two-square move is obstructed 
                validMoves.append(oneSquareAdvance)
                
        else: # if it's not the pawn's first turn
            validMoves.append(oneSquareAdvance)

        validMoves = list(filter(lambda x: isinstance(x, tuple), validMoves))    
        return validMoves

    def getEnPassantCaptureMoves(self):
        validMoves = []
        selfRank = self.location[1]
        occupantSquares = []
        # maps pawn colour to rank for meeting the en passant capture conditions
        colorToCurrentRank = {"White": 4, "Black": 6}
        
        adjacentLeftSquare = getOneSquareLeft(self, self.location)
        adjacentRightSquare = getOneSquareRight(self, self.location)
        adjacentSquares = [adjacentLeftSquare, adjacentRightSquare]
        adjacentSquares = list(filter(lambda x: isinstance(x, tuple), adjacentSquares))
        
        for square in adjacentSquares:
            file = square[0]
            occupant = getPieceFromLocation(square)

            # if a pawn of opposite color moves two squares forward on its first turn
            if isinstance(occupant, Pawn) and occupant.color != self.color \
                and selfRank == occRank == colorToCurrentRank[self.color] \
                    and occupant.firstTurn == 1:
                occRank = square[1]
                captureSquares = self.getPawnCaptureSquares()
                
                for cSqr in captureSquares:
                    cFile = cSqr[0]
                    if cFile == file:
                        validMoves.append(cSqr)
                        occupantSquares.append(occupant.location)

        return [validMoves, occupantSquares]
        
    def getValidMoves(self):
        # valid moves from Pawn capture and move functions 
        validMoves = self.getPawnCaptureMoves() + self.getPawnAdvanceMoves() + self.getEnPassantCaptureMoves()[0]
        return validMoves
    
    def isMoveValid(self, newSquare):
        return newSquare in self.getValidMoves()
    
    
####################################################
## Functions 
####################################################
    

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


# returns the piece at the specific square,
# or the empty square if there isn't a piece on the square
def getPieceFromLocation(square: tuple[str, int]) -> Union[Piece, str]:
    r, c = getBoardIndexFromRankAndFile(square)
    return BOARD[r][c]


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
    if type(piece) == Pawn and piece.firstTurn <= 2:
        piece.firstTurn += 1

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