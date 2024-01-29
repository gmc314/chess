# Full Stack Chess

# Summary
Local 2-player chess featuring back and front ends

# Plan:
## Back-end:
### Pieces and Board 
The board is an 8x8 list of lists.

Pieces are classes with properties:
  1. Colour 
  2. Type
  3. Location
  4. ID
  5. Points

#### Pieces Overview
King
  - Check and Checkmate conditions 
    - Direct check 
    The king would be captured if not moved from its current location  
    - Indirect check
    If the king moves to the square, it would be captured next turn
  - Can move one square in all directions

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

Pawn
  - Can only move forward depending on colour
  - On the first turn, can move two squares forward or one sqaure 
  - Captures pieces diagonally 
  - Can capture en passant 

#### Coding Details
  - Orientation of the board 
  - Colour of the pawn determines valid move direction
  - What is a valid move? 
  - Castling conditions
  - Capturing
  - Pawn promotion

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