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
    def __init__(self, color: str, name: str, id: str, location: tuple, canCastle: bool, points: int) -> None:
        self.id = id
        self.color = color 
        self.name = name
        self.location = location
        self.canCastle = False
        self.points = points

    # move piece from current square to new `square`
    @classmethod
    def moveFromCurrentSquare(self, square: tuple):
        currentSquare = self.location
        currentFile = currentSquare[0]
        currentRank = currentSquare[1]
        newSquare = (square[0], square[1])
        if not self.isMoveValid(newSquare):
            return "invalid move"
        
        currentCol = int(currentRank) - 1
        currentRow = fileIndex[currentFile]
        


    @classmethod
    def isThreatened(self):
        pass
    
    @classmethod
    def isMoveValid(self, square):
        pass

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
    def __init__(self, color: str, id, location: tuple) -> None:
        self.id = id
        self.color = color 
        self.name = "King"
        self.location = location
        self.canCastle = True
        self.points = 0

class Queen(Piece):
    def __init__(self, color: str, id, location: tuple) -> None:
        self.id = id
        self.color = color 
        self.name = "Queen"
        self.location = location
        self.points = 9

class Rook(Piece):
    def __init__(self, color: str, id, location: tuple) -> None:
        self.id = id
        self.color = color 
        self.name = "Rook"
        self.location = location
        self.canCastle = True
        self.points = 5

class Bishop(Piece):
    def __init__(self, color: str, id, location: tuple) -> None:
        self.id = id
        self.color = color 
        self.name = "Bishop"
        self.location = location
        self.canCastle = True
        self.points = 3

class Knight(Piece):
    def __init__(self, color: str, id, location: tuple) -> None:
        self.id = id
        self.color = color 
        self.name = "Knight"
        self.location = location
        self.canCastle = True
        self.points = 3

class Pawn(Piece):
    def __init__(self, color: str, id, location: tuple) -> None:
        self.id = id
        self.color = color 
        self.name = "Pawn"
        self.location = location
        self.canCastle = True
        self.points = 1

