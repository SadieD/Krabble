import tiles, validator, board, scoring
import string

plr_tiles = {0: [],1: []}
current_player = 0
d = board.get_board()

def get_tiles(player):
    '''refills player rack with new tiles from the bag'''
    global plr_tiles
    new_tiles = tiles.dist_tiles(plr_tiles[player])
    plr_tiles[player].extend(new_tiles)
    print plr_tiles[player]
    return new_tiles
    
def update_tiles(player, rem_tiles, exchange=False):
    '''removes used tiles from player rack'''
    global plr_tiles
    print 'update tiles'
    print plr_tiles[player]
    print rem_tiles
    for i in rem_tiles :
        if i.islower(): i = '?'
        if i in plr_tiles[player]:
            plr_tiles[player].remove(i)
    if exchange:
        tiles.exchange_tiles(rem_tiles)
    print 'Result'
    print plr_tiles[player]

def player_turn(move):
    '''turn logic goes here'''
    global plr_tiles, d, current_player
    bingo = False
    
    if validator.validate_move(d,move):
        if len(move) == 7: bingo = True
        scoring.tally(current_player, bingo)
        return True
    return False