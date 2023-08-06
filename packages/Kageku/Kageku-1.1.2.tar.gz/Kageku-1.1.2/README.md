# Kageku

## What "Kageku" is?
"Kageku" is a game created in one night to be one of the side games me and my friends can play inside our RPG to obtain resources inside it if we play well.

This game is played with a chess board and pieces and works just like chess, but with some key differences.

### Board
The board starts with a different configuration (as shown below)

. | a  | b | c | d | e | f | g | h
-- |-- |-- |-- |-- |-- |-- |-- |--
**8**|k|-|r|-|-|-|-|-
**7**|p|p|p|-|-|-|-|-
**6**|-|-|-|-|-|-|-|-
**5**|-|-|-|-|-|-|-|-
**4**|-|-|-|-|-|-|-|-
**3**|-|-|-|-|-|-|-|-
**2**|-|-|-|-|-|P|P|P
**1**|-|-|-|-|-|R|-|K

### Winning
To win, you must either take your opponent's king (yes, no checkmate) or promote a pawn.

The ideia behind not having the obligation to checkmate to win is both to be more simple to people who aren't used to playing chess and potentially speeding up the games.

### "Mana"
In the game we have a system that resembles a mana system that caps your plays in your turn. The use of it is stated below.

To calculate how much mana do you have at any given point, you will count the number of friendly pawns you have at your opponent side of the field and add one if you have a friendly pawn in your side of the field.

### Spawning pieces
This is the use of the mana. Each turn you can summon any amount of pieces you want as long as the combined cost of all of them is less than or equal to your mana. Pieces that can spawn other pieces references to all pieces in which you can spawn other pieces in empty squares adjacent to them (only up, down, left and right are considered adjacent). To know if a piece can spawn other pieces, you will check if this piece is adjacent to another piece that is able to spawn pieces. The king is always a piece that can spawn others.

The table of pieces costs is the following (for now)

Pawn | Knight  | Bishop | Rook | Queen
-- |-- |-- |-- |--
1|2|3|4|5

You cannot have more than 8 pawns, 2 knights, 2 bishops, 2 rooks and 1 queen.

### Other details
- You cannot move the pawns two squares up in the first move like you do in chess

## Installation

To install this package you can use ```pip``` like:

```pip install kageku```

## Requirements

You'll need Python to run this project (I'm using Python 3.6.8, I don't know if everything works in a different version). No special package is required!

To run the [welcome program](https://github.com/lucaspellegrinelli/kageku-ai/blob/master/welcome.py) you'll need to run this command

> python welcome.py
