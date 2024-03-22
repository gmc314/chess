from typing import Union

# the board is an 8x8 matrix
boardLength = 8
emptySquare = " -- "
BOARD = [[emptySquare for i in range(boardLength)] for j in range(boardLength)]

# this is for mapping the board's letters of the files to list indices
fileIndex = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

class Player:
    def __init__(self, colour: str, points: int, pieces: list) -> None:
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


def oppositeColour(colour):
    return "Black" if colour == "White" else "White"

class Piece:
    def __init__(self, colour: str, symbol: str, ID: str, location: tuple, canCastle: bool, captured: bool, points: int) -> None:
        self.colour = colour 
        self.symbol = symbol
        self.ID = ID
        self.location = location
        self.canCastle = canCastle
        self.captured = captured
        self.points = points

    def __repr__(self) -> str:
        return f"' {self.colour[0]}{self.symbol} '"

    def __str__(self) -> str:
        symbolToName = {"K": "King",
                        "Q": "Queen",
                        "R": "Rook",
                        "B": "Bishop",
                        "N": "Knight",
                        "P": "Pawn"}
        
        return f"{self.colour} {symbolToName[self.symbol]}"


# inheriting from Piece class
class King(Piece):
    def __init__(self, colour, ID, location):
        super().__init__(colour, "K", ID, location, canCastle=True, captured=False, points=0)
        
    # checks if the squares between rook and king are not defended as per rules of castling
    def checkEmptyCastleSquaresForThreatenedSquares(self, squaresBetweenKingAndRook: list[tuple[str, int]]) -> bool:
        opponentColour = oppositeColour(self.colour)
        opponentPlayer = colourToPlayer[opponentColour]
        
        for sqr in squaresBetweenKingAndRook:
            for piece in opponentPlayer.pieces:
                if squareDefended(sqr, piece):
                    return True
                
        return False 
                    
    # self.getCastleMoves() returns the squares which the king can go on if it can castle with a rook    
    def getCastleMoves(self):
        validMoves = []
        kingStartingSquare = {"Black": ("e", 8),
                              "White": ("e", 1)}
        
        if self.location != kingStartingSquare[self.colour] or self.canCastle == False:
            return validMoves
        
        # both sets of squares for the castling conditions are defined  
        castleLengthToSquaresForCastling = {
            "Kingside": getSquaresInStraightDir(self, getOneSquareRight, self.location), # for Kingside castling 
            "Queenside": getSquaresInStraightDir(self, getOneSquareLeft, self.location) # for Queenside castling 
        }

        # we expect the number of empty squares between the king and rook 
        # to be 2 if Kingside castling and 3 if Queenside castling
        castleLengthToNumberOfEmptySquaresForCastling = {
            "Kingside": 2,
            "Queenside": 3
        }

        # the original rook squares according to colour and length of castle
        rookSquares = {
            "Black": {
                "Kingside": ("h", 8), 
                "Queenside": ("a", 8)
                }, 
            "White": {
                "Kingside": ("h", 1),
                "Queenside": ("a", 1)
                }
        }

        # castleLength is for the keys of the dictionaries defined above so we can efficiently use space 
        # in writng code and avoid too much repetition
        for castleLength in ["Kingside", "Queenside"]:
            castlingDirectionSquares = castleLengthToSquaresForCastling[castleLength]
            # filtering for empty squares
            castlingDirectionSquares = list(filter(lambda sqr: getPieceFromLocation(sqr) == emptySquare, 
                                                castlingDirectionSquares))
            
            # if the squares between the king and rook are attacked, can't castle in that direction 
            if self.checkEmptyCastleSquaresForThreatenedSquares(castlingDirectionSquares):
                continue 
            
            # checking if the direction has any obstructions other than the rook
            if castleLengthToNumberOfEmptySquaresForCastling[castleLength] == len(castlingDirectionSquares):
                rookSquareOccupant = getPieceFromLocation(rookSquares[self.colour][castleLength])
                
                # checking if the rook is on its original square and hasn't moved yet
                if isinstance(rookSquareOccupant, Rook) and rookSquareOccupant.canCastle:
                
                    # this will add the two-square move of the king as a valid move
                    validMoves.append(castlingDirectionSquares[1])

        return validMoves

    # returns one-square moves in all directions
    def getSingleSquareMoves(self):
        validMoves = []
        oneSquareMoveFunctions = [
            getOneSquareUp,getOneSquareDown,getOneSquareLeft,getOneSquareRight,
            getOneSquareDiagBR,getOneSquareDiagTL,getOneSquareDiagBL,getOneSquareDiagTR
            ]
        # looping to get all single square moves in all directions
        for moveFunction in oneSquareMoveFunctions:
            validMoves.append(moveFunction(self, self.location))
        
        validMoves = filterListForSquares(validMoves)
    
        return validMoves

    def getValidMoves(self):
        moves = self.getSingleSquareMoves() + self.getCastleMoves()
        return moves
        
    
    def isMoveValid(self, newSquare):
        # returns a Boolean value depending on if the square is valid 
        return newSquare in self.getValidMoves() 
    

# inheriting from Piece class
class Queen(Piece):
    def __init__(self, colour, ID, location):
        super().__init__(colour, "Q", ID, location, canCastle=False, captured=False, points=9)  
    # getting all valid moves in all directions
    def getValidMoves(self):
        validMoves = []
        oneSquareMoveFunctions = [
            getOneSquareUp,getOneSquareDown,getOneSquareLeft,getOneSquareRight,
            getOneSquareDiagBR,getOneSquareDiagTL,getOneSquareDiagBL,getOneSquareDiagTR
            ]
        
        # looping to get all single square moves in all directions
        for oneSquareFunction in oneSquareMoveFunctions:
            validMoves += getSquaresInStraightDir(
                self, 
                oneSquareFunction,
                self.location
                )
        return validMoves
    
    def isMoveValid(self, newSquare):
        # returns a Boolean value depending on if the square is valid 
        return newSquare in self.getValidMoves()


# inheriting from Piece class
class Rook(Piece):
    def __init__(self, colour, ID, location):
        super().__init__(colour, "R", ID, location, canCastle=True, captured=False, points=5)
        
    # getting the vertical and horizontal moves 
    def getValidMoves(self):
        validMoves = []
        oneSquareVerticalHorizontalFunctions = [
            getOneSquareUp,
            getOneSquareDown,
            getOneSquareLeft,
            getOneSquareRight
        ]
        
        # looping over the four vertical and horizontal directions
        for oneSquareFunction in oneSquareVerticalHorizontalFunctions:
            validMoves += getSquaresInStraightDir(
                self, 
                oneSquareFunction, 
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
        super().__init__(colour, "B", ID, location, canCastle=False, captured=False, points=3) 
         
    def getValidMoves(self):
        validMoves = []
        oneSquareDiagonalFunctions = [
            getOneSquareDiagBR,
            getOneSquareDiagTL,
            getOneSquareDiagBL,
            getOneSquareDiagTR
            ]
        
        # looping over the four diagonal directions
        for oneSquareFunction in oneSquareDiagonalFunctions:
            validMoves += getSquaresInStraightDir(
                self, 
                oneSquareFunction,
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
        super().__init__(colour, "N", ID, location, canCastle=False, captured=False, points=3) 
        
    # gets a list of valid moves for the Knight
    # for a knight to move, it can go in a diagonal direction one 
    # square regardless if the square is occupied, and then it goes one more 
    # square in an either vertical or horizontal direction 
    # referring to standard chess rules 
    def getValidMoves(self):
        validMoves = []
        diagSquares = []

        # the four one-square diagonal functions
        oneSquareDiagonalFunctions = [
            getOneSquareDiagBR,
            getOneSquareDiagTL,
            getOneSquareDiagBL,
            getOneSquareDiagTR
        ]

        # getting the squares that are adjacent diagonally 
        for oneSquareFunction in oneSquareDiagonalFunctions:
            diagSquares.append(oneSquareFunction(self, self.location))
        
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
        super().__init__(colour, "P", ID, location, canCastle=False, captured=False, points=1) 
        # a number variable to track the number of turns for en passant capturing
        self.numMoves = 0

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
        if self.numMoves == 0:
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
                
                if occupant != emptySquare:
                    adjacentOccupants.append(occupant)
        
        adjacentSquares = [occ.location for occ in adjacentOccupants if isinstance(occ, Pawn)]      
        
        # loop over the available left and right adjacent squares to see if there are any pawna on them
        for square in adjacentSquares:
            file = square[0]
            occupant = getPieceFromLocation(square)
            occRank = square[1]

            # if a pawn of the opposite colour moves two squares forward on its first turn
            if occupant.colour != self.colour and \
                selfRank == occRank == colourToCurrentRank[self.colour] and \
                   occupant.numMoves == 1:
                
                # we get the diagonal squares for the pawn 
                # to move as per en passant
                captureSquares = self.getPawnCaptureSquares()
                
                # loop through the two possible diagonal squares to see if they are valid moves
                for cSqr in captureSquares:
                    cFile = cSqr[0]
                    if cFile == file and getPieceFromLocation(cSqr) == emptySquare:
                        # if yes, add the square to the valid moves list
                        validMoves.append(cSqr)
                        
        return [validMoves, adjacentSquares]
        
    def getValidMoves(self):
        # valid moves from Pawn capture and move functions 
        validMoves = self.getPawnCaptureMoves() + self.getPawnAdvanceMoves() + self.getEnPassantCaptureMoves()[0]
        return validMoves
    
    def isMoveValid(self, newSquare):
        # returns a Boolean value depending on if the square is valid 
        return newSquare in self.getValidMoves() 
 


####################################################
## Functions 
####################################################

# this function returns the string "Board Cleared" if called and clears the board of all pieces currently on it.
# MODIFIES: BOARD
def clearBoard():
    for i in range(boardLength): 
        for j in range(boardLength):
            if isinstance(BOARD[i][j], Piece):
                piece = BOARD[i][j]
                del piece # delete the piece from memory
            BOARD[i][j] = emptySquare

    # remove all pieces from both players 
    for colour in ["White", "Black"]:
        colourToPlayer[colour].pieces = []
    return "Board Cleared"


# this function returns True if the square is valid. False otherwise 
def isSquareValid(square: tuple[str, int]):
    # detecting for the right input
    if not type(square) == tuple:
        return False

    try:
        file, rank = square
    
    except ValueError: 
        return False

    # in case if the key is not in the fileIndex dictionary
    try:
        fileIndex[file]
    
    except KeyError:
        return False

    # return a bool based on if rank is on or off the board
    return 1 <= rank <= boardLength


# gets the indices of the Board from rank and file 
def getBoardIndexFromRankAndFile(square: tuple[str, int]):
    if not isSquareValid(square):
        return "Invalid"

    file, rank = square
    col = fileIndex[file]    
    row = boardLength - rank

    return (row, col)


# filters the list for squares instead of False
def filterListForSquares(squareList: list) -> list:
    try:
        lst = list(filter(lambda sqr: isSquareValid(sqr), squareList))
    
    except TypeError:
        return []
    
    return lst


# gets the rank and file from indices of the Board
def getRankAndFileFromBoardIndex(row: int, col: int):
    # checking if row and col are integers between 0 and 7
    if type(row) != int or type(col) != int or not (0 <= row <= 7) or not (0 <= col <= 7): 
        return "Invalid"
    
    file = list(fileIndex.keys())[list(fileIndex.values()).index(col)]
    rank = boardLength - row 
    
    return (file, rank)


# returns the piece at the specific square,
# or the empty square if there isn't a piece on the square
def getPieceFromLocation(square: tuple[str, int]) -> Union[Piece, str]:
    try:
        r, c = getBoardIndexFromRankAndFile(square)
    
    except ValueError:
        return "Invalid"
    
    return BOARD[r][c]


# converts the rank and file tuple to a string
# returns a capital letter followed by a number 
def stringifyRankFile(square: tuple[str, int]) -> str:
    if not isSquareValid(square):
        return False
    
    else:
        return f"{square[0].upper()}{square[1]}"


# place a piece on the board at its initial square. 
# returns a verification message
# MODIFIES: BOARD
def placePiece(piece: Piece) -> str:
    currentSquare = piece.location
    row, col = getBoardIndexFromRankAndFile(currentSquare)
    BOARD[row][col] = piece
    
    colourToPlayer[piece.colour].pieces.append(piece)

    return str(piece) + " placed"


# this function does the process of capturing where
# the capturer piece captures the capturee piece
# MODIFIES: BOARD 
# returns a verification message
def capture(capturer: Piece, capturee: Piece) -> str:
    # if the pawn is capturing en passant, it moves to the forward diagonal square
    if isinstance(capturer, Pawn) and isinstance(capturee, Pawn) and capturer.getEnPassantCaptureMoves()[1] != []:
        enPassantMoveSquares = capturer.getEnPassantCaptureMoves()[0]
        occupantSquares = capturer.getEnPassantCaptureMoves()[1]
        captureeFile = capturee.location[0]

        # the current BOARD location of the capturee
        captureeRow, captureeCol = getBoardIndexFromRankAndFile(capturee.location)
        
        # the current BOARD location of the capturer
        capturerRow, capturerCol = getBoardIndexFromRankAndFile(capturer.location)
        
        if capturee.location in occupantSquares:
            # take the diag square that has the same file as the capturee
            for sqr in enPassantMoveSquares:
                file = sqr[0] 
                
                if file == captureeFile:
                    # moving the capturee off the board
                    BOARD[captureeRow][captureeCol] = emptySquare

                    # set captured parameter to True
                    capturee.captured = True

                    # moving the attacking pawn from the current square
                    BOARD[capturerRow][capturerCol] = emptySquare
                    
                    # moving the attacking pawn to the adjacent diagonal square
                    capturerRow, capturerCol = getBoardIndexFromRankAndFile(sqr)
                    capturer.location = getRankAndFileFromBoardIndex(capturerRow, capturerCol)
                    BOARD[capturerRow][capturerCol] = capturer

                    # add points to player
                    colourToPlayer[capturer.colour].points += capturee.points

                    # remove piece from player's piece list
                    colourToPlayer[capturee.colour].pieces.remove(capturee)

                    return f"{str(capturee)} captured en passant."

    # non en-passant case:
    # settting captured Piece parameter to True
    capturee.captured = True
    captureeRow, captureeCol = getBoardIndexFromRankAndFile(capturee.location)
    
    # delete capturee from the board
    BOARD[captureeRow][captureeCol] = emptySquare
    
    # the capturer gets the capturee's location
    capturer.location = capturee.location
    BOARD[captureeRow][captureeCol] = capturer
    
    # add points to player 
    colourToPlayer[capturer.colour].points += capturee.points
                  
    # remove piece from player's piece list
    colourToPlayer[capturee.colour].pieces.remove(capturee)

    return f"{str(capturee)} captured."


# assuming the king can castle, this function moves the rook to castling position 
# in response to the king's move
# kingMoveSquare is the square the king moves to to castle  
# MODIFIES: BOARD
def castle(king: King, kingMoveSquare: tuple[str, int]) -> str:
    moveFile = kingMoveSquare[0]
    
    # if the king Queenside castles (and is on the c file), the rook moves to the adjacent right square
    # if the king Kingside castles (and is on the g file), the rook moves to the adjacent left square
    fileToDirectionForRook = {"g": getOneSquareLeft, 
                              "c": getOneSquareRight
                              }
    
    # getting locations of rooks 
    kingFileToRookFile = {"g": "h",
                          "c": "a"
                          }
    
    colorToRookRank = {"Black": 8,
                       "White": 1
                       }
    
    # getting the messages for castling
    kingFileToCastleMessage = {"g": " kingside castled.",
                               "c": " queenside castled."
                               }
    
    rook = getPieceFromLocation((kingFileToRookFile[moveFile], colorToRookRank[king.colour]))
    if rook.canCastle:
        # moves the rook to the correct position for castling
        currentRookRow, currrentRookCol = getBoardIndexFromRankAndFile(rook.location)
        BOARD[currentRookRow][currrentRookCol] = emptySquare

        newRookLocation = fileToDirectionForRook[moveFile](king, king.location)
        newRookRow, newRookCol = getBoardIndexFromRankAndFile(newRookLocation)
        rook.location = newRookLocation

        BOARD[newRookRow][newRookCol] = rook
        rook.canCastle = False
        return str(king) + kingFileToCastleMessage[moveFile]


# replaces the pawn with a piece with pieceSymbol 
# requires symbol to be one of Q, B, R, N
def pawnPromotion(pawn: Pawn, pieceSymbol: str) -> Union[Queen, Rook, Bishop, Knight]:
    # tracks white to 8 (the rank of which the pawn is promoted)
    # and black to 1
    colourToPromotionRank = {
        "White": 8,
        "Black": 1
        }    
    symbolToClass = {
        "Q": Queen,
        "N": Knight, 
        "B": Bishop,
        "R": Rook
        }
    # if the pawn is in the most forward rank for promotion,
    # return the new class of piece 
    if pawn.location[1] == colourToPromotionRank[pawn.colour]:
        # get a new instance of the class at the pawn's location
        newPiece = symbolToClass[pieceSymbol](pawn.colour, pieceSymbol, pawn.location)
        return newPiece
    

# move piece from current square to new `square`
# MODIFIES: BOARD
def moveFromCurrentSquare(piece: Piece, newSquare: tuple[str, int]) -> str:
    invalid = "invalid move"
    playerPieces = colourToPlayer[piece.colour].pieces
    # check if the piece is on the board 
    if piece not in playerPieces or not piece.isMoveValid(newSquare) or piece.captured:
        return invalid
    
    opponent = colourToPlayer[oppositeColour(piece.colour)]
    if isinstance(piece, King):
        # indirect check squares for king 
        indirectCheckMoves = list(filter(lambda m: kingIsInIndirectCheck(piece, m), piece.getValidMoves()))
        
        # if the move puts the king in check when the king is indirectly threatened
        if newSquare in indirectCheckMoves:
            return invalid

        # if the king doesn't move to a castling square
        if newSquare not in piece.getCastleMoves():
            piece.canCastle = False
            
        # if the king moves to a castling square
        elif newSquare in piece.getCastleMoves():
            currentRow, currentCol = getBoardIndexFromRankAndFile(piece.location) 
            
            newRow, newCol = getBoardIndexFromRankAndFile(newSquare)
            newRank, newFile = getRankAndFileFromBoardIndex(newRow, newCol)
            
            # move king from the current square
            BOARD[currentRow][currentCol] = emptySquare
            # to new square
            BOARD[newRow][newCol] = piece
            piece.location = (newRank, newFile)
            
            # castle function handles the rook
            message = castle(piece, newSquare)
            piece.canCastle = False
            return message
    
    # for testing purposes: if there's a king on the board
    try:
        # if the piece isn't the king but the king is in check and the piece can't block the check:
        king = [p for p in colourToPlayer[piece.colour].pieces if isinstance(piece, King)][0]
        for opponentPiece in opponent.pieces:
            if kingIsInCheck(king, opponentPiece):
                blockCheck = canBlockCheck(piece, opponentPiece, king)
    
                # if the piece can't block the check against the king, return invalid
                if not blockCheck[0]:      
                    return invalid
                
                # if the check can be blocked, restrict the valid moves 
                else:
                    newValidMoves = blockCheck[1]
                    if newSquare not in newValidMoves:
                        return invalid
    
    except IndexError:
        pass

    currentSquare = piece.location
    currentRow, currentCol = getBoardIndexFromRankAndFile(currentSquare)
    
    # if the pawn can capture en passant
    if isinstance(piece, Pawn) and piece.getEnPassantCaptureMoves()[0] != []:
        enPassantMoves = piece.getEnPassantCaptureMoves()[0]
        if newSquare not in enPassantMoves:
            return invalid
        
        enPassantCaptureSquares = piece.getEnPassantCaptureMoves()[1]
        
        # if the space is occupied:
        for cSqr in enPassantCaptureSquares:
            occupant = getPieceFromLocation(cSqr)
            
            if occupant != emptySquare:
                # call the capture function and print out the message
                message = capture(piece, occupant)
            else:
                message = ""
        
        return f"{str(piece)} {stringifyRankFile(currentSquare)} to {stringifyRankFile(newSquare)}. {message}"

    # non en-passant case:
    # getting location of move
    newRow, newCol = getBoardIndexFromRankAndFile(newSquare)
    newRank, newFile = getRankAndFileFromBoardIndex(newRow, newCol)
    
    # if the space is occupied by the opposite colour:
    occupant = getPieceFromLocation((newRank, newFile))
    
    if occupant != emptySquare:
        # call the capture function and print out the message
        message = capture(piece, occupant)
    else:
        message = ""
    
    # move piece from the current square
    BOARD[currentRow][currentCol] = emptySquare

    # to new square
    piece.location = (newRank, newFile)
    
    # pawn promotion
    pawnColourToPromotionRank = {
        "White": 8, 
        "Black": 1
        }
    if isinstance(piece, Pawn) and newRank == pawnColourToPromotionRank[piece.colour]:
        symbolOfNewPiece = input(f"{piece.colour}: Enter one of [Q, R, N, B] to promote the pawn: ")
        BOARD[newRow][newCol] = pawnPromotion(piece, symbolOfNewPiece)   
    
    else:
        BOARD[newRow][newCol] = piece

    # post-move conditions:
    # condition for en passant and first turn two-square forward move
    if isinstance(piece, Pawn) and piece.numMoves <= 2:
        piece.numMoves += 1

    # Conditions for not being allowed to castle:
    # if the rook moves 
    if isinstance(piece, Rook):
        piece.canCastle = False

    # print out the move 
    return f"{str(piece)} {stringifyRankFile(currentSquare)} to {stringifyRankFile(newSquare)}. {message}"


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
    if rank == boardLength:
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
        if occupant.colour == piece.colour and (not isinstance(piece, Knight)):
            return False
    
    return newSquare


# diagBL means the diagonal from top right to bottom left
# the function returns the diagBL adjacent square of the piece. returns 
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

# returns True if the king is in check by a piece
def kingIsInCheck(king: King, piece: Piece) -> bool:
    if piece.colour == king.colour:
        return False
    
    # if a piece can capture the king, return True
    if king.location in piece.getValidMoves():
        king.canCastle = False
        return True

    return False

# if the king is in check by any piece, return True
def kingIsInCheckGlobal(king: King) -> bool:
    opponentPlayer = colourToPlayer[oppositeColour(king.colour)]

    # looping over the opponent's pieces
    for piece in opponentPlayer.pieces:

        # if a piece can capture the king, return True
        if king.location in piece.getValidMoves():
            return True

    return False


# returns True if the square is defended by a piece 
# delete the piece on the square and see if the piece can go to that square
def squareDefended(square: tuple[str, int], piece: Piece) -> bool: 
    occupant = getPieceFromLocation(square)
    pieceMoves = piece.getValidMoves()
    
    if occupant == emptySquare:
        return square in pieceMoves
    
    # if a pawn defends the square, it needs to capture it 
    if isinstance(piece, Pawn):
        if occupant.colour == piece.colour:
            occupant.colour = oppositeColour(occupant.colour)
            pieceMoves = piece.getPawnCaptureMoves()
            result = square in pieceMoves
            occupant.colour = oppositeColour(occupant.colour)
            return result
        
        else:
            pieceMoves = piece.getPawnCaptureMoves()
            return square in pieceMoves 

    r, c = getBoardIndexFromRankAndFile(square)
    # removing the occupant from the board
    BOARD[r][c] = emptySquare
    # check if the square that was occupied is a valid move of the piece 
    pieceMoves = piece.getValidMoves()
    # replace the piece back to the board
    BOARD[r][c] = occupant

    return square in pieceMoves
    

# this function returns True if the king is in indirect check 
# (i.e. the king would be in check if moved to that square)
def kingIsInIndirectCheck(king: King, square: tuple[str, int]) -> bool:
    opponentPlayer = colourToPlayer[oppositeColour(king.colour)]
    
    for piece in opponentPlayer.pieces:
        if squareDefended(square, piece):
            return True

    return False


# if the king is in check, the check can be stopped if another piece blocks the path of the attacking piece
# moving the piece is valid only if the king is no longer in check after this other piece moves 
# need to check one move ahead.
def canBlockCheck(defendingPiece: Piece, attackingPiece: Piece, king: King) -> tuple[bool, list]:
    newValidMoves = []
    if not kingIsInCheck(king, attackingPiece):
        return (False, newValidMoves)
        
    originalDefenderLocation = defendingPiece.location
    attackerMoves = set(attackingPiece.getValidMoves())
    defenderMoves = set(defendingPiece.getValidMoves())
    intersectionMoves = attackerMoves.intersection(defenderMoves)
    
    for move in intersectionMoves:
        # moving the defending piece to the square that intersects
        currentR, currentC = getBoardIndexFromRankAndFile(originalDefenderLocation)
        BOARD[currentR][currentC] = emptySquare
        defendingPiece.location = move
        r, c = getBoardIndexFromRankAndFile(move)
        BOARD[r][c] = defendingPiece

        if not kingIsInCheck(king, attackingPiece):
            newValidMoves.append(move)
            # if the king is no longer in check, return the piece back to its original location
            newR, newC = getBoardIndexFromRankAndFile(move)
            BOARD[newR][newC] = emptySquare
            defendingPiece.location = originalDefenderLocation
            origR, origC = getBoardIndexFromRankAndFile(move)
            BOARD[origR][origC] = defendingPiece
            break
    
    # return the piece back to its original location
    newR, newC = getBoardIndexFromRankAndFile(move)
    BOARD[newR][newC] = emptySquare
    defendingPiece.location = originalDefenderLocation
    origR, origC = getBoardIndexFromRankAndFile(move)
    BOARD[origR][origC] = defendingPiece
    canBlock = True if newValidMoves != [] else False
    
    return (canBlock, newValidMoves)


# returns True if the king is in checkmate
def checkmate(king: King) -> bool:
    playerPieces = colourToPlayer[king.colour].pieces
    opponentPlayer = colourToPlayer[oppositeColour(king.colour)]
    opponentPieces = opponentPlayer.pieces

    if not kingIsInCheckGlobal(king):
        print("Gothere")
        return False
    
    # the for loop checks if every move is defended by the opponent 
    for move in king.getValidMoves():
        # filter for opponent pieces that defends the square that the king can move to 
        piecesIndirectlyThreateningTheKing = list(filter(lambda piece: squareDefended(move, piece), 
                                               opponentPieces))
        
        # if there are no pieces defending that square the king can move to
        if piecesIndirectlyThreateningTheKing == []:
            return False
        
        # getting the opponent pieces that aren't defending the square that the king can move to 
        piecesNotThreateningTheKing = [piece for piece in opponentPieces 
                                       if piece not in piecesIndirectlyThreateningTheKing]

        # if the king can capture a piece that threatens it and that piece is not defended
        for attackingPiece in piecesIndirectlyThreateningTheKing:
            for otherPiece in piecesNotThreateningTheKing:
                if attackingPiece.location == move and not squareDefended(attackingPiece.location, otherPiece):
                    return False

    # need to check:
                # if another piece can capture the attacking piece, and then the king is no longer in check 

    # if there's a move that can be blocked
    for piece in playerPieces:
        for opponPiece in opponentPieces:
            if canBlockCheck(piece, opponPiece, king)[0]:
                return False

    return True