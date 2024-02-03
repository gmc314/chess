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

    @classmethod
    def isMoveValid(self, newSquare):
        return True


class Queen(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Queen", ID, location, False, 9) 
   
    @classmethod
    def isMoveValid(self, newSquare):
        return True
    

class Rook(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Rook", ID, location, True, 5)

    @classmethod
    def isMoveValid(self, newSquare):
        return True
        

class Bishop(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Bishop", ID, location, False, 3) 
    
    @classmethod
    def isMoveValid(self, newSquare):
        return True
        

class Knight(Piece):
    def __init__(self, color, ID, location):
        super().__init__(color, "Knight", ID, location, False, 3) 
    
    @classmethod
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