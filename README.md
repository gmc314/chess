# Full Stack Chess

# Summary
Local 2-player chess featuring back and front ends

# Plan:
## Back-end:
### Pieces and Board 
The board is an 8x8 list of lists.

#### Pieces Overview
King
  - Check and Checkmate conditions 
    - Direct check 
    The king would be captured if not moved from its current location  
    - Indirect check
    If the king moves to the square, it would be captured next turn
  - Can move one square in all directions
  - Can castle with rook

Queen
  - Can move horizontally, vertically, and diagonally
  - Can move any number of squares in the above directions

Bishop
  - Can move diagonally
  - Can move any number of squares

Knight 
  - Can move in an L-shape (2 squres in a vertical or horizonal direction, and 1 square in the other direction)
  - Can jump over pieces

Rook 
  - Can move veritically or horizontally
  - Can move any number of squares 
  - Can castle with king

Pawn
  - Can only move forward depending on colour
  - On the first turn, can move two squares forward or one sqaure 
  - Captures pieces diagonally 
  - Can capture en passant 

Pieces are classes with properties:
  1. Colour 
  2. Type
  3. Location
  4. ID
  5. Points
  6. canCastle

Class Methods for all pieces:
  1. `moveFromCurrentSquare(self, squre)`
  2. `isThreatened(self)`
  3. `isMoveValid(self, square)`
  4. `getAllValidMoves(self, square)`
  5. `getCurrentSquare(self)`

#### Coding Details
  - Orientation of the board will be in the usual chess standard. 
  - Rank and file will be standard.
  - Colour of the pawn determines valid move direction.
  - What is a valid move? 
    - Determined by type, path, and obstructions 
  - Castling conditions:
    1. King and rook are in their starting positions
    2. No pieces in the way 
    3. - Short castle: non-queen side castling 
       - Long castle: queen side castling   
  - Capturing conditions:
    1. Piece of opposite colour is in the valid path of a piece 
    2. Pawn begins with a 2-square move for en passant
  - Pawn promotion conditions:
    1. Pawn reaches the opposite end of the board 
    2. On the same turn, change to one of: queen, rook, knight, bishop

## Server-side:
Login 
Saving game state
Logging moves

## Front-end:
Login screen
Mouse drags pieces
Board rotates on each player's turn?
Initial board condition
Undo button?
Stalemate button> 