from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import logging
import sqlite3 as lite
import time, re, os
import smtplib

con = lite.connect('crabble.db')
con.text_factory = str
cur = con.cursor()

logging.basicConfig(level=logging.DEBUG)

server = SimpleXMLRPCServer(('', 32485), logRequests=True, allow_none=True)
mailserver = smtplib.SMTP('smtp.mailserver.com', 587)

def player_lost(usr):
    mailserver.login("username", "password")

    #Send the mail
    msg = "\nHello!\nYour password is: {kwarg}".format(kwarg=password) # The /n separates the message from the headers
    mailserver.sendmail("user@mailserver.com", usr_mail, msg)

def player_check(player):
    user = player['user']
    with con:
        cur.execute("SELECT user FROM players WHERE user=?", (user,))
        user_check = cur.fetchone()
    logging.debug("Player Check: username: {kwarg}".format(kwarg=user))
    if not user_check : return False
    return True
    
def player_new(player):
    # create a unique user name, with password and email
    # see if user name exists, if not check password and email validity
    # if everything is good, return true and send user to main screen
    # if username taken return false
    user = player['user']
    password = player['password']
    email = player['email']
    print user
    if not re.match(r'[\w.-]+@[\w.-]+', email) :
        logging.debug("Registration: invalid email: {kwarg}".format(kwarg=email))
        return False
    if not player_check(player):
        with con:
            cur.execute("INSERT INTO players(user, password, email) \
                VALUES(?,?,?)", (user,password,email))
        logging.debug("Registration: new user: {kwarg}".format(kwarg=user))
        return True
    logging.debug("Registration: username unavailable: {kwarg}".format(kwarg=user))
    return False
    
def player_login(player):
    # validate username and password, return game_data if valid, false if not
    user = player['user']
    password = player['password']

    with con:
        cur.execute("SELECT password FROM players WHERE user=?", (user,))
        password_check = cur.fetchone()
    if password_check <> None and password_check[0] == password :
        logging.debug("Login: success: {kwarg}".format(kwarg=user))
        return player_data_fetch(user)
    else :
        logging.debug("Login: failure: {kwarg}".format(kwarg=user))
        return False
    
def player_data_fetch(user):
    # fetch and return player data, list of active games and invites

    with con:
        cur.execute("SELECT id, player_2, match \
            FROM player_data WHERE user=? AND state =1", (user,))
        data = cur.fetchall()
    return data
    
def player_data_match(players):    
    with con:
        cur.execute("SELECT MAX(match) FROM player_data WHERE user=? AND player_2=?", (players[0],players[1]))
        match = cur.fetchone()
        if match <> None:
            return match[0]
        else:
            return 0
            
def player_data_new(players, id):
    
    match = int(player_data_match(players)) + 1
    id = int(id)
    
    with con:
        cur.execute("INSERT INTO player_data(id,user,player_2,match,state) \
            VALUES (?,?,?,?)", (id,players[0],players[1],match,1))
        con.commit()
    return
    
def game_check(id):  
    # check if game exists or is active or ended
    id = int(id)
    with con:
        cur.execute("SELECT state FROM game WHERE id=?", (id,))
        game = cur.fetchone()
    if game <> None:
        if game[0] == 1 : return True
    return False
    
def match_check(players):
    with con:
        cur.execute("SELECT id FROM player_data WHERE user=? AND player_2=? \
            AND state=1", (players[0],players[1]))
        con.commit()
        id = cur.fetchone()
    if id == None : return False
    return id
    
def game_new(players):
    last = match_check(players)
    if last : return last
    with con:
        cur.execute("INSERT INTO game (turn,state) \
            VALUES (?,?)", (0,1))
        con.commit()
        id = cur.lastrowid
    player_data_new(players, id)
    logging.debug("Game: New: {kwarg}".format(kwarg=id))
    return True
    
def game_get(id):  
    # check if game exists or is active or ended
    id = int(id)
    if game_check(id) :
        with con:
            cur.execute("SELECT board, rack, score, turn FROM game WHERE id=?", (id,))
            game_pack = cur.fetchone()
        if game_pack <> None:
            game = []
            for i in range(len(game_pack)):
                game.append(game_pack[i])
            return game
    return False
    
def game_move(game_pack):
    id = int(game_pack['id'])
    board = game_pack['board']
    rack = game_pack['rack']
    score = game_pack['score']
    turn = int(game_pack['turn'])
    lastmove = time.strftime("%d-%m-%Y %H:%M")
    with con:
        cur.execute("UPDATE game SET board=?, rack=?, score=?, turn=?, state=1, lastmove=? \
            WHERE id=?", (board, rack, score, turn, lastmove, id))
        con.commit()
    logging.debug('Game: Move: {kwarg}'.format(kwarg=id))
    return True
    
def game_end(id):
    # mark game as ended, can be called by player wishing to surrender
    # update player victory/losses if game_state = active (1)
    id = int(id)
    lastmove = time.strftime("%d-%m-%Y %H:%M")
    with con:
        cur.execute("UPDATE game SET state=0, lastmove=? \
            WHERE id=?", (lastmove, id))
        cur.execute("UPDATE player_data SET state=0 WHERE id=?", (id,))
        con.commit()
    logging.debug('Game: End: {kwarg}'.format(kwarg=id))
    return
    
server.register_function(game_get)
server.register_function(player_new)
server.register_function(player_login)
server.register_function(player_data_fetch)
server.register_function(player_check)


try:
    print 'Use Control-C to exit'
    server.serve_forever()
except KeyboardInterrupt:
    print 'Exiting'