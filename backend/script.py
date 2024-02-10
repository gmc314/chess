from typing import Union

# the board is an 8x8 matrix
BOARD = [[" -- " for i in range(8)] for j in range(8)]

# this is for mapping the board's letters of the files to list indices
fileIndex = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

class Piece:
    def __init__(self, colour: str, name: str, ID: str, location: tuple, canCastle: bool, points: int) -> None:
        self.colour = colour 
        self.name = name
        self.ID = ID
        self.location = location
        self.canCastle = canCastle
        self.points = points

    def __repr__(self) -> str:
        return f"' {self.colour[0]}{self.name} '"


# inheriting from Piece class
class King(Piece):
    def __init__(self, colour, ID, location):
        super().__init__(colour, "K", ID, location, True, 0) 
    
    # self.getCastleMoves() returns the squares which the king can go on if it can castle with a rook    
    def getCastleMoves(self):
        validMoves = []
        if self.canCastle == False:
            return validMoves
        
        # both sets of squares for the castling conditions are defined  
        mapToSquaresForCastling = {
            "Short": getSquaresInStraightDir(self, getOneSquareRight, self.location), # for short castling 
            "Long": getSquaresInStraightDir(self, getOneSquareLeft, self.location) # for long castling 
        }

        # we expect the number of empty squares between the king and rook 
        # to be 2 if short castling and 3 if long castling
        mapToNumberOfEmptySquaresForCastling = {
            "Short": 2,
            "Long": 3
        }

        # the original rook squares according to colour and length of castle
        rookSquares = {
            "Black": {"Short": ("h", 8), 
                      "Long": ("a", 8)}, 

            "White": {"Short": ("h", 1), 
                      "Long": ("a", 1)}
        }

        # castleLength is for the keys of the dictionaries defined above so we can efficiently use space 
        # in writng code and avoid too much repetition
        for castleLength in ["Short", "Long"]:
            castlingDirectionSquares = mapToSquaresForCastling[castleLength]
            # checking if the direction has any obstructions other than the rook
            castlingDirectionSquares = list(filter(lambda sqr: getPieceFromLocation(sqr) == " -- ", 
                                                castlingDirectionSquares))       
                  
            if mapToNumberOfEmptySquaresForCastling[castleLength] == len(castlingDirectionSquares):
                # checking if the rook is on its original square and hasn't moved yet
                rookSquareOccupant = getPieceFromLocation(rookSquares[self.colour][castleLength])

                if isinstance(rookSquareOccupant, Rook) and rookSquareOccupant.canCastle:
                    # this will add the two-square move of the king as a valid move
                    validMoves.append(castlingDirectionSquares[1])

        return validMoves

    def castle(self):
        pass

    # returns one-square moves in all directions
    def getSingleSquareMoves(self):
        validMoves = []
        indexToOneSquareMoveFunctions = {
            0: getOneSquareUp,
            1: getOneSquareDown,
            2: getOneSquareLeft,
            3: getOneSquareRight,
            4: getOneSquareDiagBR,
            5: getOneSquareDiagTL,
            6: getOneSquareDiagBL,
            7: getOneSquareDiagTR
        }

        # looping to get all single square moves in all directions
        for i in range(8):
            validMoves.append(indexToOneSquareMoveFunctions[i](self, self.location))
        
        validMoves = filterListForSquares(validMoves)
    
        return validMoves

    def getValidMoves(self):
        return self.getSingleSquareMoves() + self.getCastleMoves()

    def isMoveValid(self, newSquare):
        # returns a Boolean value depending on if the square is valid 
        return newSquare in self.getValidMoves() 
    

# inheriting from Piece class
class Queen(Piece):
    def __init__(self, colour, ID, location):
        super().__init__(colour, "Q", ID, location, False, 9) 
    
    # getting all valid moves in all directions
    def getValidMoves(self):
        validMoves = []
        indexToOneSquareMoveFunctions = {
            0: getOneSquareUp,
            1: getOneSquareDown,
            2: getOneSquareLeft,
            3: getOneSquareRight,
            4: getOneSquareDiagBR,
            5: getOneSquareDiagTL,
            6: getOneSquareDiagBL,
            7: getOneSquareDiagTR
        }
        
        # looping to get all moves in all directions
        for i in range(8):
            validMoves += getSquaresInStraightDir(self, 
                                                     indexToOneSquareMoveFunctions[i],
                                                     self.location)
        
        return validMoves
    
    def isMoveValid(self, newSquare):
        # returns a Boolean value depending on if the square is valid 
        return newSquare in self.getValidMoves()


# inheriting from Piece class
class Rook(Piece):
    def __init__(self, colour, ID, location):
        super().__init__(colour, "R", ID, location, True, 5)

    # getting the vertical and horizontal moves 
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
            validMoves += getSquaresInStraightDir(self, 
                                                     indexToOneSquareVerticalHorizontalFunctions[i], 
                                                     self.location
                                                     )
        
        # return valid vertical and horizontal moves        
        return validMoves
    
    def isMoveValid(self, newSquare):
        # returns a Boolean value depending on if the square is valid 
        return newSquare in self.getValidMoves()


# inheriting from Piece class
class Bishop(Piece):
    def __init__(self, colour, ID, location):
        super().__init__(colour, "B", ID, location, False, 3) 
    
    def getValidMoves(self):
        validMoves = []
        indexToOneSquareDiagonalFunctions = {
            0: getOneSquareDiagBR,
            1: getOneSquareDiagTL,
            2: getOneSquareDiagBL,
            3: getOneSquareDiagTR
        }
        
        # looping over the four diagonal directions
        for i in range(4):
            validMoves += getSquaresInStraightDir(self, 
                                                     indexToOneSquareDiagonalFunctions[i],
                                                     self.location
                                                     )
        
        # return valid diagonal moves
        return validMoves
    
    def isMoveValid(self, newSquare):
        # returns a Boolean value depending on if the square is valid 
        return newSquare in self.getValidMoves()


# inheriting from Piece class
class Knight(Piece):
    def __init__(self, colour, ID, location):
        super().__init__(colour, "N", ID, location, False, 3) 
    
    # gets a list of valid moves for the Knight
    # for a knight to move, it can go in a diagonal direction one 
    # square regardless if the square is occupied, and then it goes one more 
    # square in an either vertical or horizontal direction 
    # referring to standard chess rules 
    def getValidMoves(self):
        validMoves = []
        diagSquares = []

        # the four one-square diagonal functions
        indexToOneSquareDiagonalFunctions = {
            0: getOneSquareDiagBR,
            1: getOneSquareDiagTL,
            2: getOneSquareDiagBL,
            3: getOneSquareDiagTR
        }
        # getting the squares that are adjacent diagonally 
        for i in range(4):
            diagSquares.append(indexToOneSquareDiagonalFunctions[i](self, self.location))
        
        # keep track of each diagonal square
        oneSquareD1, oneSquareD2, oneSquareD3, oneSquareD4 = diagSquares
        
        # keep the valid squares (not off the board)
        diagSquares = filterListForSquares(diagSquares)
        
        
        # this dictionary maps each diagonal square above to the one square vertical or horizontal 
        # function that follows to get the L-shape
        diagSquaresToKnightMoves = {
            oneSquareD1: [getOneSquareRight, getOneSquareDown],
            oneSquareD2: [getOneSquareLeft, getOneSquareUp],
            oneSquareD3: [getOneSquareLeft, getOneSquareDown],
            oneSquareD4: [getOneSquareRight, getOneSquareUp]
        }
        
        # if the adjacent diagonal square is on the board, check the following 
        # vertical or horizontal square to form the knight's L-shape move
        for sqr in diagSquares:
            knightMove1 = diagSquaresToKnightMoves[sqr][0](self, sqr)
            knightMove2 = diagSquaresToKnightMoves[sqr][1](self, sqr)

            validMoves += [knightMove1, knightMove2]
        # gather all the results after looping through the diagonal squares and
        # filter the list for valid moves 
        validMoves = filterListForSquares(validMoves)

        return validMoves

    def isMoveValid(self, newSquare):
        # returns a Boolean value depending on if the square is valid 
        return newSquare in self.getValidMoves() 


# inheriting from Piece class
class Pawn(Piece):
    def __init__(self, colour, ID, location):
        super().__init__(colour, "P", ID, location, False, 1) 
        # a number variable to track the number of turns for en passant capturing
        self.firstTurn = 0

    # this function returns the possible adjacent diagonal squares that a pawn could capture  
    def getPawnCaptureSquares(self) -> list[tuple]:
        # maps pawn colour to its diagonal capture moves 
        colourToCaptureMoveFunctions = {
            "White": [getOneSquareDiagTL, getOneSquareDiagTR],
            "Black": [getOneSquareDiagBL, getOneSquareDiagBR]
            }
        # the two adjacent diagonal squares stored in a list
        captureSquareDiagLeft = colourToCaptureMoveFunctions[self.colour][0](self, self.location)
        captureSquareDiagRight = colourToCaptureMoveFunctions[self.colour][1](self, self.location)

        captureSquares = [captureSquareDiagLeft, captureSquareDiagRight]
        
        # if any are not valid moves, filter them out
        captureSquares = filterListForSquares(captureSquares)

        return captureSquares

    # gets the diagonal squares for capturing
    def getPawnCaptureMoves(self) -> list[tuple]:
        capturableMoves = []
        captureSquares = self.getPawnCaptureSquares()

        # tracking occupants of the opposite colour for each diagonal move
        for square in captureSquares:
            occupant = getPieceFromLocation(square)

            if isinstance(occupant, Piece) and square != False and self.colour != occupant.colour:
                capturableMoves.append(square)
        
        return capturableMoves

    # gets the one or two square forward moves for the pawn
    def getPawnAdvanceMoves(self):
        validMoves = []

        colourToAdvanceDirectionFunction = {
            "White": getOneSquareUp,
            "Black": getOneSquareDown
        }

        oneSquareAdvance = colourToAdvanceDirectionFunction[self.colour](self, self.location)
        occupant = getPieceFromLocation(oneSquareAdvance)
        
        # if the square in front of the pawn is occupied, the oneSquareAdvance is invalid
        if isinstance(occupant, Piece):
            oneSquareAdvance = False
        
        # if this is the pawn's first turn, can advance two squares
        if self.firstTurn == 0:
            try: # get the two valid moves for a white pawn on the first turn
                validMoves += [oneSquareAdvance, colourToAdvanceDirectionFunction[self.colour](self, oneSquareAdvance)] 

            except TypeError: # if the two-square move is obstructed 
                validMoves.append(oneSquareAdvance)
                
        else: # if it's not the pawn's first turn
            validMoves.append(oneSquareAdvance)

        validMoves = filterListForSquares(validMoves)  
        return validMoves

    # gets the diagonal squares and the adjacent horizontal squares for the en passant capture
    def getEnPassantCaptureMoves(self):
        validMoves = []
        selfRank = self.location[1]
        
        # maps pawn colour to rank for meeting the en passant capture conditions
        colourToCurrentRank = {"White": 5, "Black": 4}
        
        adjacentLeftSquare = getOneSquareLeft(self, self.location)
        adjacentRightSquare = getOneSquareRight(self, self.location)
        
        # storing the occupant's square for the capture function
        adjacentOccupants = []
        adjacentSquares = [adjacentLeftSquare, adjacentRightSquare]
        for sqr in adjacentSquares:
            if sqr != False:
                occupant = getPieceFromLocation(sqr)
                
                if occupant != " -- ":
                    adjacentOccupants.append(occupant)
        
        adjacentSquares = [occ.location for occ in adjacentOccupants if isinstance(occ, Pawn)]      
        
        # loop over the available left and right adjacent squares to see if there are any pawna on them
        for square in adjacentSquares:
            file = square[0]
            occupant = getPieceFromLocation(square)
            occRank = square[1]

            # if a pawn of opposite colour moves two squares forward on its first turn
            if occupant.colour != self.colour and \
                selfRank == occRank == colourToCurrentRank[self.colour] and \
                   occupant.firstTurn == 1:
                
                # if the condition above holds, the we get the diagonal
                # squares for the pawn to move to as per en passant
                captureSquares = self.getPawnCaptureSquares()
                
                for cSqr in captureSquares:
                    cFile = cSqr[0]
                    if cFile == file and getPieceFromLocation(cSqr) == " -- ":
                        validMoves.append(cSqr)
                        
        return [validMoves, adjacentSquares]
        
    def getValidMoves(self):
        # valid moves from Pawn capture and move functions 
        validMoves = self.getPawnCaptureMoves() + self.getPawnAdvanceMoves() + self.getEnPassantCaptureMoves()[0]
        return validMoves
    
    def isMoveValid(self, newSquare):
        # returns a Boolean value depending on if the square is valid 
        return newSquare in self.getValidMoves() 
        

class Player:
    def __init__(self, colour: str, points: int, pieces: list[Piece]) -> None:
        self.colour = colour
        self.points = points
        self.pieces = pieces

    def __repr__(self) -> str:
        pluralS = "" if self.points == 1 else "s"
        return f"{self.colour} with {self.points} point{pluralS}"    
    
WHITE = Player("White", 0, [])
BLACK = Player("Black", 0, [])

colourToPlayer = {
    "White": WHITE,
    "Black": BLACK
}

####################################################
## Functions 
####################################################

# this function returns the string
# MODIFIES: BOARD
def clearBoard():
    for i in range(8): 
        for j in range(8):
            BOARD[i][j] = " -- "
    
    return "Board Cleared"

# gets the indices of the Board from rank and file 
def getBoardIndexFromRankAndFile(square: tuple[str, int]):
    file, rank = square
    col = fileIndex[file]
    row = len(BOARD) - rank
    return (row, col)


# filters the list for squares instead of False
def filterListForSquares(squareList: list) -> list:
    return list(filter(lambda x: isinstance(x, tuple), squareList))


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
# MODIFIES: BOARD
def placePiece(piece: Piece) -> str:
    currentSquare = piece.location
    row, col = getBoardIndexFromRankAndFile(currentSquare)
    BOARD[row][col] = piece
    
    colourToPlayer[piece.colour].pieces.append(piece)

    return f"{piece} placed"


# this function does the process of capturing where
# the capturer piece captures the capturee piece
# MODIFIES: BOARD 
# returns a verification message
def capture(capturer: Piece, capturee: Piece) -> str:
    
    if isinstance(capturer, Pawn) and isinstance(capturee, Pawn) and capturer.getEnPassantCaptureMoves()[1] != []:
        # if the pawn is capturing en passant, it moves to the forward diagonal square
        moveSquares = capturer.getEnPassantCaptureMoves()[0]
        occupantSquares = capturer.getEnPassantCaptureMoves()[1]
        captureeFile = capturee.location[0]
        # the current BOARD location of the capturee
        captureeRow, captureeCol = getBoardIndexFromRankAndFile(capturee.location)
        
        # the current BOARD location of the capturer
        capturerRow, capturerCol = getBoardIndexFromRankAndFile(capturer.location)
        
        if capturee.location in occupantSquares:
            # take the diag square that has the same file as the capturee
            for mSqr in moveSquares:
                file = mSqr[0] 
                
                if file == captureeFile:
                    # moving the capturee off the board
                    BOARD[captureeRow][captureeCol] = " -- "

                    # moving the attacking pawn from the current square
                    BOARD[capturerRow][capturerCol] = " -- "
                    
                    # moving the attacking pawn to the adjacent diagonal square
                    capturerRow, capturerCol = getBoardIndexFromRankAndFile(mSqr)
                    BOARD[capturerRow][capturerCol] = capturer

                    # add points to player
                    colourToPlayer[capturer.colour].points += capturee.points
                    
                    return f"{capturee.colour[0]}{capturee.name} captured en passant."

    # non en-passant case
    captureeRow, captureeCol = getBoardIndexFromRankAndFile(capturee.location)
    
    # delete capturee from the board
    BOARD[captureeRow][captureeCol] = " -- "
    capturer.location = capturee.location

    # the capturer gets the capturee's location
    BOARD[captureeRow][captureeCol] = capturer
    
    # add points to player
    colourToPlayer[capturer.colour].points += capturee.points
                    
    return f"{capturee.colour[0]}{capturee.name} captured."


# move piece from current square to new `square`
# MODIFIES: BOARD
def moveFromCurrentSquare(piece: Union[King, Queen, Rook, Bishop, Knight, Pawn], newSquare: tuple[str, int]) -> str:
    if not piece.isMoveValid(newSquare):
        return "invalid move"   

    currentSquare = piece.location
    currentRow, currentCol = getBoardIndexFromRankAndFile(currentSquare)
    
    if isinstance(piece, Pawn) and piece.getEnPassantCaptureMoves()[0] != []:
        enPassantMoves = piece.getEnPassantCaptureMoves()[0]

        if newSquare not in enPassantMoves:
            return "invalid move"
        
        enPassantCaptureSquares = piece.getEnPassantCaptureMoves()[1]
        
        # if the space is occupied:
        for cSqr in enPassantCaptureSquares:
            occupant = getPieceFromLocation(cSqr)
            
            if occupant != " -- ":
                # call the capture function and print out the message
                captureMessage = capture(piece, occupant)
            else:
                captureMessage = ""
        
        return f"{piece.name} {stringifyRankFile(currentSquare)} to {stringifyRankFile(newSquare)}. {captureMessage}"

    # non en-passant case:
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
    if isinstance(piece, Pawn) and piece.firstTurn <= 2:
        piece.firstTurn += 1

    # coniditon for castling
    elif isinstance(piece, Rook):
        piece.canCastle = False

    # print out the move 
    return f"{piece.name} {stringifyRankFile(currentSquare)} to {stringifyRankFile(newSquare)}. {captureMessage}"


# the getOneSquareLeft function returns the left adjacent square of the piece. returns 
# false if the square is occupied by the same colour or if the square is off the board
def getOneSquareLeft(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
    file, rank = currentSquare
    if file == "a":
        return False

    newFile = chr(ord(file) - 1)
    newSquare = (newFile, rank)
    occupant = getPieceFromLocation(newSquare)
    
    if isinstance(occupant, Piece):
        if occupant.colour == piece.colour:
            return False
        
    return newSquare


# the getOneSquareRight function returns the right adjacent square of the piece. returns 
# false if the square is occupied by the same colour or if the square is off the board
def getOneSquareRight(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
    file, rank = currentSquare
    if file == "h":
        return False

    newFile = chr(ord(file) + 1)
    newSquare = (newFile, rank)
    occupant = getPieceFromLocation(newSquare)    
    
    if isinstance(occupant, Piece):
        if occupant.colour == piece.colour:
            return False

    return newSquare


# the getOneSquareUp function returns the up adjacent square of the piece. returns 
# false if the square is occupied by the same colour or if the square is off the board
def getOneSquareUp(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
    file, rank = currentSquare
    if rank == len(BOARD):
        return False

    newRank = rank + 1

    occupant = getPieceFromLocation((file, newRank))
    
    if isinstance(occupant, Piece):
        if occupant.colour == piece.colour:
            return False

    return (file, newRank)


# the getOneSquareDown function returns the down adjacent square of the piece. returns 
# false if the square is occupied by the same colour or if the square is off the board
def getOneSquareDown(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
    file, rank = currentSquare
    if rank == 1:
        return False

    newRank = rank - 1
    
    occupant = getPieceFromLocation((file, newRank))
    
    if isinstance(occupant, Piece):
        if occupant.colour == piece.colour:
            return False

    return (file, newRank)


# diagBR means the diagonal from top left to bottom right
# the function returns the diagBR adjacent square of the piece. returns 
# false if the square is occupied by the same colour or if the square is off the board
def getOneSquareDiagBR(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
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
        
        if occupant.colour == piece.colour and (not isinstance(piece, Knight)):
            return False
    
    return newSquare


# diagTL means the diagonal from bottom right to top left
# the function returns the diagTL adjacent square of the piece. returns 
# false if the square is occupied by the same colour or if the square is off the board
def getOneSquareDiagTL(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
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
        
        if occupant.colour == piece.colour and (not isinstance(piece, Knight)):
            return False
    
    return newSquare


# diagBL means the diagonal from top right to bottom left
# the getOneSquareDiag3 function returns the diagBL adjacent square of the piece. returns 
# false if the square is occupied by the same colour or if the square is off the board
def getOneSquareDiagBL(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
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
        
        if occupant.colour == piece.colour and (not isinstance(piece, Knight)):
            return False
    
    return newSquare


# diagTR means the diagonal from bottom left to top right 
# the function returns the diagTR adjacent square of the piece. returns 
# false if the square is occupied by the same colour or if the square is off the board
def getOneSquareDiagTR(piece: Piece, currentSquare: tuple[str, int]) -> Union[bool, tuple[str, int]]:
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
        
        if occupant.colour == piece.colour and (not isinstance(piece, Knight)):
            return False
    
    return newSquare


# this function returns a list of valid moves in a vertical, horizontal, or diagonal direction
# depending on getOneSquareDirFunction
def getSquaresInStraightDir(piece: Piece, getOneSquareDirFunction, square: tuple[str, int]) -> list:
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