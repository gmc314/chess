from pprint import pprint
from script import *
import os

def clear():
    os.system("cls")

def newGame():
    clearBoard()
    # get new instances of all pieces
    bk = King("Black", "1", ('e', 8))
    placePiece(bk)
    bq = Queen("Black", "2", ('d', 8))
    placePiece(bq)
    bb1 = Bishop("Black", "3", ('c', 8))
    placePiece(bb1)
    bb2 = Bishop("Black", "4", ('f', 8))
    placePiece(bb2)
    bn1 = Knight("Black", "5", ('b', 8))
    placePiece(bn1)
    bn2 = Knight("Black", "6", ('g', 8))
    placePiece(bn2)
    br1 = Rook("Black", "7", ('a', 8))
    placePiece(br1)
    br2 = Rook("Black", "8", ('h', 8))
    placePiece(br2)
    bp1 = Pawn("Black", "9", ('a', 7))
    placePiece(bp1)
    bp2 = Pawn("Black", "10", ('b', 7))
    placePiece(bp2)
    bp3 = Pawn("Black", "11", ('c', 7))
    placePiece(bp3)
    bp4 = Pawn("Black", "12", ('d', 7))
    placePiece(bp4)
    bp5 = Pawn("Black", "13", ('e', 7))
    placePiece(bp5)
    bp6 = Pawn("Black", "14", ('f', 7))
    placePiece(bp6)
    bp7 = Pawn("Black", "15", ('g', 7))
    placePiece(bp7)
    bp8 = Pawn("Black", "16", ('h', 7))
    placePiece(bp8)

    wk = King("White", "17", ('e', 1))
    placePiece(wk)
    wq = Queen("White", "18", ('d', 1))
    placePiece(wq)
    wb1 = Bishop("White", "19", ('c', 1))
    placePiece(wb1)
    wb2 = Bishop("White", "20", ('f', 1))
    placePiece(wb2)
    wn1 = Knight("White", "21", ('b', 1))
    placePiece(wn1)
    wn2 = Knight("White", "22", ('g', 1))
    placePiece(wn2)
    wr1 = Rook("White", "23", ('a', 1))
    placePiece(wr1)
    wr2 = Rook("White", "24", ('h', 1))
    placePiece(wr2)
    wp1 = Pawn("White", "25", ('a', 2))
    placePiece(wp1)
    wp2 = Pawn("White", "26", ('b', 2))
    placePiece(wp2)
    wp3 = Pawn("White", "27", ('c', 2))
    placePiece(wp3)
    wp4 = Pawn("White", "28", ('d', 2))
    placePiece(wp4)
    wp5 = Pawn("White", "29", ('e', 2))
    placePiece(wp5)
    wp6 = Pawn("White", "30", ('f', 2))
    placePiece(wp6)
    wp7 = Pawn("White", "31", ('g', 2))
    placePiece(wp7)
    wp8 = Pawn("White", "32", ('h', 2))
    placePiece(wp8)
    return "Board ready"



# this function converts the 2 character typed move to a tuple 
def squareToTuple(squareString: str):
    file, rank = list(squareString)
    return (file.lower(), int(rank))

# gets the piece and square from playerInput
def extractMoveElements(player: Player, playerInput: str):
    pieceSymbol, currentSquare, destinationSquare = playerInput.split(' ')
    
    symbolToClass = {
        "K": King,
        "Q": Queen,
        "N": Knight, 
        "B": Bishop,
        "R": Rook,
        "P": Pawn
        }
    
    piece = [p for p in player.pieces if isinstance(p, symbolToClass[pieceSymbol]) and 
             p.location == squareToTuple(currentSquare)][0]
    
    return (piece, squareToTuple(destinationSquare))

# plan for the main playGame function
def playGame():
    newGame()
    print("####################################")
    print("##                                ##")
    print("##                                ##")
    print("##    Welcome to Python Chess!    ##")
    print("##                                ##")
    print("##                                ##")
    print("####################################\n")
    
    pprint(BOARD)

    whiteKing = [piece for piece in WHITE.pieces if isinstance(piece, King)][0]
    blackKing = [piece for piece in BLACK.pieces if isinstance(piece, King)][0]
    numRounds = 0
    
    while True:
        # White turn  
        if checkmate(whiteKing):
            gameOverMessage = "Black wins"
            break
        
        whiteMoveText = input("White: Enter [symbol] [currentSquare] [newSquare]: ")
        if whiteMoveText == "q":
            print("Quit")
            return
        
        whiteMoveInput = extractMoveElements(WHITE, whiteMoveText)
        print(whiteMoveInput)
        whiteMove = moveFromCurrentSquare(*whiteMoveInput)
        
        while whiteMove == "invalid move":
            print(whiteMove)
            whiteMoveText = input("White: Enter [symbol] [currentSquare] [newSquare]: ")
            whiteMoveInput = extractMoveElements(WHITE, whiteMoveText)
            whiteMove = moveFromCurrentSquare(*whiteMoveInput)
        clear()
        pprint(BOARD)
        
        # Black turn 
        if checkmate(blackKing):
            gameOverMessage = "White wins"
            break

        blackMoveText = input("Black: Enter [symbol] [currentSquare] [newSquare]: ")
        if blackMoveText == "q":
            print("Quit")
            return

        blackMoveInput = extractMoveElements(BLACK, blackMoveText)
        blackMove = moveFromCurrentSquare(*blackMoveInput)
        
        while blackMove == "invalid move":
            print(blackMove)
            blackMoveText = input("Black: Enter [symbol] [currentSquare] [newSquare]: ")
            blackMoveInput = extractMoveElements(BLACK, blackMoveText)
            blackMove = moveFromCurrentSquare(*blackMoveInput)
        clear()
        pprint(BOARD)
        
        numRounds += 1

        # condition for stalemate
        if numRounds > 100:
            gameOverMessage = "Stalemate"
            break

    print(gameOverMessage)
    return


playGame()