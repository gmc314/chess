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
    row = int(rank) - 1
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

    # move piece from current square to new `square`
    @classmethod
    def moveFromCurrentSquare(self, newSquare: tuple):
        if not self.isMoveValid(newSquare):
            return "invalid move"
        
        # getting current location of piece
        currentSquare = self.location 
        currentRow, currentCol = getBoardIndexFromRankAndFile(currentSquare)
 
        # getting location of move
        newRow, newCol = getBoardIndexFromRankAndFile(newSquare)
        newRank, newFile = getRankAndFileFromBoardIndex((newRow, newCol))

        # move piece from the current square

        # from current 
        BOARD[currentRow][currentCol] = None

        # to new
        self.location = (newFile, newRank)

        BOARD[newRow][newCol] = self
        # print out the move 
        return f"{self.name} {stringifyRankFile(currentSquare)} to {stringifyRankFile(newSquare)}"


    @classmethod
    def isThreatened(self):
        pass
    
    @classmethod
    def isMoveValid(self, square):
        return True

    @classmethod
    def getAllValidMoves(self):
        pass
    
    @classmethod
    def getCurrentSquare(self):
        pass

    @classmethod
    def castle(self):
        pass

# inheriting from Piece class
class King(Piece):
    def __init__(self, color, name,ID, location, canCastle, points):
        super().__init__(self, color, name, ID, location, canCastle, points)
        self.name = "King" 
        self.canCastle = True
        self.points = 0

class Queen(Piece):
    def __init__(self, color, name, ID, location, canCastle, points):
        super().__init__(self, color, name, ID, location, canCastle, points) 
        self.name = "Queen"
        self.points = 9

class Rook(Piece):
    def __init__(self, color, name, ID, location, canCastle, points):
        super().__init__(color, name, ID, location, canCastle, points) 
        self.name = "Rook"
        self.canCastle = True
        self.points = 5

class Bishop(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Bishop", ID, location, False, 3) 
        self.ID = ID
        self.location = location
        self.color = color
        


class Knight(Piece):
    def __init__(self, color, name, ID, location, canCastle, points):
        super().__init__(self, color, name, ID, location, canCastle, points) 
        self.name = "Knight"
        self.points = 3

class Pawn(Piece):
    def __init__(self, color, name, ID, location, canCastle, points):
        super().__init__(self, color, name, ID, location, canCastle, points) 
        self.name = "Pawn"
        self.points = 1


def placePiece(piece: Piece):
    currentSquare = piece.location
    row, col = getBoardIndexFromRankAndFile(currentSquare)
    BOARD[row][col] = piece
    return f"{piece} placed"