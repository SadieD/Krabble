import board, validator
locklist = []
player_score = [0,0]

TILE_VALUES = {'A':1,'B':3,'C':3,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,'J':8,'K':5, \
            'L':1,'M':3,'N':1,'O':1,'P':3,'Q':10,'R':1,'S':1,'T':1,'U':1,'V':4, \
            'W':4,'X':8,'Y':4,'Z':10,'?':0}
            
BONUS = {'W':3,'w':2,'s':2,'L':3,'l':2,'.':1}            
            
SQUARE = board.read_board(board.SPECIAL_SQUARES)
            
def tally(player, bingo = False):
    global locklist, player_score
    score  = 0
    word_score = 0
    word_bonus = 0
    words = validator.new_words
    dw, tw = 0, 0 
    for i in words:
        if word_bonus > 0 : word_score *= word_bonus
        score += word_score
        for j in i:
            if j[0].isupper():
                bonus = 1
                if SQUARE[j[1]] == 'L' or SQUARE[j[1]] == 'l':
                    if j[1] not in locklist : bonus = BONUS[SQUARE[j[1]]]
                if SQUARE[j[1]] == 'W' or SQUARE[j[1]] == 'w' or SQUARE[j[1]] == 's':
                    if j[1] not in locklist : word_bonus += BONUS[SQUARE[j[1]]]
                word_score += (TILE_VALUES[j[0]] * bonus)
    if word_bonus > 0 : word_score *= word_bonus
    score += word_score
    if bingo: score += 50
    player_score[player] += score
    return player_score[player]