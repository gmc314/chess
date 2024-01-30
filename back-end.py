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

class Piece:
    def __init__(self, color: str, name: str, id: str, location: tuple, canCastle: bool, points: int) -> None:
        self.id = id
        self.color = color 
        self.name = name
        self.location = location
        self.canCastle = False
        self.points = points

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

