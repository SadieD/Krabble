import samples
from copy import deepcopy, copy

START_COORD = (7,7)
SIZE = (START_COORD[0] * 2) + 1  # board should be square

FILE_NAME = "word_list.txt" # Word list file name

used_words = []
new_words = []

def loadWordList(filename):
    # Modify to get list online or somehow lock access
    
    try :
        with open(filename, 'r') as f:
            text = f.read()
            text = text.rstrip()
            word_list = text.split()

    except IOError:
        print "invalid file"
        
    return word_list

def coord_in_bounds(coord):
    if coord[0] > START_COORD[0] * 2 or coord[1] > START_COORD[1] * 2:
        return False
    elif coord[0] < 0 or coord[1] < 0:
        return False
    return True

def valid_word_coords(d):
    ''' Returns a list of coordinates as tuples of all connected letters '''
    checked = set([])
    to_check = []
    valid = []   
    to_check.append(START_COORD)
    
    while len(to_check) > 0:
        coord = to_check[0]
        to_check.pop(0)
        
        if is_empty(d[coord]) or coord in checked:
            checked.update([coord])
            continue
        valid.append(coord)
        
        surround = [(coord[0], coord[1] - 1), (coord[0], coord[1] + 1), (coord[0] - 1, coord[1]), (coord[0] + 1, coord[1])]
        
        for i in surround:
            if not coord_in_bounds(i):
                continue
            if i not in checked:
                to_check.append(i)
                   
        checked.update([coord])
    return valid
    

def is_empty(s):
    return s == "."

def has_floating_words(d):
    valid = valid_word_coords(d)
    for coord in d:
        if is_empty(d[coord]):
            continue
        if coord not in valid:
            return True
    return False
        
def getLines(dir, d):
    ''' Returns a list of words from a board
        dir = direction to scan, 0 for vertical, 1 for horizontal
        d = board dictionary
    '''
    word_data = []
    # Check for single letter at start square
    if not is_empty(d[(7,7)]):
        if is_empty(d[(6,7)]) and is_empty(d[(8,7)]) and is_empty(d[(7,6)]) and is_empty(d[(7,8)]):
            return d[(7,7)]
    
    for cnt1 in range(SIZE):
        word_c = []
        for cnt2 in range(SIZE):
            #Flips scanning values based on arg d
            if dir == 0 : i, j, v, h = cnt1, cnt2, 0, 1
            else: i, j, v, h = cnt2, cnt1, 1, 0
            if cnt2 == 0:
                if d[(i,j)].isalpha() and d[(i + v,j + h)].isalpha():
                    word_c.append((d[(i,j)],(i,j)))
            elif cnt2 < 14:
                if d[(i,j)].isalpha() and d[(i + v,j + h)].isalpha():
                    word_c.append((d[(i,j)],(i,j)))
                elif d[(i,j)].isalpha() and d[(i - v,j - h)].isalpha():
                    word_c.append((d[(i,j)],(i,j)))
                    word_data.append(word_c)
                    word_c = [] # In case there's more than one word in a line ;)
            elif cnt2 == 14:
                if d[(i,j)].isalpha() and d[(i - v,j - h)].isalpha():
                    word_c.append((d[(i,j)],(i,j)))
                    word_data.append(word_c)
    return word_data

def has_invalid_words(d, word_list):
    '''checks if board contains invalid words, logs words played'''
    word_data = []
    strings = ''
    invalid_words = ''

    word_data.extend(getLines(0, d))
    word_data.extend(getLines(1, d))
    
    for i in word_data:
        if strings <> '':
            if strings not in word_list: invalid_words += strings + " "
        strings = ''
        for j in i:
            strings += j[0].upper()
    if strings not in word_list: invalid_words += strings + " " 
    if len(invalid_words) <> 0: return True
    return False

def validate(d):
    ''' Returns True if the board is a valid Scrabble state, False if not.

        The d parameter is a dictionary whose keys are (column, row) tuples
        and whose values are a string letter.
    '''
    if not has_floating_words(d):
        if not has_invalid_words(d, loadWordList(FILE_NAME)): return True
    return False
    
def validate_move(d, move):
    if move_contains_zero_letters(move) or move_not_in_bounds(move) : return False
    if move_length_invalid(move) : return False
    if move_is_on_top_of_existing_letters(d, move) : return False
    
    if move_is_all_in_one_row(move):
        if not move_is_contiguous(d, move, 1) : return False
    elif move_is_all_in_one_col(move):
        if not move_is_contiguous(d, move, 0) : return False
    else: return False
    
    if board_is_invalid_after_move(d, move) : return False
    
    commit_move(d, move)
    log_words(d)
    return True
    
def log_words(d):
    global used_words, new_words
    new_words = []
    
    new_words.extend(getLines(0, d))
    new_words.extend(getLines(1, d))
    
    for i in used_words:
        if i in new_words: new_words.remove(i)
    used_words.extend(new_words)

def commit_move(d, move):
    ''' This function takes a board d and modifies it by applying the given
        move to it.  For example, if a move contains {(3, 3): 'Q'}, then after
        this function call, d[(3, 3)] should be 'Q'.  d should still contain
        everything that it previously contained prior to this function.

        The move variable should *not* be modified as a part of this function.

        Parameters:
            d and move are of the same types specified in the validate_move
            function.

        Returns: d
    '''
    for i in move.iterkeys():
        d[i] = move[i]
    # print board.stringify_board(d)
    return d

def board_is_invalid_after_move(d, move):
    ''' Returns True if the board d is valid after applying move to it.
        Does not modify either d or move directly.  Instead it copies
        d, applies the move to that copy, and validates that copy.
    '''
    temp_d = create_temp_board(d, move)
    for i in move.iterkeys():
        temp_d[i] = move[i]
        
    if validate(temp_d): return False
    
    return True

def create_temp_board(d, move):
    temp_d = deepcopy(d)
    for i in move.iterkeys():
        temp_d[i] = move[i]
    return temp_d

def move_contains_zero_letters(move):
    ''' Returns True if move has zero letters in it, False otherwise '''
    if len(move) == 0 : return True
    for i in move.itervalues():
        if i == '' : return True
    return False
    
def move_length_invalid(move):
    ''' Returns True if move has zero letters in it, False otherwise '''
    temp = [x for x in move.iterkeys()]
    if len(temp) < 0 or len(temp) > 7 : return True
    return False

def move_is_on_top_of_existing_letters(d, move):
    ''' Returns True if any letter in move would be placed on top of
        an existing letter in board d, i.e. d[(3, 4)] == 'Q' and
        move[(3, 4)] == 'X'.  Returns False otherwise.
    '''
    for i in move.iterkeys():
        if not is_empty(d[i]) : return True
    return False
    
def move_not_in_bounds(move):
    for i in move.iterkeys():
        if not coord_in_bounds(i) : return True
    return False

def move_is_all_in_one_col(move):
    ''' Returns True if all letters in move are in the same row. '''
    c = -1
    for x,y in move.iterkeys():
        if c < 0 : c = x
        if x <> c : return False
        c = x
    return True
    
def move_is_all_in_one_row(move):
    ''' Returns True if all letters in move are in the same col. '''
    c = -1
    for x,y in move.iterkeys():
        if c < 0 : c = y
        if y <> c : return False
        c = y
    return True
    
def move_is_contiguous(d, move, dir):
    '''Returns True if move is contiguous
    
        Parameters:
            d and move are dictionaries composed of coordinates in tuple form with a letter as
            a value. dir is an integer 0 or 1, determines the direction to check the board.
    '''
    
    temp_d = create_temp_board(d, move)
    
    temp = [x for x in move.iterkeys()]
    if dir == 0:
        temp = sorted(temp, key=lambda x: x[1])
        word_len = temp[-1][1] - temp[0][1]
    elif dir == 1:
        temp = sorted(temp, key=lambda x: x[0])
        word_len = temp[-1][0] - temp[0][0]
    s_coord = temp[0]
    for i in range(word_len + 1):
        if dir == 0:
            if is_empty(temp_d[(s_coord[0],s_coord[1]+i)] ): return False
        elif dir == 1:
            if is_empty(temp_d[(s_coord[0]+i,s_coord[1])] ): return False
    return True
