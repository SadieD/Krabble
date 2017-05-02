import pygame, os, sys, string, re
import board, tiles, turn, validator, scoring, client
from copy import deepcopy
from pygame.locals import *
from board_objects import *
from time import sleep

#initialize
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((534,480))
pygame.display.set_caption('Krabble')
pygame.display.set_icon(square_start)

page_id = 0

dragging = False
crnt_tile = -1

''' define form controls and game objects '''
button_swap = Button('swap',(480,92))
button_pass = Button('pass',(480,119))
button_recall = Button('recall',(480,146))
button_send = Button('send',(480,173))
button_login = Button('login',(275,250))
button_offline = Button('offline',(335,250))
button_register = Button('register',(395,250))
button_play = Button('play',(241,221))
button_newgame = Button('new',(372,290))

button_swapMenu = Button('',(213,260))
button_swapMenu.visible = False

txtbx_user = Input(x=275,y=200,maxlength=20,
color=(0,0,0), prompt=' User: ',visible=True)
txtbx_pass = Input(x=275,y=225,maxlength=20,
color=(0,0,0), password=True, prompt=' Pass: ',visible=True)
txtbx_email = Input(x=275,y=175,maxlength=32,
color=(0,0,0), prompt='EMail: ')
txtbx_friend = Input(x=178,y=447,maxlength=20,
color=(0,0,0), prompt='Add Friend: ',visible=True)

lbl_login = Label_obj('Invalid username or password',(275,275),18,(255,0,0))

my_prompt = Prompt_box((182,190), "This is a test. BOOOOOP")

squares = []
rack = []

tiles_game = []
tiles_blank = []
tiles_swap = []

game_info = []
lbl_gamelist = []

def make_blankMenu():
    '''builds blank menu, sets tile positions'''
    offset_w, offset_h = 0, 0
    a_cnt = 0
    sec_row = True
    a = [chr(x) for x in xrange(ord('a'), ord('z')+1)]
    
    for i in range(4):
        offset_h += 32
        offset_w = 0
        sec_row ^= True
        if sec_row: offset_w += 16
        for j in range(7):
            tiles_blank.append(Tile_obj((155 + offset_w, 144 + offset_h),a[a_cnt]))
            a_cnt += 1
            offset_w += 32
            if sec_row and j == 5: break
            
def make_swapMenu():
    '''builds exchange menu, sets tile positions'''
    offset_w = 0
    for i in turn.plr_tiles[turn.current_player]:
        tiles_swap.append(Tile_obj((128 + offset_w, 217),i.lower()))
        offset_w += 32

def make_rack():
    '''builds rack, sets positions rack slots'''
    offset_h = 0
    for i in range(7):
        rack.append(Rack_slot((492,250 + offset_h)))
        offset_h += 32

def make_squares():
    '''builds game board, sets positions of squares'''
    d = board.read_board(board.SPECIAL_SQUARES)
    x, y = 0, -32
    for i in range(15):                            
        y += 32
        x = 0
        for j in range(15):
            if d[(j,i)] == '.': squares.append(Square_obj((x, y),square_blank))
            elif d[(j,i)] == 'W': squares.append(Square_obj((x, y),square_tw))
            elif d[(j,i)] == 'l': squares.append(Square_obj((x, y),square_dl))
            elif d[(j,i)] == 'w': squares.append(Square_obj((x, y),square_dw))
            elif d[(j,i)] == 'L': squares.append(Square_obj((x, y),square_tl))
            elif d[(j,i)] == 's': squares.append(Square_obj((x, y),square_start))
            squares[-1].coord = (j,i)
            x += 32
            
def make_text(text, text_pos, font_size, color):
    temp_font = pygame.font.Font(None, font_size)
    text_render = temp_font.render(str(text), 1, color)
    screen.blit(text_render, text_pos)
    
def make_gameInfo(player_data):
    del lbl_gamelist[:]
    del game_info[:]
    offset = 0
    bump = " " * 30
    print player_data
    
    if any(isinstance(el, list) for el in player_data) :
        for record in player_data :
            game_info.append(Game_info(record[0],record[1],record[2]))
            lbl_gamelist.append(Label_obj(str(record[0]) + bump + str(record[1]) + 
                                bump + str(record[2]),(130,55 + offset),18,(0,0,0),
                                clickable=True,link=record[0]))
            offset += 15
    else :
        game_info.append(Game_info(player_data[0],player_data[1],player_data[2]))
        lbl_gamelist.append(Label_obj(str(game_info[0].id) + bump + str(game_info[0].player_2) + 
                                bump + str(game_info[0].match),(130,55 + offset),18,(0,0,0),
                                clickable=True,link=game_info[0].id))

def make_game(game_pack = None, online=False) :
    if game_pack :
        print 'Cake!'
        # place_tiles(game_pack['board'])
        # turn.d = game_pack['board']
        
    elif online :
        tiles.initialize_bag()
        rack_tiles(turn.current_player)
    else:
        tiles.initialize_bag()
        rack_tiles(turn.current_player)
        print turn.d
    #else :
        # place_tiles()
    
''' page logic and drawing '''
    
def draw_game():
    screen.blit(background, (0,0))
    for i in squares : i.draw(screen)
    make_text('Player: ' + str(turn.current_player + 1), (488, 231), 14, (255,255,255))
    make_text('tiles remain:', (487, 67), 11, (255,255,255))
    make_text(len(tiles.main_bag), (502, 75), 12, (255,255,255))
    
    make_text(txtbx_user.value + ':', (485, 12), 14, (255,255,255))
    make_text(scoring.player_score[0], (485, 23), 14, (255,255,255))
    make_text('Player 2:', (485, 38), 14, (255,255,255))
    make_text(scoring.player_score[1], (485, 48), 14, (255,255,255))
    
    #Draw buttons
    button_pass.draw(screen)
    button_recall.draw(screen)
    button_send.draw(screen)
    button_swap.draw(screen)

    for i in tiles_game : i.draw(screen)
    
def draw_turn():
    '''offline turn mask'''
    global page_id
    screen.blit(switch_bg, (0,0))
    make_text('change players', (225,220), 35, (255,255,255))
    make_text('click anywhere to continue', (155,250), 35, (255,255,255))
    if event.type == MOUSEBUTTONDOWN: page_id = 1
    
def draw_blank():
    '''blank tile screen'''
    screen.blit(shaded, (0,0))
    make_text('choose a letter', (175,147), 35, (0,0,0))
    for i in tiles_blank : i.draw(screen)
    
def draw_swap():
    '''handles tile swaps'''
    global tiles_swap, page_id
    tiles_toSwap = []
    screen.blit(shaded, (0,0))
    screen.blit(rack_img, (112,222))
    for i in tiles_swap:
        screen.blit(i.image, i.rect)
        if i.mouseOver():
            if event.type == MOUSEBUTTONDOWN:
                sleep(.2)
                if i.rect.y == 210:
                    i.rect.y = 217
                    i.swap = False    
                else:
                    i.rect.y = 210
                    i.swap = True       
    if button_swapMenu.mouseOver():
        if event.type == MOUSEBUTTONDOWN:
            sleep(.3)
            for i in tiles_swap:
                if i.swap:
                    if i.ltr.islower(): i.ltr = '?'
                    tiles_toSwap.append(i.ltr)
                    for j in tiles_game:
                        if j.owner == turn.current_player and not j.locked and j.ltr == i.ltr:
                            tiles_game.remove(j)
                            break
            ''' if online game
                - client.game_move 
                - lock rack and board tiles
                - check server for new move
                    * update rack and unlock
                else: do offline stuff
            '''
            page_id = 4                            
            turn.update_tiles(turn.current_player, tiles_toSwap, True)
            rack_tiles(turn.current_player)
            turn.current_player = int(not turn.current_player)
            inviso_tiles()
            rack_tiles(turn.current_player)
            tiles_swap = []
            
def draw_login():
    screen.blit(switch_bg, (0,0))
    
    if txtbx_user.focus : txtbx_user.update(events)
    txtbx_user.draw(screen)

    if txtbx_pass.focus : txtbx_pass.update(events)
    txtbx_pass.draw(screen)   
    
    if txtbx_email.focus : txtbx_email.update(events)
    txtbx_email.draw(screen)   
    
    button_login.draw(screen)
    button_offline.draw(screen)
    button_register.draw(screen)
    
    lbl_login.draw(screen)
    
def draw_home():
    screen.blit(choose_bg, (0,0))
    
    #if txtbx_user.focus : txtbx_user.update(events)
    #txtbx_user.draw(screen)
    button_play.visible = True
    button_newgame.visible = True
    button_play.draw(screen)
    button_newgame.draw(screen)
    
    if txtbx_friend.focus : txtbx_friend.update(events)
    txtbx_friend.draw(screen)
    
    for i in lbl_gamelist :
        i.visible = True
        i.draw(screen)
        
def overBoard():
    '''Checks if we are over a specific square'''
    for i in squares: #check board
        if i.mouseOver() : return True
    return False
    
def overRack():
    '''Checks if we are over a specific rack slot'''
    for i in rack: #check rack
        if i.rect.collidepoint(pygame.mouse.get_pos()): return True
    return False
    
def overTile(group):
    '''Checks if we are over a specific tile'''
    for i in range(len(group)):
        if group[i].mouseOver(): return True
    return False
    
def mouseclickControl():
    '''Mouse over effect for buttons'''
    for buttonobj in Button : buttonobj.focus = False
    
    for buttonobj in Button:
        if buttonobj.mouseOver() : buttonobj.focus = True
    
def clickControl():
    '''control click event detection'''
    for txtbxobj in Input : txtbxobj.focus = False
    for lblObj in Label_obj : lblObj.focus = False
    
    ''' Handles button clicks'''
    for buttonobj in Button:
        if buttonobj.mouseOver() : buttonClick(buttonobj.name)
    
    for txtbxobj in Input:
        if txtbxobj.mouseOver() : txtbxobj.focus = True
    
    for lblObj in Label_obj:
        if lblObj.mouseOver() : lblObj.focus = True
    
def buttonClick(button):
    global page_id
    ''' Handles button events'''
    disableControls()
    sleep(.3) # debounce ^_^
    if button == 'send': #send move
        move = get_move()
        if turn.player_turn(move):
            ''' if online game
                - client.game_move 
                - lock rack and board tiles
                - check server for new move
                    * update rack and unlock
                else: do offline stuff
            '''
            page_id = 4
            turn.update_tiles(turn.current_player, move.values())
            lock_tiles()
            rack_tiles(turn.current_player)
            turn.current_player = int(not turn.current_player)
            inviso_tiles()
            rack_tiles(turn.current_player)
    elif button == 'pass': #pass
        ''' if online game
            - client.game_move 
            - lock rack and board tiles
            - check server for new move
                * update rack and unlock
            else: do offline stuff
        '''
        page_id = 4
        recallTiles()
        turn.current_player = int(not turn.current_player)
        inviso_tiles()
        rack_tiles(turn.current_player)
    elif button == 'recall': #recall
        recallTiles()
    elif button == 'swap': #swap
        recallTiles()
        make_swapMenu()
        page_id = 2
    elif button == 'new': #new online game
        if client.player_check(txtbx_friend.value) :
            if client.game_new(player.me,txtbx_friend.value) :
                make_game(1)
                page_id = 1
    elif button == 'register': #register user
        if txtbx_email.visible :
            if len(txtbx_user.value) > 4  and len(txtbx_pass.value) > 5 :
                if re.match(r'[\w.-]+@[\w.-]+', txtbx_email.value) :
                    if client.register(txtbx_user.value,txtbx_pass.value,txtbx_email.value) :
                        page_id = 5
                    else:
                        lbl_login.name = 'user name not available'
                        lbl_login.visible = True
                else:
                    lbl_login.name = 'please enter a valid email address'
                    lbl_login.visible = True
            else:
                lbl_login.name = 'username must be > 5 characters'
                lbl_login.visible = True
        else:
            txtbx_email.visible = True
    elif button == 'play': #continue online game
        print Label_obj.last_focus.link
        print client.fetch_game(Label_obj.last_focus.link)
        game_pack = client.fetch_game(Label_obj.last_focus.link)
        make_game(game_pack, 1)
        page_id = 1
    elif button == 'login': #login
        login = {
            'user':str(txtbx_user.value),
            'password':str(txtbx_pass.value),
        }
        player_data = client.login(login)
        if player_data <> False :
            make_gameInfo(player_data)
            page_id = 5
        else:
            lbl_login.name = 'invalid username or password'
            lbl_login.visible = True
    elif button == 'offline': #offline mode
        # list saved offline games and new offline game
        make_game(0)
        page_id = 1
        
def disableControls() :
    for buttonobj in Button :
        buttonobj.visible = False
        
def create_offset(drag_obj,mpos):
    '''Creates offset tuple to position tile appropriately for dragging
    args: drag_obj - object, mpos - mouse position'''
    return (mpos[0] - drag_obj.rect.x, mpos[1] - drag_obj.rect.y) 
    
def getTile(group):
    '''Returns tile last clicked'''
    for i in range(len(group)):
        if group[i].mouseOver(): return i
    return -1
                
def tileSnap(lst, tile):
    '''Aligns tile with board square or rack slot'''
    for n in range(len(lst)):
        for i in range(len(lst[n])):
            if lst[n][i].rect.collidepoint(pygame.mouse.get_pos()):
                if not lst[n][i].occupied:
                    tile.move((lst[n][i].rect.x,lst[n][i].rect.y),(0,0))
                    tile.last_position = (lst[n][i].rect.x,lst[n][i].rect.y)
                    isOccupied()
                    break
                else:
                    tile.move(tile.last_position,(0,0))
    
                
def rack_tiles(player):
    '''Get new tiles for player, then position tiles in the rack space
       args: player - integer representing current turn'''
    print 'Rack Tiles ' + str(player)
    c = 0
    openSlot = []
    isOccupied()
    for i in range(len(rack)):
        if not rack[i].occupied: openSlot.append(i)   
    print 'open rack slots: ', openSlot
    for i in turn.get_tiles(player):
        tiles_game.append(Tile_obj((rack[openSlot[c]].rect.x, 
                            rack[openSlot[c]].rect.y),i.lower()))
        tiles_game[-1].owner = player
        c += 1
        
    # do online stuff, since this seems to mark the end of a turn
    
def recallTiles():
    '''Moves unlocked tiles to the rack'''
    for i in squares:
        if i.occupied:
            for j in tiles_game:
                if i.rect.contains(j.rect) and not j.locked:       
                    for k in rack:
                        if not k.occupied:
                            j.rect.x = k.rect.x
                            j.rect.y = k.rect.y
                            isOccupied()    
    
def isOccupied():
    ''' Checks whether a slot on the board or rack is occupied for drag and drop purposes'''
    #check board
    for i in squares:
        i.occupied = False
        for j in range(len(tiles_game)):
            if i.rect.contains(tiles_game[j].rect):
                tiles_game[j].coord = i.coord
                i.occupied = True
                break
    #check rack
    for i in rack:
        i.occupied = False
        for j in range(len(tiles_game)):
            if i.rect.contains(tiles_game[j].rect) and tiles_game[j].visible:
                if tiles_game[j].blank:
                    tiles_game[j].image = tile_load['?']
                    tiles_game[j].ltr = '?'
                i.occupied = True
                break
                
def lock_tiles():
    '''Lock tiles on board, locked tiles cannot be moved or played'''
    for i in squares:
        if i.occupied:
            for j in tiles_game:
                if i.rect.contains(j.rect):
                    j.locked = True
                    scoring.locklist.append(j.coord)
                
def inviso_tiles():
    '''Switch visibility for current tiles in rack'''
    for i in rack:
        for j in tiles_game:
            if i.rect.contains(j.rect):
                j.visible ^= True
                
def get_move():
    '''Returns a dictionary with all tiles on the board that were placed 
       in the current move'''
    move = {}
    for i in squares:
        if i.occupied:
            for j in tiles_game:
                if i.rect.contains(j.rect) and not j.locked: move[i.coord] = j.ltr                    
    return move
 
draw_mode = {0 : draw_login,
                1 : draw_game,
                2 : draw_swap,
                3 : draw_blank,
                4 : draw_turn,
                5 : draw_home,
}
    
#build game board
make_squares()
make_rack()
make_blankMenu()

#Main loop
while True:
    
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT: os._exit(1)
    
    mouseclickControl()

    draw_mode[page_id]()
    
    my_prompt.draw(screen)
    
    if event.type == MOUSEBUTTONDOWN and clickControl() and not dragging : buttonClick()
    
    if page_id == 3: #draw blank menu, handle event
        if event.type == MOUSEBUTTONDOWN and overTile(tiles_blank):
            crnt_tile = getTile(tiles_blank)
            tiles_game[-1].ltr = tiles_blank[crnt_tile].ltr.lower()
            tiles_game[-1].image = tile_load[tiles_game[-1].ltr.lower()]
            page_id = 1
    elif page_id == 1: #normal game play
        if event.type == MOUSEBUTTONDOWN and overTile(tiles_game) and not dragging:
            crnt_tile = getTile(tiles_game)
            tiles_game.insert(len(tiles_game)-1,tiles_game.pop(crnt_tile))
            if not tiles_game[-1].locked and tiles_game[-1].visible:
                tiles_game[-1].dragged = True
                dragging = True
                offset = create_offset(tiles_game[-1],pygame.mouse.get_pos())
        elif event.type == MOUSEBUTTONUP and overBoard() and dragging:
            if tiles_game[-1].dragged: tileSnap([squares,rack],tiles_game[-1])
            tiles_game[-1].dragged = False
            dragging = False
            isOccupied()
            if tiles_game[-1].ltr == '?': page_id = 3
        elif event.type == MOUSEBUTTONUP and overRack():
            if tiles_game[-1].dragged: tileSnap([squares,rack],tiles_game[-1])
            tiles_game[-1].dragged = False
            dragging = False
            isOccupied()         
        elif event.type == MOUSEBUTTONUP and dragging:
            tiles_game[-1].move(tiles_game[-1].last_position,(0,0))
            tiles_game[-1].dragged = False
            dragging = False
            isOccupied()
            
        #Move tile if drag event
        if tiles_game[-1].dragged and dragging: 
            tiles_game[-1].move(pygame.mouse.get_pos(),offset) 
    
    pygame.display.flip() #update the screen