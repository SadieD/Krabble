import random, string, copy

NEW_BAG = {'A':9,'B':2,'C':2,'D':4,'E':12,'F':2,'G':3,'H':2,'I':9,'J':1,'K':1, \
            'L':4,'M':2,'N':6,'O':8,'P':2,'Q':1,'R':6,'S':4,'T':6,'U':4,'V':2, \
            'W':2,'X':1,'Y':2,'Z':1,'?':2}
            
main_bag = []

def initialize_bag(new_game=True, bag = NEW_BAG):
    # Takes dictionary of letters and quantity, returns scrambled list of letters
    if new_game:
        temp = bag.items()
        str_bag = ""
        for i in temp:
            str_bag += i[0] * i[1]
        main_bag.extend(shuffle_bag(str_bag))
    
def shuffle_bag(bag):
    bag = random.sample(bag, len(bag))
    return bag
    
def random_tile(bag):
    tile = random.choice(bag)
    return tile
    
def dec_tile(tile):
    main_bag.remove(tile)
    return bag
    
def dist_tiles(player_tiles):
    # Give the player tiles until they have seven
    # player_tiles = list of letters, up to 7 items
    tile = ""
    temp_tiles = copy.deepcopy(player_tiles)
    new_tiles = []
    while len(temp_tiles) < 7:
        if len(main_bag) == 0 : break #Do something, we're out of tiles!
        tile = random_tile(main_bag)
        temp_tiles.append(tile)
        new_tiles.append(tile)
        main_bag.remove(tile)
    return new_tiles
    
def exchange_tiles(player_tiles):
    main_bag.extend(player_tiles)
    shuffle_bag(main_bag)
    