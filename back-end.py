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
    def __init__(self, color: str, name: str, id, location: tuple, isThreatened: bool) -> None:
        self.id = id
        self.color = color 
        self.name = name
        self.location = location
        self.isThreatened = isThreatened