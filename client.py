import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://cnoss.us/xmlrpc')

#test game data
'''
id = '258'

board = {
    '(0,0)' : ".",
    '(0,1)' : "S",
    '(0,2)' : ".",
    '(0,3)' : "A",
    '(0,4)' : ".",
    '(0,5)' : "."
}

rack = ('awhyqkl','klwsjrw')

score = ('10','18')

turn = 0

#pack it up
params = {
    'id':id, 
    'board':board, 
    'rack':rack, 
    'score':score,
    'turn':turn
}
'''
def login(creds):
    return proxy.player_login(creds)
    
def register(usr,pswd,eml):
    creds = {'user':usr,'password':pswd,'email':eml}
    return proxy.player_new(creds)

def fetch_game(id):
    fetch_game = proxy.game_get(id)
    # board    :    fetch_game[0]

def player_check(u_in):
    u_out = {'user':u_in}
    return proxy.player_check(u_out)
    
def player_lost(u_in):
    u_out = {'user':u_in}
    return proxy.player_lost(u_out)