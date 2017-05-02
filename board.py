import validator
import math

SPECIAL_SQUARES = """\
W..l...W...l..W
.w...L...L...w.
..w...l.l...w..
l..w...l...w..l
....w.....w....
.L...L...L...L.
..l...l.l...l..
W..l...s...l..W
..l...l.l...l..
.L...L...L...L.
....w.....w....
l..w...l...w..l
..w...l.l...w..
.w...L...L...w.
W..l...W...l..W"""

BOARD_EMPTY = """\
...............
...............
...............
...............
...............
...............
...............
...............
...............
...............
...............
...............
...............
...............
..............."""

MAIN_BOARD = BOARD_EMPTY

SIZE = 0

def read_board(str_board):
    '''Takes in a string in the form of a grid of letters
        Returns a board in the format described below.
        #  keys: coodinates tuple (column, row) where row and column are integers
        #  values: a letter'''
    board = {}
    lines = str_board.splitlines()
    for row, y in zip(lines, range(len(lines))):
        for col, x in zip(row, range(len(row))):
            key = (x, y)
            board[key] = col
    return board
    
def commit_board(board):
    global MAIN_BOARD
    MAIN_BOARD = stringify_board(board)
    pass
    
def get_board():
    global MAIN_BOARD
    board = read_board(MAIN_BOARD)
    return board

def stringify_board(board):
    '''Takes a board in dictionary format and returns a
       string in grid format'''
    result = ""
    SIZE = int(math.sqrt(len((board))))
    for row in range(SIZE):
        if row > 0:
            result += "\n"
        for col in range(SIZE):
            result += board[(col, row)]
            
    return result