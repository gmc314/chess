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
def getBoardIndexFromRankAndFile(square: tuple):
    file, rank = square
    col = fileIndex[file]
    row = 8 - int(rank)
    return (row, col)


# gets the rank and file from indices of the Board
def getRankAndFileFromBoardIndex(indices: tuple):
    row, col = indices
    file = list(fileIndex.keys())[list(fileIndex.values()).index(col)]
    rank = row + 1
    return (file, rank)


# convert rank and file tuple to string
def stringifyRankFile(square: tuple):
    return f"{square[0]}{square[1]}"


class Piece:
    def __init__(self, color: str, name: str, ID: str, location: tuple, canCastle: bool, points: int):
        self.ID = ID
        self.color = color 
        self.name = name
        self.location = location
        self.canCastle = canCastle
        self.points = points

    def __repr__(self) -> str:
        return f"{self.color} {self.name}"


    @classmethod
    def castle(self):
        pass


# inheriting from Piece class
class King(Piece):    
    def __init__(self, color, ID, location):
        super().__init__(color, "King", ID, location, True, 0) 
        self.ID = ID
        self.location = location
        self.color = color

    @classmethod
    def isMoveValid(self, newSquare):
        return True


class Queen(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Queen", ID, location, False, 9) 
        self.ID = ID
        self.location = location
        self.color = color
   
    @classmethod
    def isMoveValid(self, newSquare):
        return True
    

class Rook(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Rook", ID, location, True, 5) 
        self.ID = ID
        self.location = location
        self.color = color

    @classmethod
    def isMoveValid(self, newSquare):
        return True
        

class Bishop(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Bishop", ID, location, False, 3) 
        self.ID = ID
        #self.location = location
        self.color = color

    @classmethod
    def isMoveValid(self, newSquare):
        if newSquare != None:
            return True
        


class Knight(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Knight", ID, location, False, 3) 
        self.ID = ID
        self.location = location
        self.color = color
    
    @classmethod
    def isMoveValid(self, newSquare):
        return True    

class Pawn(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Pawn", ID, location, False, 1) 
        self.ID = ID
        self.location = location
        self.color = color
        
    @classmethod
    def isMoveValid(self, newSquare):
        return True


# place a piece on the board at its initial square
def placePiece(piece: Piece):
    currentSquare = piece.location
    row, col = getBoardIndexFromRankAndFile(currentSquare)
    BOARD[row][col] = piece
    return f"{piece} placed"


# move piece from current square to new `square`
def moveFromCurrentSquare(piece: Piece, newSquare: tuple):
    if not piece.isMoveValid(newSquare):
        return "invalid move"
    
    # getting current location of piece
    currentSquare = piece.location
    currentRow, currentCol = getBoardIndexFromRankAndFile(currentSquare)

    # getting location of move
    newRow, newCol = getBoardIndexFromRankAndFile(newSquare)
    newRank, newFile = getRankAndFileFromBoardIndex((newRow, newCol))

    # move piece from the current square

    # from current 
    BOARD[currentRow][currentCol] = None

    # to new
    piece.location = (newFile, newRank)

    BOARD[newRow][newCol] = piece
    # print out the move 
    return f"{piece.name} {stringifyRankFile(currentSquare)} to {stringifyRankFile(newSquare)}"

